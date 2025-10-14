#!/usr/bin/env python3
"""
Fix broken asset links that point to /s/ directory.

This script:
1. Finds all broken links that point to /s/ directory (PDFs, images)
2. Checks if the files exist in the content directories
3. Updates the links to point to the correct asset locations
"""

import json
import re
from pathlib import Path
from typing import List, Dict, Set

BASE_DIR = Path(__file__).resolve().parents[1]
CONTENT_DIR = BASE_DIR / "content"
REPORT_FILE = BASE_DIR / "jobs" / "reports" / "link-check-report.json"

def find_asset_files() -> Dict[str, Path]:
    """Find all asset files in the content directories."""
    asset_files = {}
    
    # Look for files in content directories
    for content_dir in CONTENT_DIR.iterdir():
        if content_dir.is_dir():
            # Look for files in the content directory
            for file_path in content_dir.rglob("*"):
                if file_path.is_file() and not file_path.name.endswith('.json'):
                    # Create a mapping from filename to full path
                    filename = file_path.name
                    asset_files[filename] = file_path
    
    return asset_files

def fix_asset_links():
    """Fix broken asset links."""
    if not REPORT_FILE.exists():
        print(f"❌ Report file not found: {REPORT_FILE}")
        return

    with open(REPORT_FILE, 'r', encoding='utf-8') as f:
        report = json.load(f)

    # Find all asset files
    asset_files = find_asset_files()
    print(f"✅ Found {len(asset_files)} asset files in content directories")

    # Track fixes
    fixes_made = 0
    files_updated = 0
    content_files_to_update = {}

    # Find broken links with /s/ prefix
    for page in report.get('broken_links', []):
        page_slug = page['slug']
        content_file_path = None
        
        # Find the content file for this page
        for content_file in CONTENT_DIR.rglob("content.json"):
            try:
                with open(content_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if data.get('slug') == page_slug:
                        content_file_path = content_file
                        break
            except Exception:
                continue
        
        if not content_file_path:
            continue

        # Check each broken link
        for broken_link_info in page.get('broken_links', []):
            link = broken_link_info['link']
            
            # Check if this is an asset link
            if link.startswith('/s/') or link.startswith('/assets/'):
                # Extract filename from the link
                filename = link.split('/')[-1]
                
                # Check if we have this file
                if filename in asset_files:
                    asset_path = asset_files[filename]
                    
                    # Create the correct asset URL
                    # For now, we'll use a relative path from the content directory
                    correct_link = f"/assets/{filename}"
                    
                    print(f"🔧 Fixing asset: {link} -> {correct_link}")
                    print(f"   File found at: {asset_path}")
                    
                    # Track this fix
                    if content_file_path not in content_files_to_update:
                        content_files_to_update[content_file_path] = []
                    content_files_to_update[content_file_path].append((link, correct_link))
                    fixes_made += 1
                else:
                    print(f"⚠️  Asset not found: {filename}")

    # Apply fixes to content files
    for content_file_path, link_fixes in content_files_to_update.items():
        try:
            with open(content_file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Apply each fix
            for old_link, new_link in link_fixes:
                content = content.replace(old_link, new_link)
            
            # Write back the updated content
            with open(content_file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            files_updated += 1
            print(f"✅ Updated: {content_file_path.name} ({len(link_fixes)} fixes)")
            
        except Exception as e:
            print(f"❌ Error updating {content_file_path}: {e}")

    print(f"\n🎉 SUMMARY:")
    print(f"✅ Fixed {fixes_made} broken asset links")
    print(f"📄 Updated {files_updated} content files")
    print(f"📈 This should reduce broken links by {fixes_made}")

if __name__ == "__main__":
    print("🔧 Fixing broken asset links...")
    fix_asset_links()
