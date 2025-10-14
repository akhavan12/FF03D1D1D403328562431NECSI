from __future__ import annotations

import hashlib
import mimetypes
import os
from pathlib import Path
from typing import Dict, Tuple, Optional

import requests
from bs4 import BeautifulSoup


DEFAULT_TIMEOUT = 20
USER_AGENT = "NECSI-Factory/1.0 (+https://necsi.edu)"


def _sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _ext_from_url_or_ct(url: str | None, content_type: str | None) -> str:
    # Try URL extension first
    if url:
        guess, _ = mimetypes.guess_type(url)
        if guess:
            ext = mimetypes.guess_extension(guess) or ""
            if ext:
                return ext
        # fallback to explicit suffix
        suf = Path(url).suffix
        if suf:
            return suf
    # Then from content-type
    if content_type:
        ext = mimetypes.guess_extension(content_type.split(";")[0].strip()) or ""
        if ext:
            return ext
    return ""


def _download(url: str) -> Tuple[bytes, str | None]:
    resp = requests.get(url, timeout=DEFAULT_TIMEOUT, headers={"User-Agent": USER_AGENT})
    resp.raise_for_status()
    return resp.content, resp.headers.get("content-type")


def download_single(url: str, slug: str, assets_root: Path, manifest_path: Path) -> Optional[str]:
    """Download a single asset URL and return public path /assets/<slug>/<file> or None on failure."""
    try:
        data, ct = _download(url)
        digest = _sha256_bytes(data)[:16]
        ext = _ext_from_url_or_ct(url, ct) or ""
        filename = f"{digest}{ext}"
        local_rel = Path(slug) / filename
        local_abs = assets_root / local_rel
        if not local_abs.exists():
            local_abs.parent.mkdir(parents=True, exist_ok=True)
            local_abs.write_bytes(data)
        public_path = f"/assets/{local_rel.as_posix()}"
        # append to manifest
        try:
            import json
            existing = {}
            if manifest_path.exists():
                existing = json.loads(manifest_path.read_text() or "{}") or {}
            existing_assets = existing.get("assets", [])
            existing_assets.append({
                "original_url": url,
                "content_type": ct,
                "sha256": digest,
                "path": public_path,
            })
            existing["assets"] = existing_assets
            manifest_path.parent.mkdir(parents=True, exist_ok=True)
            manifest_path.write_text(json.dumps(existing, indent=2))
        except Exception:
            pass
        return public_path
    except Exception:
        return None


def download_and_rewrite_assets(html: str, slug: str, assets_root: Path, manifest_path: Path) -> Tuple[str, Dict]:
    """Download external <img> and <audio> assets referenced in the given HTML and rewrite to /assets/<slug>/... paths.

    Returns (rewritten_html, manifest_dict)
    """
    assets_root.mkdir(parents=True, exist_ok=True)
    soup = BeautifulSoup(html, "lxml")
    manifest = {"assets": []}

    def handle_tag(tag, attr: str):
        url = tag.get(attr)
        if not url:
            return
        # Only external http(s)
        if not (url.startswith("http://") or url.startswith("https://")):
            return
        try:
            data, ct = _download(url)
            digest = _sha256_bytes(data)[:16]
            ext = _ext_from_url_or_ct(url, ct) or ""
            filename = f"{digest}{ext}"
            local_rel = Path(slug) / filename
            local_abs = assets_root / local_rel
            if not local_abs.exists():
                local_abs.parent.mkdir(parents=True, exist_ok=True)
                local_abs.write_bytes(data)
            public_path = f"/assets/{local_rel.as_posix()}"
            # rewrite attribute
            tag[attr] = public_path
            manifest["assets"].append({
                "original_url": url,
                "content_type": ct,
                "sha256": digest,
                "path": public_path,
            })
        except Exception:
            # On failure, leave as-is
            return

    # Process imgs and audio sources
    for img in soup.find_all("img"):
        handle_tag(img, "src")
    for audio in soup.find_all("audio"):
        handle_tag(audio, "src")
        # Also handle <source> under audio
        for src in audio.find_all("source"):
            handle_tag(src, "src")

    # Also process asset-like anchors (images, audio, pdf)
    exts = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg", ".pdf", ".mp3", ".wav", ".m4a"}
    for a in soup.find_all("a"):
        href = a.get("href")
        if not href:
            continue
        lower = href.lower()
        if any(lower.endswith(e) for e in exts):
            handle_tag(a, "href")

    # Write manifest
    try:
        existing = {}
        if manifest_path.exists():
            import json
            existing = json.loads(manifest_path.read_text() or "{}")
            if not isinstance(existing, dict):
                existing = {}
        # merge simple
        existing_assets = existing.get("assets", [])
        existing_assets.extend(manifest["assets"])  # may contain dups
        existing["assets"] = existing_assets
        manifest_path.parent.mkdir(parents=True, exist_ok=True)
        manifest_path.write_text(__import__("json").dumps(existing, indent=2))
    except Exception:
        pass

    return str(soup), manifest
