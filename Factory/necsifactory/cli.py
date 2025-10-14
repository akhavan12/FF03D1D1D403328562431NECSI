from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

import typer
from rich import print as rprint
from rich.table import Table
from ingest.webarchive import extract_main_html
from normalize.normalize import html_to_markdown, extract_title_and_summary
from normalize.cleanup import clean_html
from normalize.sections import extract_sections
from normalize.assets import download_and_rewrite_assets, download_single
from normalize.panels import extract_panels
import hashlib
import yaml
from bs4 import BeautifulSoup
import re
import plistlib
from urllib.parse import urlparse, parse_qs

APP = typer.Typer(help="NECSI Content Foundry CLI (Factory)")

BASE_DIR = Path(__file__).resolve().parents[1]
STATE_DIR = BASE_DIR / "orchestrator" / "state"
CONTENT_DIR = BASE_DIR / os.getenv("FACTORY_CONTENT_DIR", "content")
ASSETS_DIR = BASE_DIR / os.getenv("FACTORY_ASSETS_DIR", "public_assets")
JOBS_DIR = BASE_DIR / os.getenv("FACTORY_JOBS_DIR", "jobs")
SCHEMAS_DIR = BASE_DIR / "schemas"
SOURCES_DIR = BASE_DIR / "sources"
DEBUG_DIR = JOBS_DIR / "debug"

STATE_DIR.mkdir(parents=True, exist_ok=True)
CONTENT_DIR.mkdir(parents=True, exist_ok=True)
ASSETS_DIR.mkdir(parents=True, exist_ok=True)
(JOBS_DIR / "reports").mkdir(parents=True, exist_ok=True)
SOURCES_DIR.mkdir(parents=True, exist_ok=True)
DEBUG_DIR.mkdir(parents=True, exist_ok=True)


def _state_path(slug: str) -> Path:
    return STATE_DIR / f"{slug}.json"


def _now_iso() -> str:
    # Use timezone-aware UTC timestamps
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _load_yaml(p: Path, default: dict) -> dict:
    if p.exists():
        return yaml.safe_load(p.read_text()) or default
    return default


def _sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


# --- Squarespace hero utility helpers -------------------------------------------------
def _images_from_webarchive(path: Path) -> list[str]:
    """Extract image URLs in capture order from a .webarchive/.plist/.xml file.
    Falls back to an empty list if parsing fails.
    """
    try:
        with path.open("rb") as f:
            data = plistlib.load(f)
    except Exception:
        return []

    found: list[str] = []

    def _walk(node):
        if isinstance(node, dict):
            url = node.get("WebResourceURL")
            mime = node.get("WebResourceMIMEType", "")
            if url and ("images.squarespace-cdn.com" in url or (isinstance(mime, str) and mime.startswith("image/"))):
                found.append(url)
            for v in node.values():
                _walk(v)
        elif isinstance(node, list):
            for v in node:
                _walk(v)

    _walk(data)
    # de-dupe preserving order
    seen = set()
    out: list[str] = []
    for u in found:
        if u not in seen:
            seen.add(u)
            out.append(u)
    return out


def _width_hint(u: str) -> int:
    q = parse_qs(urlparse(u).query)
    fmt = q.get("format", [""])[0]
    m = re.match(r"(\d+)w$", fmt)
    return int(m.group(1)) if m else 0


def _pick_logo_banner(urls: list[str]) -> tuple[Optional[str], Optional[str]]:
    logo = None
    banner = None
    # Prefer explicit favicon/logo for logo
    for u in urls:
        fn = os.path.basename(urlparse(u).path).lower()
        if "favicon" in fn or "logo" in fn:
            logo = u
            break
    if not logo and urls:
        logo = urls[0]

    start = urls.index(logo) if logo in urls else -1
    seq = urls[(start + 1):] if start >= 0 else urls
    for u in seq:
        fn = os.path.basename(urlparse(u).path).lower()
        if "favicon" in fn or "logo" in fn:
            continue
        # prefer large images if hint exists
        if _width_hint(u) >= 1200 or True:
            banner = u
            break
    if not banner and len(urls) >= 2:
        banner = urls[1]
    return logo, banner


