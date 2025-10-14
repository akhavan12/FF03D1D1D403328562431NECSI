from __future__ import annotations

import plistlib
from pathlib import Path
from typing import Optional, Tuple
from bs4 import BeautifulSoup


def extract_main_html(path: Path) -> Tuple[Optional[str], str, Optional[str]]:
    """Extract main URL, HTML string, and title from a .webarchive file.

    Returns: (url, html, title)
    """
    with path.open("rb") as f:
        data = plistlib.load(f)
    main = data.get("WebMainResource") or {}
    url = main.get("WebResourceURL")
    raw = main.get("WebResourceData") or b""
    html = raw.decode("utf-8", errors="replace")
    title: Optional[str] = None
    try:
        soup = BeautifulSoup(html, "lxml")
        if soup.title and soup.title.string:
            title = soup.title.string.strip()
    except Exception:
        pass
    return url, html, title
