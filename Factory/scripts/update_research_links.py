#!/usr/bin/env python3
"""
Update research page links to point to local Astro research pages
"""

import json
import re
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
CONTENT_DIR = BASE_DIR / "content"
RESEARCH_FILE = CONTENT_DIR / "research" / "content.json"

def update_links_in_markdown(markdown_content):
    """Update external necsi.edu links to local research pages"""
    
    # Pattern to match markdown links like [text](/slug) or [text](https://necsi.edu/slug)
    link_pattern = r'\[([^\]]+)\]\(([^)]+)\)'
    
    def replace_link(match):
        text = match.group(1)
        url = match.group(2)
        
        # If it's already a relative link starting with /, keep it
        if url.startswith('/') and not url.startswith('//'):
            return match.group(0)
        
        # If it's an external necsi.edu link, convert to local
        if 'necsi.edu' in url:
            # Extract slug from URL
            if '/research/' in url:
                slug = url.split('/research/')[-1]
            elif url.endswith('/'):
                slug = url.rstrip('/').split('/')[-1]
            else:
                slug = url.split('/')[-1]
            
            # Clean up slug (remove query params, etc.)
            slug = slug.split('?')[0].split('#')[0]
            
            return f'[{text}](/research/{slug})'
        
        # If it's a simple slug without leading slash, assume it's a research page
        if not url.startswith('http') and not url.startswith('/') and not url.startswith('#'):
            return f'[{text}](/research/{url})'
        
        # For other links, keep as is
        return match.group(0)
    
    return re.sub(link_pattern, replace_link, markdown_content)

def main():
    """Update the research page content with local links"""
    
    if not RESEARCH_FILE.exists():
        print(f"Research file not found: {RESEARCH_FILE}")
        return
    
    # Read current content
    with open(RESEARCH_FILE, 'r', encoding='utf-8') as f:
        content = json.load(f)
    
    # Update the narrative markdown
    if 'narrative_md' in content:
        print("Updating links in research narrative...")
        content['narrative_md'] = update_links_in_markdown(content['narrative_md'])
    
    # Update sections links
    if 'sections' in content:
        print("Updating links in research sections...")
        for section_name, items in content['sections'].items():
            if isinstance(items, list):
                for item in items:
                    if isinstance(item, dict) and 'url' in item:
                        url = item['url']
                        if 'necsi.edu' in url or (url.startswith('/') and not url.startswith('/research')):
                            # Extract slug and convert to local research link
                            if '/research/' in url:
                                slug = url.split('/research/')[-1]
                            else:
                                slug = url.strip('/').split('/')[-1]
                            item['url'] = f'/research/{slug}'
    
    # Write updated content back
    with open(RESEARCH_FILE, 'w', encoding='utf-8') as f:
        json.dump(content, f, indent=2, ensure_ascii=False)
    
    print(f"Updated research content: {RESEARCH_FILE}")

if __name__ == "__main__":
    main()