@APP.command()
def version():
    """Show version and paths."""
    from . import __version__

    rprint({
        "version": __version__,
        "base": str(BASE_DIR),
        "content": str(CONTENT_DIR),
        "assets": str(ASSETS_DIR),
        "jobs": str(JOBS_DIR),
    })


@APP.command()
def ingest(
    add: Optional[Path] = typer.Option(
        None, "--add", help="Path to incoming source file (webarchive/html/xml)"
    ),
    slug: Optional[str] = typer.Option(None, "--slug", help="Target slug"),
):
    """Register raw source into the pipeline (INGESTED state)."""
    if not add or not slug:
        raise typer.BadParameter("--add and --slug are required")
    if not add.exists():
        raise typer.BadParameter(f"Incoming file not found: {add}")

    state = {
        "slug": slug,
        "status": "INGESTED",
        "timestamps": {"INGESTED": _now_iso()},
        "artifacts": {"source_path": str(add)},
        "checksums": {},
        "diffs": {},
    }
    _state_path(slug).write_text(json.dumps(state, indent=2))
    # If webarchive/html, extract and store sources/<slug>/raw.html for Stage-2
    ext = add.suffix.lower()
    if ext in [".webarchive", ".html", ".htm"]:
        try:
            if ext == ".webarchive":
                url, html, title = extract_main_html(add)
            else:
                html = add.read_text(errors="replace")
                url, title = None, None
            slug_dir = SOURCES_DIR / slug
            slug_dir.mkdir(parents=True, exist_ok=True)
            (slug_dir / "raw.html").write_text(html)
            # seed manifests
            (slug_dir / "asset_manifest.json").write_text(json.dumps({"assets": []}, indent=2))
            (slug_dir / "dom_map.json").write_text(json.dumps({"notes": "TODO: populate DOM map"}, indent=2))
            # persist basic provenance
            st = json.loads(_state_path(slug).read_text())
            st.setdefault("metadata", {})["url"] = url
            st["metadata"]["title"] = title
            _state_path(slug).write_text(json.dumps(st, indent=2))
        except Exception as e:
            rprint(f"[yellow]WARN[/] Could not pre-extract raw.html: {e}")
    rprint(f"[green]INGESTED[/] {slug} ← {add}")


