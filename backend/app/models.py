from typing import Literal

from pydantic import BaseModel, HttpUrl


class ScrapeRequest(BaseModel):
    """
    Request model for /scrape.

    Extra fields:
    - mode: "auto" | "static" | "js"
    - deep: if True, use more aggressive scroll/pagination
    Both are OPTIONAL and default to assignment-compatible behaviour.
    """
    url: HttpUrl
    mode: Literal["auto", "static", "js"] = "auto"
    deep: bool = False
