#!/usr/bin/env python3
"""
Open PDF download URLs in your browser.
This script will open each PDF URL so you can download them manually.
"""

import webbrowser
import time
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
PDF_DOWNLOAD_URLS = BASE_DIR / "jobs" / "reports" / "necsi-pdf-download-urls.txt"

def open_pdf_urls():
    """Open PDF URLs in browser for manual download."""
    if not PDF_DOWNLOAD_URLS.exists():
        print(f"❌ PDF URLs file not found: {PDF_DOWNLOAD_URLS}")
        return

    # Read URLs (only the first URL for each PDF)
    urls = []
    with open(PDF_DOWNLOAD_URLS, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line.startswith('https://necsi.edu/s/'):
                urls.append(line)

    print(f"🚀 Opening {len(urls)} PDF URLs in your browser...")
    print("Please download each PDF and save it to Factory/incoming/pdfs/")
    print("Press Enter to open the next URL, or 'q' to quit.\n")

    for i, url in enumerate(urls):
        print(f"Opening {i+1}/{len(urls)}: {url}")
        webbrowser.open(url)
        response = input("Press Enter for next URL, or 'q' to quit: ")
        if response.lower() == 'q':
            break
        time.sleep(1)  # Small delay

    print("\nFinished opening URLs.")
    print("Remember to move all downloaded PDFs to Factory/incoming/pdfs/")
    print("Then run: python scripts/organize_downloaded_pdfs.py")

if __name__ == "__main__":
    open_pdf_urls()
