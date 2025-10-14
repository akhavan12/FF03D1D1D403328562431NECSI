#!/usr/bin/env python3
"""
Fix internal links in research content to point to correct /research/ URLs.

This script:
1. Finds all research content files
2. Updates internal links to point to /research/slug instead of /slug
3. Preserves external links and asset links
"""

import json
import re
from pathlib import Path
from typing import List, Dict, Set

BASE_DIR = Path(__file__).resolve().parents[1]
CONTENT_DIR = BASE_DIR / "content"

def get_all_research_slugs() -> Set[str]:
    """Get all research content slugs."""
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

def fix_links_in_content(content: str, research_slugs: Set[str]) -> str:
    """Fix internal links in content to point to /research/ URLs."""
    # Pattern to match markdown links: [text](/slug)
    # This will match internal links that start with / and don't start with /research/
    def replace_link(match):
        full_match = match.group(0)
        link_text = match.group(1)
        link_url = match.group(2)
        
        # Skip if it's already a /research/ link
        if link_url.startswith('/research/'):
            return full_match
            
        # Skip if it's an external link
        if link_url.startswith('http'):
            return full_match
            
        # Skip if it's an asset link
        if link_url.startswith('/assets/') or link_url.startswith('/s/'):
            return full_match
            
        # Skip if it's a special page
        if link_url in ['/', '/about', '/research']:
            return full_match
            
        # Extract the slug from the URL
        slug = link_url.lstrip('/')
        
        # If this slug exists as research content, update the link
        if slug in research_slugs:
            new_url = f'/research/{slug}'
            return f'[{link_text}]({new_url})'
        
        # Return unchanged if not a research slug
        return full_match
    
    # Apply the replacement
    pattern = r'\[([^\]]+)\]\(([^)]+)\)'
    return re.sub(pattern, replace_link, content)

def main():
    print("🔧 Fixing internal research links...")
    
    # Get all research slugs
    research_slugs = get_all_research_slugs()
    print(f"📋 Found {len(research_slugs)} research content slugs")
    
    # Process all research content files
    updated_count = 0
    total_count = 0
    
    for content_file in CONTENT_DIR.rglob("content.json"):
        try:
            with open(content_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Only process research content
            if data.get('type') != 'research':
                continue
                
            total_count += 1
            original_content = data.get('narrative_md', '')
            
            if original_content:
                # Fix the links
                updated_content = fix_links_in_content(original_content, research_slugs)
                
                # Check if anything changed
                if updated_content != original_content:
                    data['narrative_md'] = updated_content
                    
                    # Write back the updated content
                    with open(content_file, 'w', encoding='utf-8') as f:
                        json.dump(data, f, indent=2, ensure_ascii=False)
                    
                    updated_count += 1
                    print(f"✅ Updated: {data.get('slug', 'unknown')}")
                    
        except Exception as e:
            print(f"❌ Error processing {content_file}: {e}")
    
    print(f"\n🎉 Fixed internal links in {updated_count}/{total_count} research content files")
    print("   All internal research links now point to /research/slug URLs")

if __name__ == "__main__":
    main()
