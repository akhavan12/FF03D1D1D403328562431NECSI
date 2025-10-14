from __future__ import annotations

from bs4 import BeautifulSoup
from typing import Optional


def clean_html(html: str, cleanup_cfg: dict) -> str:
    """Apply Stage-2 cleanup rules to strip chrome and layout cruft.

    Steps:
    - Remove <script>, <style>, <link rel=stylesheet>, and JSON/script data blocks
    - Optionally isolate a content root if a hint is provided
    - Remove denylisted selectors
    - Remove forms and selects (common source of massive option lists like country codes)
    - Drop inline style attributes
    - Return serialized HTML of cleaned content root (or full doc if no root found)
    """
    soup = BeautifulSoup(html, "lxml")

    # 1) Remove scripts, styles, and stylesheet links
    for tag in soup.find_all(["script", "style"]):
        tag.decompose()
    for link in soup.find_all("link"):
        if link.get("rel") and "stylesheet" in [r.lower() for r in link.get("rel")]:
            link.decompose()

    # 2) Identify content root via hint selector(s)
    root = soup
    hint = (cleanup_cfg or {}).get("content_root_hint")
    if hint:
        # Try multiple comma-separated selectors in order
        for sel in [s.strip() for s in hint.split(",") if s.strip()]:
            found = soup.select_one(sel)
            if found:
                root = found
                break

    # 3) Remove denylisted selectors within the chosen root
    denylist = (cleanup_cfg or {}).get("denylist", [])
    for sel in denylist:
        for node in root.select(sel):
            node.decompose()

    # 4) Remove forms and selects (often contain giant option lists)
    for tag in root.find_all(["form", "select", "option", "input", "textarea", "button"]):
        tag.decompose()

    # 5) Remove inline style attributes from remaining tags
    for t in root.find_all(True):
        if t.has_attr("style"):
            del t["style"]

    # Serialize only the content root if it's not the full document
    # If root is soup, return the whole cleaned document; otherwise return the fragment's HTML
    if root is soup:
        return str(soup)
    else:
        # Wrap fragment to keep a valid HTML string
        frag = BeautifulSoup("<div></div>", "lxml")
        frag_div = frag.div
        # Append children of root to frag
        for child in list(root.children):
            frag_div.append(child if child is not None else "")
        return str(frag_div)
