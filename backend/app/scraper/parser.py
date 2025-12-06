# backend/app/scraper/parser.py
from typing import Any, Dict, List, Tuple
from urllib.parse import urljoin

from bs4 import BeautifulSoup


def parse_document(
    input_url: str,
    html: str,
    base_url: str,
    strategy: str,
) -> Dict[str, Any]:
    soup = BeautifulSoup(html, "lxml")

    meta = extract_meta(soup, base_url)
    # Extra helper field, not required but useful
    meta["strategy"] = strategy

    sections = extract_sections(soup, base_url)

    from .utils import utc_now_iso
    return {
        "url": input_url,
        "scrapedAt": utc_now_iso(),
        "meta": meta,
        "sections": sections,
    }


def extract_meta(soup: BeautifulSoup, base_url: str) -> Dict[str, Any]:
    # Title
    title = ""
    if soup.title and soup.title.string:
        title = soup.title.string.strip()
    og_title = soup.find("meta", property="og:title")
    if og_title and og_title.get("content"):
        title = og_title["content"].strip() or title

    # Description
    description = ""
    desc_meta = soup.find("meta", attrs={"name": "description"})
    if desc_meta and desc_meta.get("content"):
        description = desc_meta["content"].strip()
    og_desc = soup.find("meta", property="og:description")
    if og_desc and og_desc.get("content"):
        description = og_desc["content"].strip() or description

    # Language
    lang = ""
    html_tag = soup.find("html")
    if html_tag and html_tag.get("lang"):
        lang = html_tag["lang"].strip()

    # Canonical
    canonical = None
    canonical_link = soup.find("link", rel="canonical")
    if canonical_link and canonical_link.get("href"):
        canonical = urljoin(base_url, canonical_link["href"].strip())

    return {
        "title": title or "",
        "description": description or "",
        "language": lang or "",
        "canonical": canonical,
    }


def extract_sections(soup: BeautifulSoup, base_url: str) -> List[Dict[str, Any]]:
    sections: List[Dict[str, Any]] = []

    # Primary: landmark tags (helps avoid noise)
    candidates = soup.find_all(
        ["header", "nav", "main", "section", "footer", "article"]
    )

    # Fallback: heading-based
    if not candidates:
        heading_parents = set()
        for h in soup.find_all(["h1", "h2", "h3"]):
            if h.parent:
                heading_parents.add(h.parent)
        candidates = list(heading_parents)

    for idx, el in enumerate(candidates):
        text_content = el.get_text(strip=True)
        if not text_content:
            continue

        sec_type = guess_section_type(el)
        label = derive_label(el, sec_type)
        content = extract_content_from_section(el, base_url)
        raw_html, truncated = truncate_html(str(el))

        sections.append(
            {
                "id": f"{sec_type}-{idx}",
                "type": sec_type,
                "label": label,
                "sourceUrl": base_url,
                "content": content,
                "rawHtml": raw_html,
                "truncated": truncated,
            }
        )

    if not sections:
        # Extreme fallback: body as one section
        body = soup.body or soup
        content = extract_content_from_section(body, base_url)
        raw_html, truncated = truncate_html(str(body))
        sections.append(
            {
                "id": "section-0",
                "type": "section",
                "label": "Main content",
                "sourceUrl": base_url,
                "content": content,
                "rawHtml": raw_html,
                "truncated": truncated,
            }
        )

    return sections


def guess_section_type(el) -> str:
    tag = (el.name or "").lower()
    classes = " ".join(el.get("class", [])).lower() if el.get("class") else ""
    text = el.get_text(" ", strip=True).lower()

    if tag == "nav":
        return "nav"
    if tag == "footer":
        return "footer"
    if tag == "header" or "hero" in classes or "banner" in classes:
        return "hero"
    if "faq" in classes or "faq" in text:
        return "faq"
    if "pricing" in classes or "pricing" in text:
        return "pricing"
    if tag in ["ul", "ol"]:
        return "list"
    if "grid" in classes:
        return "grid"

    return "section"


def derive_label(el, sec_type: str) -> str:
    heading = el.find(["h1", "h2", "h3"])
    if heading and heading.get_text(strip=True):
        return heading.get_text(strip=True)

    if sec_type == "hero":
        return "Hero"
    if sec_type == "nav":
        return "Navigation"
    if sec_type == "footer":
        return "Footer"
    if sec_type == "faq":
        return "FAQ"
    if sec_type == "pricing":
        return "Pricing"

    text = el.get_text(" ", strip=True)
    words = text.split()
    if words:
        return " ".join(words[:7])
    return "Section"


def extract_content_from_section(el, base_url: str) -> Dict[str, Any]:
    # Headings
    headings = [
        h.get_text(" ", strip=True)
        for h in el.find_all(["h1", "h2", "h3"])
        if h.get_text(strip=True)
    ]

    # Text (p + li)
    text_parts = [
        p.get_text(" ", strip=True)
        for p in el.find_all(["p", "li"])
        if p.get_text(strip=True)
    ]
    text = " ".join(text_parts)

    # Links
    links = []
    for a in el.find_all("a", href=True):
        href = urljoin(base_url, a["href"].strip())
        link_text = a.get_text(" ", strip=True)
        links.append({"text": link_text, "href": href})

    # Images
    images = []
    for img in el.find_all("img", src=True):
        src = urljoin(base_url, img["src"].strip())
        alt = img.get("alt", "") or ""
        images.append({"src": src, "alt": alt})

    # Lists
    lists: List[List[str]] = []
    for lst in el.find_all(["ul", "ol"]):
        items = [
            li.get_text(" ", strip=True)
            for li in lst.find_all("li")
            if li.get_text(strip=True)
        ]
        if items:
            lists.append(items)

    # Tables
    tables = []
    for table in el.find_all("table"):
        rows = []
        for tr in table.find_all("tr"):
            cols = [
                td.get_text(" ", strip=True)
                for td in tr.find_all(["td", "th"])
                if td.get_text(strip=True)
            ]
            if cols:
                rows.append(cols)
        if rows:
            tables.append(rows)

    return {
        "headings": headings,
        "text": text,
        "links": links,
        "images": images,
        "lists": lists,
        "tables": tables,
    }


def truncate_html(html: str, limit: int = 4000) -> Tuple[str, bool]:
    if len(html) <= limit:
        return html, False
    return html[:limit], True
