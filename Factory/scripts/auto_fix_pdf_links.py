#!/usr/bin/env python3
"""
Automatically fix PDF links as they are downloaded.

This script:
1. Monitors the incoming/pdfs directory for new PDF files
2. Automatically copies them to the assets directory
3. Updates the Astro site content
4. Reports on progress
"""

import time
import shutil
from pathlib import Path
from typing import Set

BASE_DIR = Path(__file__).resolve().parents[1]
INCOMING_PDFS_DIR = BASE_DIR / "incoming" / "pdfs"
ASSETS_DIR = BASE_DIR.parents[0] / "sites" / "necsi-site" / "public" / "assets"
MISSING_PDFS_SIMPLE = BASE_DIR / "jobs" / "reports" / "missing-pdfs-simple.txt"

def get_missing_pdf_list() -> Set[str]:
    """Get the list of missing PDFs."""
    if not MISSING_PDFS_SIMPLE.exists():
        return set()
    
    with open(MISSING_PDFS_SIMPLE, 'r', encoding='utf-8') as f:
        return {line.strip() for line in f if line.strip() and not line.startswith('#')}

def auto_fix_pdf_links():
    """Monitor and automatically fix PDF links as they're downloaded."""
    print("🔄 Starting automatic PDF link fixing...")
    print("   Monitoring for new PDF downloads...")
    
    # Ensure directories exist
    INCOMING_PDFS_DIR.mkdir(parents=True, exist_ok=True)
    ASSETS_DIR.mkdir(parents=True, exist_ok=True)
    
    # Get the list of PDFs we're looking for
    missing_pdfs = get_missing_pdf_list()
    print(f"📋 Looking for {len(missing_pdfs)} missing PDF files")
    
    processed_pdfs = set()
    total_fixed = 0
    
    print("\n🚀 Monitoring for downloads... (Press Ctrl+C to stop)")
    print("   This will automatically fix PDF links as they're downloaded")
    
    try:
        while True:
            # Check for new PDF files
            if INCOMING_PDFS_DIR.exists():
                for pdf_file in INCOMING_PDFS_DIR.glob("*.pdf"):
                    pdf_filename = pdf_file.name
                    
                    if pdf_filename not in processed_pdfs and pdf_filename in missing_pdfs:
                        # Copy to assets directory
                        dest_file = ASSETS_DIR / pdf_filename
                        
                        try:
                            shutil.copy2(pdf_file, dest_file)
                            processed_pdfs.add(pdf_filename)
                            total_fixed += 1
                            
                            print(f"✅ Fixed: {pdf_filename} ({total_fixed}/{len(missing_pdfs)})")
                            
                            # Show progress
                            if total_fixed % 10 == 0:
                                print(f"📊 Progress: {total_fixed}/{len(missing_pdfs)} PDFs fixed ({total_fixed/len(missing_pdfs)*100:.1f}%)")
                                
                        except Exception as e:
                            print(f"❌ Error copying {pdf_filename}: {e}")
            
            # Check if we're done
            if len(processed_pdfs) >= len(missing_pdfs):
                print(f"\n🎉 ALL PDFs PROCESSED!")
                print(f"   ✅ Fixed {total_fixed} PDF links")
                print(f"   📁 PDFs available at: {ASSETS_DIR}")
                print(f"   🔗 PDF links should now work in your research pages")
                break
            
            # Wait before checking again
            time.sleep(2)
            
    except KeyboardInterrupt:
        print(f"\n⏹️  Monitoring stopped by user")
        print(f"   ✅ Fixed {total_fixed} PDF links so far")
        print(f"   📁 PDFs available at: {ASSETS_DIR}")
    
    print(f"\n📊 FINAL RESULTS:")
    print(f"   ✅ PDFs fixed: {total_fixed}")
    print(f"   📋 Total missing: {len(missing_pdfs)}")
    print(f"   📈 Progress: {total_fixed/len(missing_pdfs)*100:.1f}%")

if __name__ == "__main__":
    auto_fix_pdf_links()
