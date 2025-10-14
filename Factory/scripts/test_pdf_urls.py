#!/usr/bin/env python3
"""
Test PDF URLs to find the correct format.

This script:
1. Tests a few sample PDF URLs in different formats
2. Determines which URL format works for necsi.edu
3. Reports the working format for bulk downloading
"""

import requests
from pathlib import Path
from typing import List, Tuple

BASE_DIR = Path(__file__).resolve().parents[1]
MISSING_PDFS_SIMPLE = BASE_DIR / "jobs" / "reports" / "missing-pdfs-simple.txt"

def test_pdf_urls():
    """Test different URL formats to find the working one."""
    print("🧪 Testing PDF URL formats on necsi.edu...")
    
    if not MISSING_PDFS_SIMPLE.exists():
        print(f"❌ Missing PDFs list not found: {MISSING_PDFS_SIMPLE}")
        return
    
    # Read a few sample PDFs
    with open(MISSING_PDFS_SIMPLE, 'r', encoding='utf-8') as f:
        all_pdfs = [line.strip() for line in f if line.strip() and not line.startswith('#')]
    
    # Test with first 5 PDFs
    test_pdfs = all_pdfs[:5]
    print(f"📋 Testing {len(test_pdfs)} sample PDFs...")
    
    url_formats = [
        ("/s/", "https://necsi.edu/s/{}"),
        ("/assets/", "https://necsi.edu/assets/{}"),
        ("/", "https://necsi.edu/{}"),
    ]
    
    working_formats = []
    
    for pdf_filename in test_pdfs:
        print(f"\n🔍 Testing: {pdf_filename}")
        
        for format_name, url_template in url_formats:
            url = url_template.format(pdf_filename)
            
            try:
                response = requests.head(url, timeout=10, allow_redirects=True)
                status = response.status_code
                
                if status == 200:
                    print(f"   ✅ {format_name}: {status} - WORKING!")
                    working_formats.append((format_name, url_template))
                    break
                elif status == 404:
                    print(f"   ❌ {format_name}: {status} - Not found")
                else:
                    print(f"   ⚠️  {format_name}: {status} - Unexpected")
                    
            except Exception as e:
                print(f"   ❌ {format_name}: Error - {e}")
    
    # Analyze results
    if working_formats:
        print(f"\n🎉 FOUND WORKING FORMAT(S):")
        for format_name, url_template in working_formats:
            print(f"   ✅ {format_name}: {url_template}")
        
        # Use the first working format
        best_format = working_formats[0]
        print(f"\n🚀 RECOMMENDED FORMAT: {best_format[0]}")
        print(f"   URL template: {best_format[1]}")
        
        # Generate corrected download script
        generate_corrected_download_script(best_format[1], all_pdfs)
        
    else:
        print(f"\n❌ NO WORKING FORMATS FOUND")
        print(f"   The PDFs might be:")
        print(f"   • Behind authentication")
        print(f"   • Moved to a different location")
        print(f"   • No longer available")
        print(f"   • Require different URL structure")

def generate_corrected_download_script(url_template: str, all_pdfs: List[str]):
    """Generate a corrected download script with the working URL format."""
    script_path = BASE_DIR / "scripts" / "download_pdfs_corrected.py"
    
    with open(script_path, 'w', encoding='utf-8') as f:
        f.write('#!/usr/bin/env python3\n')
        f.write('"""\n')
        f.write('Download PDFs using the correct URL format.\n')
        f.write('This script uses the tested working URL format.\n')
        f.write('"""\n\n')
        f.write('import requests\n')
        f.write('import time\n')
        f.write('from pathlib import Path\n\n')
        f.write('BASE_DIR = Path(__file__).resolve().parents[1]\n')
        f.write('INCOMING_PDFS_DIR = BASE_DIR / "incoming" / "pdfs"\n')
        f.write('MISSING_PDFS_SIMPLE = BASE_DIR / "jobs" / "reports" / "missing-pdfs-simple.txt"\n\n')
        f.write('def download_pdfs():\n')
        f.write('    """Download PDFs using the correct URL format."""\n')
        f.write('    print("📥 Downloading PDFs using tested URL format...")\n\n')
        f.write('    # Ensure directory exists\n')
        f.write('    INCOMING_PDFS_DIR.mkdir(parents=True, exist_ok=True)\n\n')
        f.write('    # Read PDF list\n')
        f.write('    with open(MISSING_PDFS_SIMPLE, \'r\', encoding=\'utf-8\') as f:\n')
        f.write('        pdfs = [line.strip() for line in f if line.strip() and not line.startswith(\'#\')]\n\n')
        f.write('    print(f"📋 Found {len(pdfs)} PDFs to download")\n\n')
        f.write('    downloaded = 0\n')
        f.write('    failed = 0\n')
        f.write('    skipped = 0\n\n')
        f.write('    for i, pdf_filename in enumerate(pdfs):\n')
        f.write('        file_path = INCOMING_PDFS_DIR / pdf_filename\n\n')
        f.write('        # Skip if already exists\n')
        f.write('        if file_path.exists():\n')
        f.write('            print(f"⏭️  Skipping {pdf_filename} (already exists)")\n')
        f.write('            skipped += 1\n')
        f.write('            continue\n\n')
        f.write('        # Use the tested working URL format\n')
        f.write(f'        url = "{url_template}".format(pdf_filename)\n')
        f.write('        print(f"📥 Downloading {i+1}/{len(pdfs)}: {pdf_filename}")\n\n')
        f.write('        try:\n')
        f.write('            response = requests.get(url, timeout=30)\n')
        f.write('            response.raise_for_status()\n\n')
        f.write('            # Save the file\n')
        f.write('            with open(file_path, \'wb\') as f:\n')
        f.write('                f.write(response.content)\n\n')
        f.write('            print(f"✅ Downloaded: {pdf_filename}")\n')
        f.write('            downloaded += 1\n\n')
        f.write('            # Small delay to be respectful\n')
        f.write('            time.sleep(0.5)\n\n')
        f.write('        except Exception as e:\n')
        f.write('            print(f"❌ Failed to download {pdf_filename}: {e}")\n')
        f.write('            failed += 1\n\n')
        f.write('    print(f"\\n📊 RESULTS:")\n')
        f.write('    print(f"✅ Downloaded: {downloaded}")\n')
        f.write('    print(f"⏭️  Skipped: {skipped}")\n')
        f.write('    print(f"❌ Failed: {failed}")\n\n')
        f.write('    if downloaded > 0:\n')
        f.write('        print(f"\\n🎉 Successfully downloaded {downloaded} PDFs!")\n')
        f.write('        print("Next: Run python scripts/organize_downloaded_pdfs.py")\n\n')
        f.write('if __name__ == "__main__":\n')
        f.write('    download_pdfs()\n')
    
    print(f"\n💾 Generated corrected download script: {script_path}")
    print(f"   Run: python {script_path}")

if __name__ == "__main__":
    test_pdf_urls()
