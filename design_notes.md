# **design_notes.md**

# Design Notes

This document explains the reasoning behind the scraper’s design, decisions, fallback logic, and limitations.


## 1. Static vs JavaScript Scraping

### Static Mode
Uses `httpx` to fetch HTML directly.  
Fast and efficient for:
- Blogs
- Docs pages
- Marketing sites without heavy JS

### When Static Fails
Static HTML often lacks:
- Lazy-loaded content
- Section text rendered by JS
- Images injected at runtime
- “Load more” elements

To detect this, we compute:
- Total extracted text length
- Number of meaningful sections
- Presence of metadata

If the content looks too small (e.g., `< 500 characters`), the scraper automatically falls back to **JS rendering**.

### JS Rendering (Playwright)
Loads and executes the full website:
- JS hydration
- Network fetches
- Client-side routing

This ensures dynamic content is captured.

---

## 2. Wait Strategy for JS Rendering

The scraper attempts to balance reliability and performance:

1. `page.goto(url, wait_until="networkidle")`
2. Scroll 3 times (`Deep Crawl` doubles this)
3. Small wait between scrolls to allow lazy content to load
4. Try clicking common expanders:
   - “Load more”
   - “Show more”
   - “More”
5. Pagination depth of 3 (`current`, `next`, `next`)

If a click fails, it is logged in the `errors` array but does not abort scraping.

---

## 3. Scroll & Click Strategy

### Scrolls
- Standard mode: 3 scrolls
- Deep crawl: 6–10 scrolls (multiplier applied)

### Clicks
Heuristics target:
- Buttons with text: “Load more”, “Show more”, “More”
- `<a rel="next">`
- Links containing the word “Next”

All interactions are logged in an `interactions.timeline`.

---

## 4. Section Grouping & Labeling

The document is chunked into meaningful UI regions.

### Landmark Elements
Primary grouping uses:
- `<header>`
- `<nav>`
- `<section>`
- `<main>`
- `<article>`
- `<footer>`

If none are meaningful, a fallback groups content by **heading parents** (`h1`, `h2`, `h3`).

### Section Labeling
Priority:
1. First heading inside section
2. Type-based label (Hero, Navigation, Footer, FAQ, Pricing)
3. First few words of the text content

### Section Types
Heuristics detect:
- Hero
- Nav
- Footer
- FAQ
- Pricing
- List
- Grid
- Generic Section

---

## 5. Noise Filtering

To avoid useless content:
- Extremely small or empty elements are skipped
- Ads / cookie banners are usually filtered out by selecting larger sections
- Inline scripts and styles are ignored

The goal is to extract meaningful user-visible sections.

---

## 6. HTML Truncation

`rawHtml` is capped at **4,000 characters**

If truncated:
- `rawHtml` contains the first 4K chars
- `truncated = true`

Purpose:
- Prevent huge payloads
- Keep API responses small
- Avoid overwhelming frontend rendering

---

## 7. Error Handling

Errors are categorized as:
- `fetch_error`
- `render_error`
- `parse_error`
- `navigation_error`

Errors never crash the scraper; they are appended to `result.errors`.

---

## 8. Known Challenges & Limitations

- Websites with bot-detection may still return 403/429  
- Infinite scroll heuristics may miss very unusual layouts  
- Extremely JS-heavy apps (React/SPA with persistent hydration) may require longer delays  
- Some content inside shadow DOMs or canvases cannot be extracted  

These limitations are normal for all general-purpose scrapers.

---

## 9. Future Improvements

- Proxy support  
- Tab-based interaction detection  
- ML-inspired section classification  
- Screenshot-based content grouping  
- Distributed crawling queue  