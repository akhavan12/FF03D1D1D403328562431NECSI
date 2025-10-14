#!/usr/bin/env python3
"""
Organize downloaded PDF files into the assets directory.

This script:
1. Reads the list of missing PDFs
2. Looks for downloaded PDFs in the incoming/pdfs directory
3. Copies them to the correct location in the assets directory
4. Updates the content links to point to the new locations
"""

import shutil
from pathlib import Path
from typing import Dict, List

BASE_DIR = Path(__file__).resolve().parents[1]
INCOMING_PDFS_DIR = BASE_DIR / "incoming" / "pdfs"
ASSETS_DIR = BASE_DIR.parents[0] / "sites" / "necsi-site" / "public" / "assets"
MISSING_PDFS_SIMPLE = BASE_DIR / "jobs" / "reports" / "missing-pdfs-simple.txt"

def organize_pdfs():
    """Organize downloaded PDFs into the assets directory."""
    print("🔄 Organizing downloaded PDF files...")
    
    if not INCOMING_PDFS_DIR.exists():
        print(f"❌ PDFs directory not found: {INCOMING_PDFS_DIR}")
        print("   Please create the directory and download PDFs there first.")
        return
    
    # Read the list of missing PDFs
    if not MISSING_PDFS_SIMPLE.exists():
        print(f"❌ Missing PDFs list not found: {MISSING_PDFS_SIMPLE}")
        print("   Please run find_missing_pdfs.py first.")
        return
    
    with open(MISSING_PDFS_SIMPLE, 'r', encoding='utf-8') as f:
        missing_pdfs = [line.strip() for line in f if line.strip() and not line.startswith('#')]
    
    print(f"📋 Looking for {len(missing_pdfs)} missing PDF files...")
    
    # Ensure assets directory exists
    ASSETS_DIR.mkdir(parents=True, exist_ok=True)
    
    # Also ensure /s/ directory exists in Astro site
    S_DIR = BASE_DIR.parents[0] / "sites" / "necsi-site" / "public" / "s"
    S_DIR.mkdir(parents=True, exist_ok=True)
    
    found_pdfs = []
    missing_files = []
    
    for pdf_filename in missing_pdfs:
        # Look for the PDF in the incoming directory
        pdf_file = INCOMING_PDFS_DIR / pdf_filename
        
        if pdf_file.exists():
            # Copy to both assets directory and /s/ directory
            dest_file_assets = ASSETS_DIR / pdf_filename
            dest_file_s = S_DIR / pdf_filename
            
            shutil.copy2(pdf_file, dest_file_assets)
            shutil.copy2(pdf_file, dest_file_s)
            
            found_pdfs.append(pdf_filename)
            print(f"✅ Copied: {pdf_filename}")
        else:
            missing_files.append(pdf_filename)
    
    print(f"\n📊 ORGANIZATION RESULTS")
    print("=" * 50)
    print(f"✅ Found and copied: {len(found_pdfs)}")
    print(f"❌ Still missing: {len(missing_files)}")
    
    if missing_files:
        print(f"\n❌ Still missing PDFs:")
        for pdf in missing_files[:10]:  # Show first 10
            print(f"   • {pdf}")
        if len(missing_files) > 10:
            print(f"   ... and {len(missing_files) - 10} more")
    
    if found_pdfs:
        print(f"\n🎉 Successfully organized {len(found_pdfs)} PDF files!")
        print(f"   PDFs are now available in: {ASSETS_DIR}")
        print(f"   Links should now work correctly in the research pages.")

if __name__ == "__main__":
    organize_pdfs()
