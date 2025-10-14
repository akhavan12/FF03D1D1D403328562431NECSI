#!/usr/bin/env python3
"""
Bulk-ingest .webarchive files from Factory/incoming/ using original slugs
extracted from the capture HTML (og:url or canonical). Optionally build to
BUILT and sync assets to the site.

Usage examples (run from the Factory directory):
  python scripts/bulk_ingest.py --build
  python scripts/bulk_ingest.py --dry-run
  python scripts/bulk_ingest.py --only overview,ending-pandemics --build

Requirements: run inside Factory's virtualenv so necsifactory.cli is importable.
"""
from __future__ import annotations

import argparse
import json
import os
import plistlib
import re
import shlex
import subprocess
from pathlib import Path
from typing import Iterable, Optional
from urllib.parse import urlparse

BASE_DIR = Path(__file__).resolve().parents[1]
INCOMING_DIR = BASE_DIR / "incoming"
SCRIPTS_DIR = BASE_DIR / "scripts"

META_OG_URL_RE = re.compile(
    rb'<meta\s+[^>]*property=["\']og:url["\'][^>]*content=["\']([^"\']+)["\'][^>]*>',
    re.I,
)
LINK_CANONICAL_RE = re.compile(
    rb'<link\s+[^>]*rel=["\']canonical["\'][^>]*href=["\']([^"\']+)["\'][^>]*>',
    re.I,
)


def _discover_webarchives(selected: Optional[Iterable[str]] = None) -> list[Path]:
    wa = sorted(INCOMING_DIR.glob("*.webarchive"))
    if selected:
        wanted = {s.strip().lower() for s in selected}
        wa = [p for p in wa if any(s in p.stem.lower() for s in wanted)]
    return wa


def _read_main_resource(p: Path) -> tuple[str, bytes]:
    """Return (url, body_bytes) for the WebMainResource inside the webarchive."""
    with p.open("rb") as f:
        data = plistlib.load(f)
    main = data.get("WebMainResource", {}) or {}
    url = main.get("WebResourceURL") or ""
    body = main.get("WebResourceData") or b""
    return url, body


def _derive_slug(url: str) -> str:
    parsed = urlparse(url)
    path = parsed.path or "/"
    slug = path.rstrip("/").split("/")[-1]
    return slug or "overview"


def _slug_from_body(body: bytes) -> Optional[str]:
    m = META_OG_URL_RE.search(body)
    if m:
        return _derive_slug(m.group(1).decode("utf-8", "ignore"))
    m2 = LINK_CANONICAL_RE.search(body)
    if m2:
        return _derive_slug(m2.group(1).decode("utf-8", "ignore"))
    return None


def _detect_slug(p: Path) -> tuple[str, str]:
    """Return (source_url_for_slug, slug). Falls back to main resource URL."""
    url, body = _read_main_resource(p)
    s = _slug_from_body(body) or _derive_slug(url)
    source = (META_OG_URL_RE.search(body) or LINK_CANONICAL_RE.search(body))
    chosen_from = "og:url/canonical" if source else "main_resource"
    return chosen_from + ":" + (url if chosen_from == "main_resource" else (source.group(1).decode("utf-8", "ignore") if source else url)), s


def _run(cmd: list[str], cwd: Path) -> int:
    print("$", " ".join(shlex.quote(c) for c in cmd))
    return subprocess.call(cmd, cwd=str(cwd))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--build", action="store_true", help="Run to BUILT after ingest")
    ap.add_argument(
        "--only",
        help="Comma-separated filters to include (matches part of filename, case-insensitive)",
    )
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--open", action="store_true", help="Open the produced content.json files")
    args = ap.parse_args()

    selected = [s.strip() for s in args.only.split(",")] if args.only else None
    items = _discover_webarchives(selected)
    if not items:
        print("No .webarchive files found in incoming/")
        return 0

    plan: list[dict] = []
    for p in items:
        try:
            chosen_from, slug = _detect_slug(p)
            plan.append({"file": str(p), "slug": slug, "source": chosen_from})
        except Exception as e:
            plan.append({"file": str(p), "slug": None, "error": str(e)})

    print(json.dumps({"plan": plan}, indent=2))

    if args.dry_run:
        return 0

    # Ingest and (optional) build
    for it in plan:
        if not it.get("slug"):
            print("Skipping (no slug):", it["file"]) 
            continue
        slug = it["slug"]
        src = it["file"]
        rc = _run(["python", "-m", "necsifactory.cli", "ingest", "--add", src, "--slug", slug], BASE_DIR)
        if rc != 0:
            print(f"[WARN] ingest failed for {slug}")
            continue
        if args.build:
            rc = _run(["python", "-m", "necsifactory.cli", "run", slug, "--to", "BUILT", "--force", "--replace", "--snapshot"], BASE_DIR)
            if rc != 0:
                print(f"[WARN] build failed for {slug}")
                continue
            if args.open:
                content = BASE_DIR / "content" / slug / "content.json"
                if content.exists():
                    _run(["open", str(content)], BASE_DIR)

    print("Done.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
