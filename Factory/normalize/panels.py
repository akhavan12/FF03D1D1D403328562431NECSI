from __future__ import annotations

"""
Panel extractor for Squarespace-style pages (e.g., About page).

This module exposes a single entry point:
    extract_panels(cleaned_html: str) -> list[dict]

It parses the cleaned HTML, discovers section/row groupings, and emits an
ordered list of panel dictionaries. Image URLs are left as absolute URLs; the
Factory CLI will be responsible for downloading assets and rewriting to local
paths in a subsequent step to keep responsibilities clear.

Panel dictionary shape (minimal, extensible):
{
  "type": "text" | "image" | "image-text" | "text-image" | "cta" | "html",
  "title": str | None,
  "body_md": str | None,
  "media": {"image_url": str | None, "alt": str | None} | None,
  "buttons": [{"label": str, "url": str, "style": str | None}] | [],
  "links": [{"text": str, "url": str}] | [],
  "layout": {"columns": int | None, "image_position": "left"|"right"|"full"|None, "align": str | None},
  "id": str | None,
}

Notes:
- This is heuristic-based and optimized for Squarespace DOMs (classes like
  sqs-section, sqs-row, sqs-block-image, sqs-block-html, sqs-block-button).
- Keep this extractor side-effect free (no file I/O). The CLI will:
  - download images (using normalize.assets)
  - rewrite panel media.image_url to local /assets/... paths
  - persist panels into content/<slug>/content.json
- We keep a light touch: if layout is ambiguous, prefer a generic type and
  preserve text as Markdown.
"""

from bs4 import BeautifulSoup
from typing import Any, Dict, List, Optional, Tuple
import re

# We reuse the HTML->Markdown converter used elsewhere to normalize text blocks
from normalize.normalize import html_to_markdown


def _text_or_none(s: Optional[str]) -> Optional[str]:
    s = (s or "").strip()
    return s if s else None


def _first_bg_image_url(node) -> Optional[str]:
    """Return a background-image url(...) from style if present, else None."""
    style = node.get("style") if hasattr(node, "get") else None
    if not style:
        return None


def _bg_image_from_css(soup: BeautifulSoup, sec_id: Optional[str]) -> Optional[str]:
    """Scan first few <style> tags for a rule targeting #<sec_id> with background-image."""
    if not sec_id:
        return None
    pat = re.compile(r"#" + re.escape(sec_id) + r"[^\{]*\{[^}]*background-image\s*:\s*url\(([^)]+)\)", re.I)
    for sty in soup.find_all("style")[:5]:
        css = sty.get_text() or ""
        m = pat.search(css)
        if m:
            return m.group(1).strip("\"'")
    return None
    m = re.search(r"background-image\s*:\s*url\(([^)]+)\)", style, flags=re.I)
    if m:
        return m.group(1).strip("\"'")
    return None


def _collect_buttons(block) -> List[Dict[str, Optional[str]]]:
    out: List[Dict[str, Optional[str]]] = []
    # Squarespace often uses anchor tags styled as buttons
    for a in block.select("a"):
        text = (a.get_text(" ", strip=True) or "").strip()
        href = a.get("href")
        classes = " ".join(a.get("class", [])).lower()
        is_button = "button" in classes or a.get("role") == "button"
        if href and (is_button or text):
            out.append({"label": text or href, "url": href, "style": None})
    return out


def _panel_type_from_children(nodes: List[Any]) -> str:
    # Very light heuristic: if both image and text-like blocks present, choose combo
    has_img = any(n.name == "img" or (n.has_attr("class") and any("image" in c for c in n.get("class", []))) for n in nodes)
    has_text = any(n.name in ("p", "h1", "h2", "h3", "h4", "h5", "h6") or (n.has_attr("class") and any("html" in c or "text" in c for c in n.get("class", []))) for n in nodes)
    if has_img and has_text:
        # Position guessing handled later
        return "image-text"
    if has_img:
        return "image"
    if has_text:
        return "text"
    return "html"


