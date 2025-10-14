#!/usr/bin/env python3
"""
Fix broken links that have incorrect /research/ prefix.

This script:
1. Finds all content files with broken links that have /research/ prefix
2. Removes the /research/ prefix to make them root-level links
3. Updates the content files with corrected links
"""

import json
import re
from pathlib import Path
from typing import List, Dict, Set

BASE_DIR = Path(__file__).resolve().parents[1]
CONTENT_DIR = BASE_DIR / "content"
REPORT_FILE = BASE_DIR / "jobs" / "reports" / "link-check-report.json"

def get_existing_slugs() -> Set[str]:
    """Get all existing content slugs."""
    slugs = set()
    for content_file in CONTENT_DIR.rglob("content.json"):
        try:
            with open(content_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                slug = data.get('slug')
                if slug:
                    slugs.add(slug)
        except Exception:
            pass
    return slugs

def fix_research_prefix_links():
    """Fix links that have incorrect /research/ prefix."""
    if not REPORT_FILE.exists():
        print(f"❌ Report file not found: {REPORT_FILE}")
        return

    with open(REPORT_FILE, 'r', encoding='utf-8') as f:
        report = json.load(f)

    existing_slugs = get_existing_slugs()
    print(f"✅ Found {len(existing_slugs)} existing content slugs")

    # Track fixes
    fixes_made = 0
    files_updated = 0
    content_files_to_update = {}

    # Find broken links with /research/ prefix that should be root-level
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
            normalized_link = broken_link_info['normalized'].lstrip('/')
            
            # Check if this is a /research/ prefix issue
            if link.startswith('/research/') and not link.startswith('/research/research'):
                # Remove /research/ prefix
                root_link = link.replace('/research/', '/')
                root_slug = root_link.lstrip('/')
                
                # Check if the root-level slug exists
                if root_slug in existing_slugs:
                    print(f"🔧 Fixing: {link} -> {root_link}")
                    
                    # Track this fix
                    if content_file_path not in content_files_to_update:
                        content_files_to_update[content_file_path] = []
                    content_files_to_update[content_file_path].append((link, root_link))
                    fixes_made += 1

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
    print(f"✅ Fixed {fixes_made} broken links")
    print(f"📄 Updated {files_updated} content files")
    print(f"📈 This should reduce broken links by {fixes_made}")

if __name__ == "__main__":
    print("🔧 Fixing broken links with incorrect /research/ prefix...")
    fix_research_prefix_links()
