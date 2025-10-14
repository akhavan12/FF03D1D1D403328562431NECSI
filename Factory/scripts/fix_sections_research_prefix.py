#!/usr/bin/env python3
"""
Fix missing /research/ prefixes in sections URLs within research content.

This script:
1. Finds all content files of type 'research'
2. Scans their sections for URLs that are missing /research/ prefix
3. Adds the /research/ prefix to make them work correctly
4. Updates the content files with corrected URLs
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

def fix_sections_in_file(content_file: Path, research_slugs: Set[str]) -> int:
    """Fix missing /research/ prefixes in sections URLs in a single content.json file."""
    fixed_count = 0
    try:
        with open(content_file, 'r', encoding='utf-8') as f:
            content_data = json.load(f)
        
        if content_data.get('type') != 'research' or 'sections' not in content_data:
            return 0

        original_content = json.dumps(content_data, ensure_ascii=False, indent=2)
        modified_content = original_content

        # Fix sections.introductions URLs
        if 'introductions' in content_data.get('sections', {}):
            for intro in content_data['sections']['introductions']:
                if 'url' in intro:
                    url = intro['url']
                    # Remove leading slash and check if it's a research slug
                    slug = url.lstrip('/')
                    if slug in research_slugs and not url.startswith('/research/'):
                        intro['url'] = f'/research/{slug}'
                        fixed_count += 1

        # Fix sections.research URLs
        if 'research' in content_data.get('sections', {}):
            for research_item in content_data['sections']['research']:
                if 'url' in research_item:
                    url = research_item['url']
                    # Remove leading slash and check if it's a research slug
                    slug = url.lstrip('/')
                    if slug in research_slugs and not url.startswith('/research/'):
                        research_item['url'] = f'/research/{slug}'
                        fixed_count += 1

        # Fix sections.policy_statements URLs
        if 'policy_statements' in content_data.get('sections', {}):
            for policy in content_data['sections']['policy_statements']:
                if 'url' in policy:
                    url = policy['url']
                    # Remove leading slash and check if it's a research slug
                    slug = url.lstrip('/')
                    if slug in research_slugs and not url.startswith('/research/'):
                        policy['url'] = f'/research/{slug}'
                        fixed_count += 1

        # Fix sections.media_coverage URLs
        if 'media_coverage' in content_data.get('sections', {}):
            for media in content_data['sections']['media_coverage']:
                if 'url' in media:
                    url = media['url']
                    # Remove leading slash and check if it's a research slug
                    slug = url.lstrip('/')
                    if slug in research_slugs and not url.startswith('/research/'):
                        media['url'] = f'/research/{slug}'
                        fixed_count += 1
        
        if fixed_count > 0:
            with open(content_file, 'w', encoding='utf-8') as f:
                json.dump(content_data, f, ensure_ascii=False, indent=2)
            print(f"✅ Updated: {content_file.parent.name} ({fixed_count} URLs fixed)")
    except Exception as e:
        print(f"❌ Error fixing sections in {content_file}: {e}")
    return fixed_count

def main():
    print("🔧 Fixing missing /research/ prefixes in sections URLs...")
    research_slugs = get_research_slugs()
    print(f"📋 Found {len(research_slugs)} research content slugs")

    total_urls_fixed = 0
    total_files_updated = 0
    
    for content_file in CONTENT_DIR.rglob("content.json"):
        urls_fixed = fix_sections_in_file(content_file, research_slugs)
        if urls_fixed > 0:
            total_files_updated += 1
            total_urls_fixed += urls_fixed
        
    print(f"\n🎉 Fixed {total_urls_fixed} URLs in {total_files_updated} research content files")
    print("   All sections URLs now have the correct /research/ prefix")

if __name__ == "__main__":
    main()
