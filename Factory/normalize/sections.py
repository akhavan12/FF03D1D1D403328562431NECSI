from __future__ import annotations

from bs4 import BeautifulSoup
from bs4.element import Tag, NavigableString
from typing import Dict, List, Tuple

SECTION_KEYS = {
    "introductions": ["introduction", "introductions"],
    "research": ["research"],
    "policy_statements": ["policy", "policy statements", "policy statement"],
    # Include common variants and typos: "news coverage", "new coverage"
    "media_coverage": ["media", "media coverage", "news coverage", "new coverage"],
}


def _matches_heading(text: str, targets: List[str]) -> bool:
    # Normalize heading text: lowercase, strip whitespace and trailing colon
    t = (text or "").strip().rstrip(":").lower()
    return any(t.startswith(k) for k in targets)


def _domain(url: str | None) -> str | None:
    if not url:
        return None
    try:
        from urllib.parse import urlparse

        netloc = urlparse(url).netloc
        return netloc or None
    except Exception:
        return None


def _normalize_url(url: str | None) -> str | None:
    if not url:
        return None
    try:
        from urllib.parse import urlparse, urlunparse, parse_qsl, urlencode

        p = urlparse(url)
        scheme = (p.scheme or "http").lower()
        netloc = (p.netloc or p.path).lower() if not p.netloc and p.path.startswith("//") else p.netloc.lower()
        path = p.path.rstrip("/")
        # prefer https if either is present
        if scheme == "http":
            scheme = "https"
        # strip tracking params
        qs = []
        for k, v in parse_qsl(p.query, keep_blank_values=False):
            kl = k.lower()
            if kl.startswith("utm_") or kl in ("fbclid", "gclid"):
                continue
            qs.append((k, v))
        query = urlencode(qs)
        return urlunparse((scheme, netloc, path, "", query, ""))
    except Exception:
        return url


