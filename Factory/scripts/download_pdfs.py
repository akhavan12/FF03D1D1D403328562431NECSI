#!/usr/bin/env python3
"""
Download missing PDF files from necsi.edu.

This script:
1. Reads the list of PDF download URLs
2. Downloads each PDF to the incoming/pdfs directory
3. Reports on success/failure
"""

import requests
import time
from pathlib import Path
from typing import List

BASE_DIR = Path(__file__).resolve().parents[1]
INCOMING_PDFS_DIR = BASE_DIR / "incoming" / "pdfs"
DOWNLOAD_URLS_FILE = BASE_DIR / "jobs" / "reports" / "pdf-download-urls.txt"

def download_pdfs():
    """Download all missing PDF files."""
    print("🔄 Downloading missing PDF files...")
    
    # Ensure directory exists
    INCOMING_PDFS_DIR.mkdir(parents=True, exist_ok=True)
    
    # Read download URLs
    if not DOWNLOAD_URLS_FILE.exists():
        print(f"❌ Download URLs file not found: {DOWNLOAD_URLS_FILE}")
        print("   Please run find_missing_pdfs.py first.")
        return
    
    with open(DOWNLOAD_URLS_FILE, 'r', encoding='utf-8') as f:
        urls = [line.strip() for line in f if line.strip() and not line.startswith('#')]
    
    print(f"📋 Found {len(urls)} PDF URLs to download")
    
    downloaded = 0
    failed = 0
    skipped = 0
    
    for i, url in enumerate(urls):
        # Extract filename from URL
        filename = url.split('/')[-1]
        file_path = INCOMING_PDFS_DIR / filename
        
        # Skip if already exists
        if file_path.exists():
            print(f"⏭️  Skipping {filename} (already exists)")
            skipped += 1
            continue
        
        print(f"📥 Downloading {i+1}/{len(urls)}: {filename}")
        
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            
            # Save the file
            with open(file_path, 'wb') as f:
                f.write(response.content)
            
            print(f"✅ Downloaded: {filename}")
            downloaded += 1
            
            # Small delay to be respectful to the server
            time.sleep(0.5)
            
        except Exception as e:
            print(f"❌ Failed to download {filename}: {e}")
            failed += 1
    
    print(f"\n📊 DOWNLOAD RESULTS")
    print("=" * 50)
    print(f"✅ Downloaded: {downloaded}")
    print(f"⏭️  Skipped: {skipped}")
    print(f"❌ Failed: {failed}")
    print(f"📈 Success rate: {downloaded/(downloaded+failed)*100:.1f}%" if (downloaded+failed) > 0 else "📈 No downloads attempted")
    
    if downloaded > 0:
        print(f"\n🎉 Successfully downloaded {downloaded} PDF files!")
        print(f"   Files saved to: {INCOMING_PDFS_DIR}")
        print(f"   Next step: Run organize_downloaded_pdfs.py to organize them")

if __name__ == "__main__":
    download_pdfs()