def _extract_image_candidate(block) -> Tuple[Optional[str], Optional[str]]:
    # Try <img src> first
    img = block.find("img")
    if img and img.get("src"):
        return img.get("src"), _text_or_none(img.get("alt"))
    # Try background-image on the container
    bg = _first_bg_image_url(block)
    if bg:
        return bg, None
    return None, None


def extract_panels(cleaned_html: str) -> List[Dict[str, Any]]:
    soup = BeautifulSoup(cleaned_html, "lxml")

    # Identify top-level sections; Squarespace uses various wrappers.
    # Fallback to visible <section> or div.sqs-section; else use large rows.
    sections = soup.select("section, div.sqs-section, div.section")
    if not sections:
        sections = soup.select("div.sqs-row, div.row")
    if not sections:
        # As a last resort, treat the body as one panel
        body_md = html_to_markdown(cleaned_html)
        return [{
            "type": "html",
            "title": None,
            "body_md": body_md,
            "media": None,
            "buttons": [],
            "links": [],
            "layout": {"columns": None, "image_position": None, "align": None},
            "id": None,
        }]

    panels: List[Dict[str, Any]] = []

    for idx, sec in enumerate(sections, start=1):
        # Within a section, look for common block containers
        blocks = sec.select(
            ",".join([
                "div.sqs-block-image",
                "div.sqs-block-html",
                "div.sqs-block-button",
                "div.sqs-block",
                "div.column",
            ])
        )
        # Title candidate: first heading inside this section
        heading = sec.find(["h1", "h2", "h3"]) 
        title = _text_or_none(heading.get_text(" ", strip=True)) if heading else None
        # Gather plain text content (excluding button areas) into Markdown
        # Clone the section, remove button areas, then convert
        sec_clone = BeautifulSoup(str(sec), "lxml")
        for btnblk in sec_clone.select("div.sqs-block-button"):
            btnblk.decompose()
        body_md = html_to_markdown(str(sec_clone))
        # Collect image URLs present in this section
        image_urls: List[str] = []
        for im in sec.select("img[src]"):
            u = (im.get("src") or "").strip()
            if u and u not in image_urls:
                image_urls.append(u)
        # Try to isolate primary image (if any)
        image_url, image_alt = _extract_image_candidate(sec)
        # If not found, walk ancestors (up to 2) for background-image
        if not image_url:
            cur = sec
            hops = 0
            while cur is not None and hops < 2 and not image_url:
                bg = _first_bg_image_url(cur)
                if bg:
                    image_url = bg
                    break
                cur = cur.parent if hasattr(cur, "parent") else None
                hops += 1
        # If still not found, try CSS <style> blocks that target this section id
        if not image_url:
            image_url = _bg_image_from_css(soup, sec.get("id"))
        # Record discovered bg candidate into image_urls list
        if image_url and image_url not in image_urls:
            image_urls.append(image_url)
        # Buttons
        buttons = []
        for btnblk in sec.select("div.sqs-block-button"):
            buttons.extend(_collect_buttons(btnblk))
        # Layout hints
        layout = {"columns": None, "image_position": None, "align": None}
        # Simple left/right guess: if first image appears before first paragraph
        first_img = sec.find("img")
        first_p = sec.find("p")
        if first_img and first_p:
            layout["image_position"] = "left" if first_img.sourceline and first_p.sourceline and first_img.sourceline < first_p.sourceline else "right"
        # Assemble panel
        ptype = _panel_type_from_children([first_img] if first_img else [])
        if ptype == "html" and (title or (body_md and body_md.strip())):
            ptype = "text"
        panels.append({
            "type": ptype,
            "title": title,
            "body_md": body_md,
            "media": {"image_url": image_url, "alt": image_alt} if image_url else None,
            "buttons": buttons,
            "links": [],
            "image_urls": image_urls,
            "layout": layout,
            "id": sec.get("id") or f"sec-{idx:03d}",
        })

    return panels
