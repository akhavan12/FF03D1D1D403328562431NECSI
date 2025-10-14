#!/usr/bin/env python3
"""
Generate download URLs for missing PDF files from necsi.edu.

This script:
1. Reads the list of missing PDFs from the previous analysis
2. Generates proper necsi.edu URLs for each PDF
3. Creates a comprehensive download list with multiple URL formats
4. Generates a browser-friendly script to open all URLs
"""

import json
import re
from pathlib import Path
from typing import List, Dict, Set

BASE_DIR = Path(__file__).resolve().parents[1]
MISSING_PDFS_SIMPLE = BASE_DIR / "jobs" / "reports" / "missing-pdfs-simple.txt"
PDF_DOWNLOAD_URLS = BASE_DIR / "jobs" / "reports" / "necsi-pdf-download-urls.txt"
PDF_BROWSER_SCRIPT = BASE_DIR / "scripts" / "open_pdf_urls.py"

def generate_pdf_urls():
    """Generate download URLs for all missing PDFs."""
    print("🔗 Generating necsi.edu download URLs for missing PDFs...")
    
    if not MISSING_PDFS_SIMPLE.exists():
        print(f"❌ Missing PDFs list not found: {MISSING_PDFS_SIMPLE}")
        print("   Please run find_missing_pdfs.py first.")
        return
    
    # Read the list of missing PDFs
    with open(MISSING_PDFS_SIMPLE, 'r', encoding='utf-8') as f:
        missing_pdfs = [line.strip() for line in f if line.strip() and not line.startswith('#')]
    
    print(f"📋 Found {len(missing_pdfs)} missing PDF files")
    
    # Generate URLs in multiple formats
    urls = []
    browser_urls = []
    
    for pdf_filename in missing_pdfs:
        # Format 1: Direct /s/ path (most common)
        direct_url = f"https://necsi.edu/s/{pdf_filename}"
        
        # Format 2: Try without /s/ prefix (some PDFs might be in root)
        root_url = f"https://necsi.edu/{pdf_filename}"
        
        # Format 3: Try with /assets/ prefix
        assets_url = f"https://necsi.edu/assets/{pdf_filename}"
        
        urls.extend([direct_url, root_url, assets_url])
        browser_urls.append(direct_url)  # Use the most likely format for browser script
    
    # Write comprehensive URL list
    with open(PDF_DOWNLOAD_URLS, 'w', encoding='utf-8') as f:
        f.write("# PDF Download URLs from necsi.edu\n")
        f.write("# Try these URLs in order - the first one that works is the correct format\n")
        f.write("# Format: https://necsi.edu/s/filename.pdf (most common)\n")
        f.write("# Format: https://necsi.edu/filename.pdf (some in root)\n")
        f.write("# Format: https://necsi.edu/assets/filename.pdf (some in assets)\n\n")
        
        for i, pdf_filename in enumerate(missing_pdfs):
            f.write(f"# {i+1:3d}. {pdf_filename}\n")
            f.write(f"https://necsi.edu/s/{pdf_filename}\n")
            f.write(f"https://necsi.edu/{pdf_filename}\n")
            f.write(f"https://necsi.edu/assets/{pdf_filename}\n")
            f.write("\n")
    
    # Create browser script
    with open(PDF_BROWSER_SCRIPT, 'w', encoding='utf-8') as f:
        f.write('#!/usr/bin/env python3\n')
        f.write('"""\n')
        f.write('Open PDF download URLs in your browser.\n')
        f.write('This script will open each PDF URL so you can download them manually.\n')
        f.write('"""\n\n')
        f.write('import webbrowser\n')
        f.write('import time\n')
        f.write('from pathlib import Path\n\n')
        f.write('BASE_DIR = Path(__file__).resolve().parents[1]\n')
        f.write('PDF_DOWNLOAD_URLS = BASE_DIR / "jobs" / "reports" / "necsi-pdf-download-urls.txt"\n\n')
        f.write('def open_pdf_urls():\n')
        f.write('    """Open PDF URLs in browser for manual download."""\n')
        f.write('    if not PDF_DOWNLOAD_URLS.exists():\n')
        f.write('        print(f"❌ PDF URLs file not found: {PDF_DOWNLOAD_URLS}")\n')
        f.write('        return\n\n')
        f.write('    # Read URLs (only the first URL for each PDF)\n')
        f.write('    urls = []\n')
        f.write('    with open(PDF_DOWNLOAD_URLS, \'r\', encoding=\'utf-8\') as f:\n')
        f.write('        for line in f:\n')
        f.write('            line = line.strip()\n')
        f.write('            if line.startswith(\'https://necsi.edu/s/\'):\n')
        f.write('                urls.append(line)\n\n')
        f.write('    print(f"🚀 Opening {len(urls)} PDF URLs in your browser...")\n')
        f.write('    print("Please download each PDF and save it to Factory/incoming/pdfs/")\n')
        f.write('    print("Press Enter to open the next URL, or \'q\' to quit.\\n")\n\n')
        f.write('    for i, url in enumerate(urls):\n')
        f.write('        print(f"Opening {i+1}/{len(urls)}: {url}")\n')
        f.write('        webbrowser.open(url)\n')
        f.write('        response = input("Press Enter for next URL, or \'q\' to quit: ")\n')
        f.write('        if response.lower() == \'q\':\n')
        f.write('            break\n')
        f.write('        time.sleep(1)  # Small delay\n\n')
        f.write('    print("\\nFinished opening URLs.")\n')
        f.write('    print("Remember to move all downloaded PDFs to Factory/incoming/pdfs/")\n')
        f.write('    print("Then run: python scripts/organize_downloaded_pdfs.py")\n\n')
        f.write('if __name__ == "__main__":\n')
        f.write('    open_pdf_urls()\n')
    
    # Make the browser script executable
    PDF_BROWSER_SCRIPT.chmod(0o755)
    
    print(f"\n💾 Generated files:")
    print(f"   📄 PDF URLs: {PDF_DOWNLOAD_URLS}")
    print(f"   🚀 Browser script: {PDF_BROWSER_SCRIPT}")
    
    print(f"\n🎯 Usage options:")
    print(f"   1. Manual download:")
    print(f"      • Open: {PDF_DOWNLOAD_URLS}")
    print(f"      • Copy URLs and download PDFs manually")
    print(f"      • Save to: Factory/incoming/pdfs/")
    
    print(f"\n   2. Browser-assisted download:")
    print(f"      • Run: python {PDF_BROWSER_SCRIPT}")
    print(f"      • Script will open each URL in your browser")
    print(f"      • Download each PDF manually")
    print(f"      • Save to: Factory/incoming/pdfs/")
    
    print(f"\n   3. After downloading:")
    print(f"      • Run: python scripts/organize_downloaded_pdfs.py")
    print(f"      • This will copy PDFs to the correct assets directory")
    
    print(f"\n📊 Summary:")
    print(f"   • {len(missing_pdfs)} PDF files to download")
    print(f"   • {len(urls)} total URLs generated (3 formats per PDF)")
    print(f"   • Most likely format: https://necsi.edu/s/filename.pdf")

if __name__ == "__main__":
    generate_pdf_urls()
