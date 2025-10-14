#!/usr/bin/env python3
"""
Process the missing research pages identified in the analysis
"""

import json
import subprocess
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
CLI_SCRIPT = BASE_DIR / "necsifactory" / "cli.py"

# Missing pages identified from analysis
MISSING_PAGES = [
    "group-selection",
    "biodiversity", 
    "-star-movies-mobile-app-released"
]

def process_missing_page(slug):
    """Process a single missing page"""
    print(f"🔄 Processing missing page: {slug}")
    
    try:
        # Run the CLI command to process the page
        result = subprocess.run([
            sys.executable, str(CLI_SCRIPT), "run", 
            "--slug", slug, 
            "--target-state", "BUILT"
        ], capture_output=True, text=True, cwd=BASE_DIR)
        
        if result.returncode == 0:
            print(f"✅ Successfully processed: {slug}")
            return True
        else:
            print(f"❌ Failed to process {slug}: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error processing {slug}: {e}")
        return False

def main():
    """Process all missing pages"""
    print("🚀 PROCESSING MISSING RESEARCH PAGES")
    print("=" * 50)
    
    success_count = 0
    total_count = len(MISSING_PAGES)
    
    for slug in MISSING_PAGES:
        if process_missing_page(slug):
            success_count += 1
        print()  # Add spacing
    
    print("=" * 50)
    print(f"📊 SUMMARY:")
    print(f"  ✅ Successfully processed: {success_count}/{total_count}")
    print(f"  ❌ Failed: {total_count - success_count}/{total_count}")
    
    if success_count == total_count:
        print("🎉 All missing pages processed successfully!")
    else:
        print("⚠️  Some pages failed to process. Check the logs above.")

if __name__ == "__main__":
    main()
