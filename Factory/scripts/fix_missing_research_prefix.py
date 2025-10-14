#!/usr/bin/env python3
"""
Fix missing /research/ prefixes in internal links within research content.

This script:
1. Finds all content files of type 'research'
2. Scans their narrative_md for internal links that are missing /research/ prefix
3. Adds the /research/ prefix to make them work correctly
4. Updates the content files with corrected links
"""

import json
import re
from pathlib import Path
from typing import List, Dict, Set

BASE_DIR = Path(__file__).resolve().parents[1]
CONTENT_DIR = BASE_DIR / "content"

def get_research_slugs() -> Set[str]:
    """Get all existing research content slugs."""
    slugs = set()
    for content_file in CONTENT_DIR.rglob("content.json"):
        try:
            with open(content_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if data.get('type') == 'research' and data.get('slug'):
                    slugs.add(data['slug'])
        except Exception:
            pass
    return slugs

def fix_links_in_file(content_file: Path, research_slugs: Set[str]) -> int:
    """Fix missing /research/ prefixes in internal links in a single content.json file."""
    fixed_count = 0
    try:
        with open(content_file, 'r', encoding='utf-8') as f:
            content_data = json.load(f)
        
        if content_data.get('type') != 'research' or 'narrative_md' not in content_data or not content_data['narrative_md']:
            return 0

        original_narrative_md = content_data['narrative_md']
        modified_narrative_md = original_narrative_md

        # Find all internal links that are missing /research/ prefix
        # Pattern for Markdown links: [text](/slug) where slug is a known research slug
        def replace_markdown_link(match):
            link_text = match.group(1)
            slug = match.group(2)
            if slug in research_slugs:
                return f"[{link_text}](/research/{slug})"
            return match.group(0)  # Return original if not a research slug

        # Pattern for HTML links: <a href="/slug"> where slug is a known research slug
        def replace_html_link(match):
            slug = match.group(1)
            if slug in research_slugs:
                return f'<a href="/research/{slug}"'
            return match.group(0)  # Return original if not a research slug

        # Apply replacements
        modified_narrative_md = re.sub(
            r'\[([^\]]+)\]\(/([^/\)]+)\)',
            replace_markdown_link,
            modified_narrative_md
        )

        modified_narrative_md = re.sub(
            r'<a href="/([^"/]+)"',
            replace_html_link,
            modified_narrative_md
        )
        
        if modified_narrative_md != original_narrative_md:
            content_data['narrative_md'] = modified_narrative_md
            with open(content_file, 'w', encoding='utf-8') as f:
                json.dump(content_data, f, ensure_ascii=False, indent=2)
            fixed_count = 1  # Count as one file updated
            print(f"✅ Updated: {content_file.parent.name}")
    except Exception as e:
        print(f"❌ Error fixing links in {content_file}: {e}")
    return fixed_count

def main():
    print("🔧 Fixing missing /research/ prefixes in internal links...")
    research_slugs = get_research_slugs()
    print(f"📋 Found {len(research_slugs)} research content slugs")

    total_files_updated = 0
    
    for content_file in CONTENT_DIR.rglob("content.json"):
        total_files_updated += fix_links_in_file(content_file, research_slugs)
        
    print(f"\n🎉 Fixed missing /research/ prefixes in {total_files_updated} research content files")
    print("   All internal research links now have the correct /research/ prefix")

if __name__ == "__main__":
    main()
