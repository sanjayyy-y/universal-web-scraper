# Universal Website Scraper (Full-Stack Assignment)

A full-stack “Universal Website Scraper” capable of handling both static and JavaScript-rendered pages, performing automated interactions (scrolling, clicks, pagination), extracting meaningful content sections, and returning a normalized JSON schema.  
Built with **FastAPI**, **Playwright**, and a **React (Vite)** frontend.

This project was completed as part of the Lyftr AI Full-Stack Assignment.

---

## Features

### Static + JavaScript Scraping  
- First attempts **static HTML fetch** for speed.  
- Automatically switches to **Playwright JS rendering** if content appears incomplete (heuristic-based).  
- Configurable through a “Mode” selector in the UI.

### Section-Based Content Extraction  
Scraper groups content into meaningful sections:
- Hero  
- Navigation  
- Footer  
- Section blocks  
- Lists  
- Tables  
- Images  
Each section includes:
- Clean text  
- Headings  
- Links  
- Raw HTML (truncated)  
- Source URL  
- Section label and type  

### Interaction Timeline  
During JS scraping, all interactions are logged:
- Scroll events  
- Load-more clicks  
- Pagination navigation  
- Final rendered page URLs  

Displayed clearly in the UI.

### Deep Crawl Mode  
Enables aggressive exploration:
- Multiple scroll rounds  
- Additional “Load more” attempts  
- Pagination depth ≥ 3  

Useful for dynamic, long pages (news feeds, blogs, marketing pages).

### Frontend Viewer  
A simple interface to:
- Enter URL  
- Select scraping mode  
- Toggle deep crawl  
- View sections as collapsible cards  
- Inspect raw JSON  
- Download result  


## Tech Stack

**Backend:**  
- FastAPI  
- Playwright (Chromium)  
- httpx  
- BeautifulSoup  
- Pydantic v2 + pydantic-settings  

**Frontend:**  
- React  
- Vite  
- Axios  


## Project Structure

## Project Structure

```text
lyftr-scraper/
├── backend/
│   └── app/
│       ├── main.py
│       ├── config.py
│       ├── models.py
│       └── scraper/
│           ├── static_scraper.py
│           ├── js_scraper.py
│           ├── parser.py
│           └── utils.py
├── frontend/
│   ├── index.html
│   ├── vite.config.js
│   └── src/
│       ├── App.jsx
│       ├── main.jsx
│       └── components/
│           ├── SectionList.jsx
│           └── JsonViewer.jsx
├── run.sh
├── design_notes.md
├── capabilities.json
└── requirements.txt



##  How to Run

From the project root:

```bash
chmod +x run.sh
./run.sh