@APP.command()
def run(
    slug: str = typer.Argument(..., help="Slug to process"),
    to: str = typer.Option("SCHEMA_VALID", "--to", help="Target state"),
    open_diff: bool = typer.Option(False, "--open-diff", help="Preview diff after run"),
    force: bool = typer.Option(False, "--force", help="Recompute intermediate artifacts"),
    replace: bool = typer.Option(False, "--replace", help="Allow overwriting existing content outputs"),
    snapshot: bool = typer.Option(False, "--snapshot", help="Create snapshot before overwriting content outputs"),
    dry_run: bool = typer.Option(False, "--dry-run", help="Simulate without writing content outputs"),
):
    """Process a single slug through the pipeline up to a target state."""
    sp = _state_path(slug)
    if not sp.exists():
        raise typer.BadParameter(f"No state found for slug: {slug}. Run 'ingest' first.")

    state = json.loads(sp.read_text())
    current = state.get("status", "INGESTED")
    # If forcing, rewind the state machine to re-run all steps deterministically
    if force:
        current = "INGESTED"
        state["status"] = current
        state.setdefault("timestamps", {})[current] = _now_iso()
    # Placeholder transitions; in future, call into ingest/normalize/validate modules
    wanted_order = [
        "INGESTED",
        "PARSED",
        "NORMALIZED",
        "SCHEMA_VALID",
        "BUILT",
        "INDEXED",
    ]
    if to not in wanted_order:
        raise typer.BadParameter(f"Unknown target state: {to}")

    while current != to:
        idx = wanted_order.index(current)
        nxt = wanted_order[idx + 1]
        # For force runs, allow recomputing from earlier stages
        if force and wanted_order.index(nxt) <= wanted_order.index(to):
            state["status"] = nxt
            state.setdefault("timestamps", {})[nxt] = _now_iso()
        else:
            state["status"] = nxt
            state.setdefault("timestamps", {})[nxt] = _now_iso()
        # Realistic transitions with simple parsing/normalization
        if nxt == "PARSED":
            # Ensure sources/<slug>/raw.html exists; if not, extract from original source
            slug_dir = SOURCES_DIR / slug
            raw_path = slug_dir / "raw.html"
            if not raw_path.exists():
                src = state.get("artifacts", {}).get("source_path")
                if not src:
                    raise typer.BadParameter("Missing source_path in state; re-ingest required.")
                add = BASE_DIR / src
                if add.suffix.lower() == ".webarchive":
                    url, html, title = extract_main_html(add)
                else:
                    html = add.read_text(errors="replace")
                    url, title = None, None
                slug_dir.mkdir(parents=True, exist_ok=True)
                raw_path.write_text(html)
                state.setdefault("metadata", {})["url"] = url
                state["metadata"]["title"] = title
            # Write debug copy
            dbg_dir = DEBUG_DIR / slug
            dbg_dir.mkdir(parents=True, exist_ok=True)
            (dbg_dir / "raw.html").write_text(raw_path.read_text())
            state.setdefault("artifacts", {})["parsed_html"] = str(raw_path.relative_to(BASE_DIR))
        elif nxt == "NORMALIZED":
            parsed_html_path = state.get("artifacts", {}).get("parsed_html")
            if not parsed_html_path:
                raise typer.BadParameter("No parsed_html artifact; cannot normalize.")
            html = (BASE_DIR / parsed_html_path).read_text()
            # Load cleanup config and apply Stage-2 cleanup before Markdown conversion
            cleanup_cfg = _load_yaml(BASE_DIR / "config" / "cleanup.yml", {})
            cleaned_html = clean_html(html, cleanup_cfg)
            # Extract a hero subtitle: first h3 near top, then remove it
            subtitle = None
            try:
                soup_sub = BeautifulSoup(cleaned_html, "lxml")
                h3 = soup_sub.find("h3")
                if h3:
                    subtitle = h3.get_text(" ", strip=True)
                    h3.extract()
                cleaned_html = str(soup_sub)
            except Exception:
                pass
            # Extract hero/banner image from background-image near top (avoid media card imgs)
            hero_image = None
            try:
                soup_hero = BeautifulSoup(cleaned_html, "lxml")
                # background-image in inline style (scan only first ~50 tags)
                import re as _re
                candidate = None
                for i, tag in enumerate(soup_hero.find_all(True)):
                    if i > 50:
                        break
                    style = tag.get("style")
                    if not style:
                        continue
                    m = _re.search(r"background-image\s*:\s*url\(([^)]+)\)", style, flags=_re.I)
                    if m:
                        u = m.group(1).strip('"\'')
                        if u.startswith("http://") or u.startswith("https://"):
                            candidate = u
                            break
                # Squarespace-specific: derive base id from *_intro or Intro-content block
                if not candidate:
                    base_id = None
                    # find id that ends with _intro
                    el_intro = soup_hero.find(True, id=_re.compile(r".+_intro$")) or soup_hero.find(True, class_=_re.compile(r"\bIntro-content\b"))
                    if el_intro and el_intro.get('id') and el_intro['id'].endswith('_intro'):
                        base_id = el_intro['id'].removesuffix('_intro')
                    # probe by base id: element with same id or data-section-id equals base
                    if base_id:
                        # Check element with exact id
                        target = soup_hero.find(True, id=base_id)
                        if not target:
                            target = soup_hero.find(True, attrs={"data-section-id": base_id})
                        # inspect styles on target and parents up to 3 levels
                        def _extract_bg_url(node):
                            if not node:
                                return None
                            st = node.get('style')
                            if st:
                                m2 = _re.search(r"background-image\s*:\s*url\(([^)]+)\)", st, flags=_re.I)
                                if m2:
                                    uu = m2.group(1).strip('"\'')
                                    if uu.startswith('http'):
                                        return uu
                            # data attributes
                            for k in ('data-image', 'data-src', 'data-bg'):
                                if node.get(k) and str(node.get(k)).startswith('http'):
                                    return node.get(k)
                            return None
                        cur = target
                        hops = 0
                        while not candidate and cur is not None and hops < 3:
                            u2 = _extract_bg_url(cur)
                            if u2:
                                candidate = u2
                                break
                            cur = cur.parent if hasattr(cur, 'parent') else None
                            hops += 1
                        # parse early <style> blocks for rules matching the base id
                        if not candidate:
                            # Look at the first few style tags only
                            for sty in soup_hero.find_all('style')[:5]:
                                css = sty.get_text() or ''
                                # patterns: #<base_id> { background-image: url(...) }
                                # or [data-section-id="<base_id>"] { background-image: url(...) }
                                # Build regex patterns without f-strings to avoid brace conflicts
                                pat1 = r"#[\w-]*" + _re.escape(base_id) + r"[\w-]*[^\{]*\{[^}]*background-image\s*:\s*url\(([^)]+)\)"
                                pat2 = r"\[data-section-id=\"" + _re.escape(base_id) + r"\"\][^\{]*\{[^}]*background-image\s*:\s*url\(([^)]+)\)"
                                mcss = _re.search(pat1, css, flags=_re.I) or _re.search(pat2, css, flags=_re.I)
                                if mcss:
                                    uu = mcss.group(1).strip('"\'')
                                    if uu.startswith('http'):
                                        candidate = uu
                                        break
                # Fallback: use webarchive resource order to pick banner (Squarespace rule)
                if not candidate:
                    try:
                        src_path = state.get("artifacts", {}).get("source_path")
                        if src_path:
                            wa_path = BASE_DIR / src_path
                            if wa_path.exists():
                                urls = _images_from_webarchive(wa_path)
                                _logo, _banner = _pick_logo_banner(urls)
                                # Debug: persist discovered images and picks
                                try:
                                    dbg = {
                                        "total": len(urls),
                                        "images": urls,
                                        "logo": _logo,
                                        "banner": _banner,
                                    }
                                    hero_dbg = DEBUG_DIR / slug / "hero.json"
                                    hero_dbg.parent.mkdir(parents=True, exist_ok=True)
                                    hero_dbg.write_text(json.dumps(dbg, indent=2))
                                except Exception:
                                    pass
                                # Persist to sources/<slug>/asset_manifest.json for traceability
                                try:
                                    manifest_path = SOURCES_DIR / slug / "asset_manifest.json"
                                    manifest = {"assets": []}
                                    if manifest_path.exists():
                                        try:
                                            manifest = json.loads(manifest_path.read_text()) or manifest
                                        except Exception:
                                            pass
                                    manifest.update({
                                        "logo_url": _logo,
                                        "banner_url": _banner,
                                        "all_image_urls": urls,
                                    })
                                    manifest_path.write_text(json.dumps(manifest, indent=2))
                                except Exception:
                                    pass
                                if _banner and (_banner.startswith("http://") or _banner.startswith("https://")):
                                    candidate = _banner
                    except Exception:
                        pass
                if candidate:
                    manifest_path = SOURCES_DIR / slug / "asset_manifest.json"
                    local = download_single(candidate, slug, ASSETS_DIR, manifest_path)
                    if local:
                        hero_image = local
            except Exception:
                pass
            # Detect panel pages (incoming/panels/ or known slugs like 'about') and extract panels
            panels = None
            try:
                src_path = state.get("artifacts", {}).get("source_path", "") or ""
                is_panel_page = "/incoming/panels/" in src_path or slug == "about"
                if is_panel_page:
                    panels = extract_panels(cleaned_html)
                    # download panel media to local assets
                    manifest_path = SOURCES_DIR / slug / "asset_manifest.json"
                    for p in panels:
                        media = p.get("media") or {}
                        img_url = media.get("image_url") if isinstance(media, dict) else None
                        if img_url and (img_url.startswith("http://") or img_url.startswith("https://")):
                            try:
                                local = download_single(img_url, slug, ASSETS_DIR, manifest_path)
                                if local:
                                    p.setdefault("media", {})["image"] = local
                            except Exception:
                                pass
                    # Promote first panel heading/subheading to page-level title/subtitle
                    try:
                        if panels:
                            p0 = panels[0]
                            # Determine title from explicit panel title or a first-level heading in body_md
                            body_md = (p0.get("body_md") or "")
                            ttl = p0.get("title")
                            import re as _re2
                            if not ttl:
                                m = _re2.search(r"^#\s+(.+)$", body_md, flags=_re2.M)
                                if m:
                                    ttl = m.group(1).strip()
                            sub = None
                            m2 = _re2.search(r"^##\s+(.+)$", body_md, flags=_re2.M)
                            if m2:
                                sub = m2.group(1).strip()
                            # Strip promoted headings from the first panel body
                            if ttl or sub:
                                new_body = body_md
                                if ttl:
                                    new_body = _re2.sub(r"^#\s+.*$\n?", "", new_body, count=1, flags=_re2.M)
                                if sub:
                                    new_body = _re2.sub(r"^##\s+.*$\n?", "", new_body, count=1, flags=_re2.M)
                                p0["body_md"] = new_body
                            # Persist into normalized state placeholders via state dict later
                            state.setdefault("_panel_promote", {})
                            if ttl:
                                state["_panel_promote"]["title"] = ttl
                            if sub:
                                state["_panel_promote"]["subtitle"] = sub
                    except Exception:
                        pass
                    # If there is a secondary hero panel like 'About Complex Systems' with empty body,
                    # try to pull the H3 that immediately follows that H1 in the original HTML as its
                    # subheading; otherwise fall back to the originally extracted subtitle.
                    try:
                        _orig_subtitle = subtitle  # prior to promotion override below
                        if _orig_subtitle:
                            import re as _re3
                            from bs4 import BeautifulSoup as _BS
                            _soup = _BS(cleaned_html, "lxml")
                            # Locate the H1 titled 'About Complex Systems' (tolerate nbsp/whitespace)
                            def _norm(t):
                                return (t or "").replace("\u00a0", " ").strip().lower()
                            h1_cs = None
                            for _h1 in _soup.find_all("h1"):
                                if _norm(_h1.get_text()) == "about complex systems":
                                    h1_cs = _h1
                                    break
                            h3_text = None
                            if h1_cs is not None:
                                _n = h1_cs.find_next("h3")
                                if _n is not None:
                                    h3_text = _norm(_n.get_text())
                            dbg_choice = DEBUG_DIR / slug / "panels_h3_choice.txt"
                            try:
                                dbg_choice.parent.mkdir(parents=True, exist_ok=True)
                                dbg_choice.write_text(f"h3_text={h3_text!r}\n")
                            except Exception:
                                pass
                            for i, p in enumerate(panels):
                                ttl = (p.get("title") or "").strip().lower()
                                if ttl == "about complex systems" or p.get("id") == "cs-header":
                                    body_md = (p.get("body_md") or "")
                                    body_md2 = _re3.sub(r"^#\s+.*$\n?", "", body_md, count=1, flags=_re3.M)
                                    substantive = _re3.search(r"[A-Za-z0-9]", body_md2.replace("\u00a0", " ").strip()) is not None
                                    if not substantive:
                                        if h3_text:
                                            p["body_md"] = f"\n\n## {h3_text}\n\n"
                                        else:
                                            p["body_md"] = f"\n\n## {_orig_subtitle}\n\n"
                                    else:
                                        p["body_md"] = body_md2
                                    break
                    except Exception:
                        pass
                    # write debug panels (after adjustments)
                    dbg_dir = DEBUG_DIR / slug
                    dbg_dir.mkdir(parents=True, exist_ok=True)
                    (dbg_dir / "panels.json").write_text(json.dumps(panels, indent=2))
            except Exception:
                pass
            # Extract sections and remove them from narrative to avoid duplication
            sections, narrative_html = extract_sections(cleaned_html)
            # Post-process sections: download media images and asset-like links
            try:
                manifest_path = SOURCES_DIR / slug / "asset_manifest.json"
                # media coverage images
                mc = sections.get("media_coverage", [])
                for item in mc:
                    img_src = item.get("image_src")
                    if img_src and (img_src.startswith("http://") or img_src.startswith("https://")):
                        local = download_single(img_src, slug, ASSETS_DIR, manifest_path)
                        if local:
                            item["image"] = local
                # policy statements: download asset-like URLs (e.g., mp3) as attachment
                exts = (".mp3", ".wav", ".m4a", ".pdf")
                for item in sections.get("policy_statements", []):
                    u = item.get("url") or ""
                    ul = u.lower()
                    if (ul.startswith("http://") or ul.startswith("https://")) and any(ul.endswith(e) for e in exts):
                        local = download_single(u, slug, ASSETS_DIR, manifest_path)
                        if local:
                            item["asset"] = local
            except Exception:
                pass
            # Download and rewrite assets in the narrative region
            try:
                assets_root = ASSETS_DIR
                manifest_path = SOURCES_DIR / slug / "asset_manifest.json"
                narrative_html, _manifest = download_and_rewrite_assets(
                    narrative_html, slug, assets_root, manifest_path
                )
            except Exception:
                pass
            md = html_to_markdown(narrative_html)
            # Markdown cleanup: remove empty headings, normalize nbsp, collapse blanks
            md = md.replace("\u00a0", " ")
            md = re.sub(r"^\s{0,3}#{1,6}\s*$", "", md, flags=re.MULTILINE)
            md = re.sub(r"\n{3,}", "\n\n", md)
            # Derive title/summary
            title_fallback = state.get("metadata", {}).get("title") or slug.replace("-", " ").title()
            title, summary = extract_title_and_summary(cleaned_html, fallback_title=title_fallback)
            # Prefer on-page H1 as canonical title; strip common site suffixes
            try:
                h1 = BeautifulSoup(cleaned_html, "lxml").find("h1")
                if h1:
                    h1_text = h1.get_text(" ", strip=True)
                    if h1_text:
                        title = h1_text
                # Strip site suffixes separated by em-dash or pipe
                if "—" in title:
                    title = title.split("—", 1)[0].strip()
                if "|" in title:
                    title = title.split("|", 1)[0].strip()
            except Exception:
                pass
            norm_path = SOURCES_DIR / slug / "normalized.md"
            norm_path.write_text(md)
            # debug traces
            dbg_dir = DEBUG_DIR / slug
            (dbg_dir / "normalized.md").write_text(md)
            (dbg_dir / "cleaned.html").write_text(cleaned_html)
            (dbg_dir / "sections.json").write_text(json.dumps(sections, indent=2))
            state.setdefault("artifacts", {})["normalized_md"] = str(norm_path.relative_to(BASE_DIR))
            state.setdefault("normalized", {})["title"] = title
            state["normalized"]["summary"] = summary
            if subtitle:
                state["normalized"]["subtitle"] = subtitle
            # Apply promoted title/subtitle from panels if present. For panel pages we prefer these.
            try:
                promo = state.get("_panel_promote", {})
                # Use local `panels` variable (if extracted in this run) to detect panel pages
                is_panel_page = bool(panels) or bool(state.get("normalized", {}).get("type") == "page" or state.get("normalized", {}).get("panels"))
                if promo.get("title") and (is_panel_page or not state["normalized"].get("title")):
                    state["normalized"]["title"] = promo["title"]
                if promo.get("subtitle") and (is_panel_page or not state["normalized"].get("subtitle")):
                    state["normalized"]["subtitle"] = promo["subtitle"]
            except Exception:
                pass
            if hero_image:
                state["normalized"]["hero_image"] = hero_image
            if panels:
                state["normalized"]["type"] = "page"
                state["normalized"]["panels"] = panels
            state["normalized"]["sections"] = sections
        elif nxt == "SCHEMA_VALID":
            # Placeholder: assume valid; future step will validate against JSON Schemas and taxonomy
            state.setdefault("validation", {})["schema"] = {"ok": True}
        elif nxt == "BUILT":
            outdir = CONTENT_DIR / slug
            # Handle overwrite semantics
            if outdir.exists() and not replace and not dry_run:
                raise typer.BadParameter("Content exists; pass --replace to overwrite")
            # Snapshot if required
            if outdir.exists() and replace and not snapshot and not dry_run:
                raise typer.BadParameter("--replace requires --snapshot (or use --force)")
            if outdir.exists() and replace and snapshot and not dry_run:
                snap_dir = BASE_DIR / "dist" / f"content-{datetime.now(timezone.utc):%Y%m%d%H%M%S}-pre"
                snap_dir.mkdir(parents=True, exist_ok=True)
                manifest = {"files": []}
                for p in outdir.rglob("*"):
                    if p.is_file():
                        rel = p.relative_to(BASE_DIR)
                        data = p.read_text(errors="replace")
                        (snap_dir / rel).parent.mkdir(parents=True, exist_ok=True)
                        (snap_dir / rel).write_text(data)
                        manifest["files"].append({
                            "path": str(rel),
                            "sha256": _sha256_text(data),
                        })
                (snap_dir / "manifest.json").write_text(json.dumps(manifest, indent=2))
            if not dry_run:
                outdir.mkdir(parents=True, exist_ok=True)
            title = state.get("normalized", {}).get("title") or slug.replace("-", " ").title()
            summary = state.get("normalized", {}).get("summary") or ""
            subtitle = state.get("normalized", {}).get("subtitle")
            narrative_md = None
            norm_md_path = state.get("artifacts", {}).get("normalized_md")
            if norm_md_path and (BASE_DIR / norm_md_path).exists():
                narrative_md = (BASE_DIR / norm_md_path).read_text()
            # Minimal envelope+body blend for now
            normalized = state.get("normalized", {})
            doc_type = (
                normalized.get("type")
                or ("page" if normalized.get("panels") else None)
                or "research"
            )
            doc = {
                "schema_version": 1,
                "type": doc_type,
                "slug": slug,
                "title": title,
                "subtitle": subtitle,
                "hero_image": state.get("normalized", {}).get("hero_image"),
                "summary": summary,
                "provenance": {
                    "source_url": state.get("metadata", {}).get("url"),
                    "capture_method": "webarchive",
                    "captured_at": state.get("timestamps", {}).get("INGESTED"),
                    "checksum": "",
                },
                "narrative_md": narrative_md or "",
                "sections": state.get("normalized", {}).get("sections", {"introductions": [], "research": [], "policy_statements": [], "media_coverage": []}),
                "panels": normalized.get("panels") or [],
                "figure_assets": [],
            }
            if not dry_run:
                (outdir / "content.json").write_text(json.dumps(doc, indent=2))
        current = nxt

    sp.write_text(json.dumps(state, indent=2))
    rprint(f"[cyan]{slug}[/] progressed to [bold]{to}[/]")
    if open_diff:
        rprint("(diff preview placeholder)")


