#!/usr/bin/env python3
"""
Download a sample of PDFs to test the process.

This script downloads the first 10 PDFs to test the download and organization process.
"""

import requests
import time
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
INCOMING_PDFS_DIR = BASE_DIR / "incoming" / "pdfs"
S_DIR = BASE_DIR.parents[0] / "sites" / "necsi-site" / "public" / "s"
MISSING_PDFS_SIMPLE = BASE_DIR / "jobs" / "reports" / "missing-pdfs-simple.txt"

def download_sample_pdfs():
    """Download first 10 PDFs as a test."""
    print("🧪 Downloading sample PDFs to test the process...")
    
    # Ensure directories exist
    INCOMING_PDFS_DIR.mkdir(parents=True, exist_ok=True)
    S_DIR.mkdir(parents=True, exist_ok=True)
    
    # Read PDF list
    with open(MISSING_PDFS_SIMPLE, 'r', encoding='utf-8') as f:
        all_pdfs = [line.strip() for line in f if line.strip() and not line.startswith('#')]
    
    # Take first 10 PDFs
    sample_pdfs = all_pdfs[:10]
    print(f"📋 Downloading {len(sample_pdfs)} sample PDFs...")
    
    downloaded = 0
    failed = 0
    
    for i, pdf_filename in enumerate(sample_pdfs):
        print(f"\n📥 Downloading {i+1}/{len(sample_pdfs)}: {pdf_filename}")
        
        # Download URL
        url = f"https://necsi.edu/s/{pdf_filename}"
        
        try:
            response = requests.get(url, timeout=30, allow_redirects=True)
            response.raise_for_status()
            
            # Save to incoming directory
            incoming_file = INCOMING_PDFS_DIR / pdf_filename
            with open(incoming_file, 'wb') as f:
                f.write(response.content)
            
            # Also save directly to /s/ directory
            s_file = S_DIR / pdf_filename
            with open(s_file, 'wb') as f:
                f.write(response.content)
            
            print(f"✅ Downloaded: {pdf_filename} ({len(response.content)} bytes)")
            downloaded += 1
            
            # Small delay
            time.sleep(0.5)
            
        except Exception as e:
            print(f"❌ Failed: {pdf_filename} - {e}")
            failed += 1
    
    print(f"\n📊 SAMPLE DOWNLOAD RESULTS")
    print("=" * 50)
    print(f"✅ Downloaded: {downloaded}")
    print(f"❌ Failed: {failed}")
    print(f"📈 Success rate: {downloaded/(downloaded+failed)*100:.1f}%" if (downloaded+failed) > 0 else "No downloads attempted")
    
    if downloaded > 0:
        print(f"\n🎉 Successfully downloaded {downloaded} sample PDFs!")
        print(f"   📁 PDFs saved to: {S_DIR}")
        print(f"   🔗 PDF links should now work at: http://localhost:4321/s/filename.pdf")
        
        # Test a few links
        print(f"\n🧪 Testing PDF links:")
        for pdf_filename in sample_pdfs[:3]:
            if (S_DIR / pdf_filename).exists():
                print(f"   ✅ /s/{pdf_filename} - Available")
            else:
                print(f"   ❌ /s/{pdf_filename} - Missing")

if __name__ == "__main__":
    download_sample_pdfs()
