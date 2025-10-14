#!/usr/bin/env python3
"""
Download PDFs using the correct URL format.
This script uses the tested working URL format.
"""

import requests
import time
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
INCOMING_PDFS_DIR = BASE_DIR / "incoming" / "pdfs"
MISSING_PDFS_SIMPLE = BASE_DIR / "jobs" / "reports" / "missing-pdfs-simple.txt"

def download_pdfs():
    """Download PDFs using the correct URL format."""
    print("📥 Downloading PDFs using tested URL format...")

    # Ensure directory exists
    INCOMING_PDFS_DIR.mkdir(parents=True, exist_ok=True)

    # Read PDF list
    with open(MISSING_PDFS_SIMPLE, 'r', encoding='utf-8') as f:
        pdfs = [line.strip() for line in f if line.strip() and not line.startswith('#')]

    print(f"📋 Found {len(pdfs)} PDFs to download")

    downloaded = 0
    failed = 0
    skipped = 0

    for i, pdf_filename in enumerate(pdfs):
        file_path = INCOMING_PDFS_DIR / pdf_filename

        # Skip if already exists
        if file_path.exists():
            print(f"⏭️  Skipping {pdf_filename} (already exists)")
            skipped += 1
            continue

        # Use the tested working URL format
        url = "https://necsi.edu/s/{}".format(pdf_filename)
        print(f"📥 Downloading {i+1}/{len(pdfs)}: {pdf_filename}")

        try:
            response = requests.get(url, timeout=30, allow_redirects=True)
            response.raise_for_status()

            # Save the file
            with open(file_path, 'wb') as f:
                f.write(response.content)

            print(f"✅ Downloaded: {pdf_filename}")
            downloaded += 1

            # Small delay to be respectful
            time.sleep(0.5)

        except Exception as e:
            print(f"❌ Failed to download {pdf_filename}: {e}")
            failed += 1

    print(f"\n📊 RESULTS:")
    print(f"✅ Downloaded: {downloaded}")
    print(f"⏭️  Skipped: {skipped}")
    print(f"❌ Failed: {failed}")

    if downloaded > 0:
        print(f"\n🎉 Successfully downloaded {downloaded} PDFs!")
        print("Next: Run python scripts/organize_downloaded_pdfs.py")

if __name__ == "__main__":
    download_pdfs()
