#!/usr/bin/env python3
"""
Download all missing PDF files from necsi.edu.

This script:
1. Downloads all 342 missing PDFs
2. Saves them directly to the /s/ directory
3. Includes progress reporting and error handling
4. Continues even if some downloads fail
"""

import requests
import time
from pathlib import Path
from typing import List

BASE_DIR = Path(__file__).resolve().parents[1]
INCOMING_PDFS_DIR = BASE_DIR / "incoming" / "pdfs"
S_DIR = BASE_DIR.parents[0] / "sites" / "necsi-site" / "public" / "s"
MISSING_PDFS_SIMPLE = BASE_DIR / "jobs" / "reports" / "missing-pdfs-simple.txt"

def download_all_pdfs():
    """Download all missing PDF files."""
    print("📥 Starting comprehensive PDF download...")
    
    # Ensure directories exist
    INCOMING_PDFS_DIR.mkdir(parents=True, exist_ok=True)
    S_DIR.mkdir(parents=True, exist_ok=True)
    
    # Read PDF list
    with open(MISSING_PDFS_SIMPLE, 'r', encoding='utf-8') as f:
        all_pdfs = [line.strip() for line in f if line.strip() and not line.startswith('#')]
    
    print(f"📋 Found {len(all_pdfs)} PDFs to download")
    
    downloaded = 0
    failed = 0
    skipped = 0
    
    for i, pdf_filename in enumerate(all_pdfs):
        # Check if already exists
        s_file = S_DIR / pdf_filename
        if s_file.exists():
            print(f"⏭️  Skipping {pdf_filename} (already exists)")
            skipped += 1
            continue
        
        print(f"📥 Downloading {i+1}/{len(all_pdfs)}: {pdf_filename}")
        
        # Download URL
        url = f"https://necsi.edu/s/{pdf_filename}"
        
        try:
            response = requests.get(url, timeout=30, allow_redirects=True)
            response.raise_for_status()
            
            # Save to both locations
            incoming_file = INCOMING_PDFS_DIR / pdf_filename
            with open(incoming_file, 'wb') as f:
                f.write(response.content)
            
            with open(s_file, 'wb') as f:
                f.write(response.content)
            
            print(f"✅ Downloaded: {pdf_filename} ({len(response.content)} bytes)")
            downloaded += 1
            
            # Progress update every 10 downloads
            if downloaded % 10 == 0:
                print(f"📊 Progress: {downloaded}/{len(all_pdfs)} downloaded ({downloaded/len(all_pdfs)*100:.1f}%)")
            
            # Small delay to be respectful
            time.sleep(0.3)
            
        except Exception as e:
            print(f"❌ Failed: {pdf_filename} - {e}")
            failed += 1
            
            # If too many failures, pause
            if failed > 10 and failed % 10 == 0:
                print(f"⚠️  {failed} failures so far. Pausing for 5 seconds...")
                time.sleep(5)
    
    print(f"\n🎉 DOWNLOAD COMPLETE!")
    print("=" * 50)
    print(f"✅ Downloaded: {downloaded}")
    print(f"⏭️  Skipped: {skipped}")
    print(f"❌ Failed: {failed}")
    print(f"📈 Success rate: {downloaded/(downloaded+failed)*100:.1f}%" if (downloaded+failed) > 0 else "No downloads attempted")
    
    if downloaded > 0:
        print(f"\n🎉 Successfully downloaded {downloaded} PDF files!")
        print(f"   📁 PDFs available at: {S_DIR}")
        print(f"   🔗 PDF links now work at: http://localhost:4321/s/filename.pdf")
        print(f"   📊 This fixes {downloaded} broken PDF links in your research pages!")

if __name__ == "__main__":
    download_all_pdfs()