def extract_sections(cleaned_html: str) -> Tuple[Dict[str, List[dict]], str]:
    """Extract section lists and return (sections, html_without_sections).

    Heuristics:
    - Locate h1-h3 nodes that match known section names
    - Collect a contiguous region after each matched heading until next heading of same/higher level
    - From the region, extract items; then remove that region from the HTML to avoid duplication in narrative_md
    """
    soup = BeautifulSoup(cleaned_html, "lxml")
    sections: Dict[str, List[dict]] = {
        "introductions": [],
        "research": [],
        "policy_statements": [],
        "media_coverage": [],
    }
    # We'll collect ranges to remove: list of nodes belonging to matched sections
    nodes_to_remove: List = []

    headings = soup.find_all(["h1", "h2", "h3"]) or []
    for h in headings:
        text = h.get_text(" ", strip=True)
        level = int(h.name[1]) if h.name and len(h.name) == 2 else 3
        key = None
        for k, aliases in SECTION_KEYS.items():
            if _matches_heading(text, aliases):
                key = k
                break
        if not key:
            continue
        # Collect a contiguous region after the heading until the next heading
        # of the same or higher level, traversing next_elements to cross wrappers/rows/cols
        collected = []
        for el in h.next_elements:
            # Stop if we reached the heading itself again (safety)
            if el is h:
                continue
            # If we encounter another heading, decide whether to stop
            if getattr(el, "name", None) in ["h1", "h2", "h3"]:
                next_level = int(el.name[1]) if el.name and len(el.name) == 2 else 3
                if next_level <= level:
                    break
            collected.append(el)
        # From collected, parse anchors and image+caption cards
        # Build a standalone HTML fragment to avoid cross-soup node issues
        html_fragment_parts: List[str] = []
        for c in collected:
            if isinstance(c, (Tag, NavigableString)):
                html_fragment_parts.append(str(c))
        wrap = BeautifulSoup("".join(html_fragment_parts), "lxml")
        # Image cards: grid rows where left is image link and right is caption link
        if key == "media_coverage":
            items: List[dict] = []
            rows = wrap.select(".row, .sqs-row")
            if not rows:
                rows = [wrap]
            for row in rows:
                # find left image link
                left_link = None
                for a in row.find_all("a"):
                    if a.find("img") is not None:
                        left_link = a
                        break
                # find caption link (prefer external, otherwise any anchor without img)
                caption_link = None
                for a in row.find_all("a"):
                    if a is left_link:
                        continue
                    if a.find("img") is None:
                        caption_link = a
                        break
                if not (left_link or caption_link):
                    continue
                href = (left_link or caption_link).get("href")
                title = (caption_link.get_text(" ", strip=True) if caption_link else "")
                if not title and left_link:
                    img = left_link.find("img")
                    if img and img.get("alt"):
                        title = img.get("alt").strip()
                norm = _normalize_url(href)
                if not (title or norm):
                    continue
                # capture image src if available for later asset download
                img_src = None
                if left_link:
                    img = left_link.find("img")
                    if img and img.get("src"):
                        img_src = img.get("src")
                item = {"title": title, "url": norm}
                if img_src:
                    item["image_src"] = img_src
                dom = _domain(norm)
                if dom:
                    item["outlet"] = dom
                items.append(item)
            # de-duplicate by normalized URL
            seen_urls = set()
            for it in items:
                u = it.get("url")
                if u and u in seen_urls:
                    continue
                if u:
                    seen_urls.add(u)
                sections[key].append(it)
        else:
            # Only collect anchors that live inside list items to avoid duplicates
            # and unrelated in-text links. Typical patterns: li > a or li p a.
            candidates = wrap.select("li a, li p a")
            seen = set()
            for a in candidates:
                title = a.get_text(" ", strip=True)
                href = a.get("href")
                if not (title or href):
                    continue
                item: dict = {"title": title, "url": href}
                # Special parsing for policy statements to include authors/outlet/date
                if key == "policy_statements":
                    li = a.find_parent("li") or a.parent
                    li_text = li.get_text(" ", strip=True) if li else ""
                    # Normalize spaces
                    li_text_norm = " ".join(li_text.split())
                    title_norm = " ".join((title or "").split())
                    authors = None
                    outlet = None
                    date = None
                    try:
                        # Split once on first comma to get authors (prefix)
                        if "," in li_text_norm:
                            authors = li_text_norm.split(",", 1)[0].strip()
                        # Find segment after the title to parse outlet/date
                        after_title_idx = li_text_norm.lower().find(title_norm.lower())
                        if after_title_idx != -1:
                            tail = li_text_norm[after_title_idx + len(title_norm):].strip()
                            # e.g., ", NECSI (July 24, 2016)."
                            # Strip leading punctuation
                            if tail.startswith(","):
                                tail = tail[1:].strip()
                            # Extract date in parentheses
                            import re
                            m = re.search(r"\(([^)]+)\)", tail)
                            if m:
                                date = m.group(1).strip()
                                tail_wo_date = tail[:m.start()].strip()
                            else:
                                tail_wo_date = tail
                            # Remaining is outlet label
                            outlet = tail_wo_date.strip(" ,.") or None
                    except Exception:
                        pass
                    if authors:
                        item["authors"] = authors
                    if outlet:
                        item["outlet"] = outlet
                    if date:
                        item["date"] = date

                key_tuple = (item.get("url") or "", item.get("title") or "")
                if key_tuple in seen:
                    continue
                seen.add(key_tuple)
                sections[key].append(item)
        # Mark collected nodes for removal to keep narrative_md clean
        nodes_to_remove.extend([n for n in collected if getattr(n, "extract", None)])

    # Create a copy of soup and remove collected nodes
    # Note: removing in-place from original soup
    for n in nodes_to_remove:
        try:
            n.extract()
        except Exception:
            pass
    html_without_sections = str(soup)
    return sections, html_without_sections
