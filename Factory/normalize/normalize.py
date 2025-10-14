from __future__ import annotations

from typing import Tuple
from bs4 import BeautifulSoup
from markdownify import markdownify as md


def html_to_markdown(html: str) -> str:
    # Convert HTML to reasonably clean Markdown
    return md(html, heading_style="ATX", strip=['script', 'style'])


def extract_title_and_summary(html: str, fallback_title: str | None = None) -> Tuple[str, str]:
    soup = BeautifulSoup(html, "lxml")
    title = fallback_title or (soup.title.string.strip() if soup.title and soup.title.string else "Untitled")
    # Build a short summary: first 2 sentences from text
    text = " ".join(s.strip() for s in soup.stripped_strings)
    # naive sentence split
    parts = text.split('. ')
    summary = '. '.join(parts[:2]).strip()
    if summary and not summary.endswith('.'):
        summary += '.'
    return title, summary[:400]