batch_app = typer.Typer(help="Batch operations")


@batch_app.command("run")
def batch_run(
    from_state: str = typer.Option("INGESTED", "--from", help="Start state filter"),
    to: str = typer.Option("BUILT", "--to", help="Target state"),
    limit: int = typer.Option(100, "--limit", help="Max items to process"),
):
    """Run a batch of items from a starting state to target state."""
    processed = 0
    for sp in sorted(STATE_DIR.glob("*.json")):
        state = json.loads(sp.read_text())
        if state.get("status") != from_state:
            continue
        slug = state["slug"]
        typer.echo(f"Processing {slug}…")
        run.callback(slug=slug, to=to, open_diff=False)  # type: ignore
        processed += 1
        if processed >= limit:
            break
    rprint(f"Batch processed: {processed}")


APP.add_typer(batch_app, name="batch")

index_app = typer.Typer(help="Index jobs")


@index_app.command("build")
def index_build():
    idx = []
    for sp in sorted(STATE_DIR.glob("*.json")):
        state = json.loads(sp.read_text())
        slug = state.get("slug")
        content_file = CONTENT_DIR / slug / "content.json"
        if content_file.exists():
            doc = json.loads(content_file.read_text())
            idx.append({
                "slug": slug,
                "title": doc.get("title"),
                "summary": doc.get("summary"),
                "tags": doc.get("tags", []),
                "excerpt": (doc.get("summary") or "")[:200],
            })
    (JOBS_DIR / "search-index.json").write_text(json.dumps(idx, indent=2))
    rprint(f"Search index written: {JOBS_DIR / 'search-index.json'}")


