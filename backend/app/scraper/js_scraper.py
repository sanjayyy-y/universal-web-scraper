# backend/app/scraper/js_scraper.py
from typing import Any, Dict, List

from playwright.async_api import async_playwright

from ..config import settings
from .parser import parse_document
from .utils import classify_error, record_event


async def scrape_with_js(
    url: str,
    interactions: Dict[str, Any],
    errors: List[Dict[str, str]],
    deep: bool = False,
) -> Dict | None:
    """
    Playwright-based JS rendering with:
    - scroll depth >= 3
    - clicks on load more / show more
    - pagination via next links
    """
    scroll_rounds = 3 * (settings.deep_scroll_multiplier if deep else 1)

    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()

            await page.goto(
                url,
                wait_until="networkidle",
                timeout=settings.js_timeout,
            )
            record_event(interactions, "js_goto", "Initial JS navigation", url=page.url)

            # Scroll (infinite scroll style)
            for i in range(scroll_rounds):
                await page.evaluate("window.scrollBy(0, document.body.scrollHeight);")
                interactions["scrolls"] += 1
                record_event(
                    interactions,
                    "scroll",
                    f"Scroll #{i + 1}",
                    url=page.url,
                )
                await page.wait_for_timeout(1500)

            # "Load more" / "Show more"
            load_more_selectors = [
                "text=Load more",
                "text=Show more",
                "text=More",
            ]
            for sel in load_more_selectors:
                try:
                    btn = await page.query_selector(sel)
                    if btn:
                        interactions["clicks"].append(sel)
                        record_event(
                            interactions,
                            "click",
                            f"Click {sel}",
                            url=page.url,
                        )
                        await btn.click()
                        await page.wait_for_timeout(2000)
                except Exception:
                    continue

            # Pagination: try to reach at least 3 pages total
            max_extra_pages = 2 if not deep else 4
            for i in range(max_extra_pages):
                next_link = await page.query_selector("a[rel='next']")
                if not next_link:
                    next_link = await page.query_selector("text=Next")
                if not next_link:
                    break

                interactions["clicks"].append("pagination-next")
                record_event(
                    interactions,
                    "click",
                    "Click pagination-next",
                    url=page.url,
                )
                await next_link.click()
                await page.wait_for_load_state("networkidle")
                if page.url not in interactions["pages"]:
                    interactions["pages"].append(page.url)
                record_event(
                    interactions,
                    "navigation",
                    f"Navigated to {page.url}",
                    url=page.url,
                )

            html = await page.content()
            current_url = page.url
            await browser.close()

        result = parse_document(
            input_url=url,
            html=html,
            base_url=current_url,
            strategy="js",
        )
        return result

    except Exception as exc:
        errors.append(classify_error(exc, phase="render"))
        return None