APP.add_typer(index_app, name="index")

redirects_app = typer.Typer(help="Redirect jobs")


@redirects_app.command("build")
def redirects_build(
    legacy_map: Optional[Path] = typer.Option(None, "--legacy-map", help="CSV map of legacy_url,new_slug"),
):
    out = JOBS_DIR / "redirects.csv"
    if legacy_map and legacy_map.exists():
        out.write_bytes(legacy_map.read_bytes())
    else:
        out.write_text("legacy_url,new_slug\n")
    rprint(f"Redirects written: {out}")


APP.add_typer(redirects_app, name="redirects")

links_app = typer.Typer(help="Link checker")


@links_app.command("check")
def links_check(
    concurrency: int = typer.Option(8, "--concurrency"),
    timeout: int = typer.Option(8000, "--timeout"),
):
    report = {
        "started": _now_iso(),
        "concurrency": concurrency,
        "timeout_ms": timeout,
        "results": [],
    }
    out = JOBS_DIR / "reports" / f"links-{datetime.utcnow():%Y%m%d}.json"
    out.write_text(json.dumps(report, indent=2))
    rprint(f"Link report stub written: {out}")


APP.add_typer(links_app, name="links")


@APP.command()
def report(
    since: Optional[str] = typer.Option(None, "--since", help="e.g., 7d"),
    by_state: bool = typer.Option(False, "--by-state"),
):
    """Basic reporting over state files."""
    rows = []
    for sp in sorted(STATE_DIR.glob("*.json")):
        state = json.loads(sp.read_text())
        rows.append((state.get("slug"), state.get("status")))

    if by_state:
        tally: dict[str, int] = {}
        for _, st in rows:
            tally[st] = tally.get(st, 0) + 1
        table = Table(title="By State")
        table.add_column("State")
        table.add_column("Count", justify="right")
        for st, ct in sorted(tally.items()):
            table.add_row(st, str(ct))
        rprint(table)
    else:
        table = Table(title="Items")
        table.add_column("Slug")
        table.add_column("State")
        for slug, st in rows:
            table.add_row(slug, st)
        rprint(table)


if __name__ == "__main__":
    APP()
