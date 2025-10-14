#!/usr/bin/env python3
"""
Analyze all links in the research page to identify which ones need updating
"""

import json
import re
from pathlib import Path
from collections import defaultdict

BASE_DIR = Path(__file__).resolve().parents[1]
CONTENT_DIR = BASE_DIR / "content"
RESEARCH_FILE = CONTENT_DIR / "research" / "content.json"

def extract_links_from_markdown(markdown_content):
    """Extract all links from markdown content"""
    links = []
    
    # Pattern to match markdown links like [text](url)
    link_pattern = r'\[([^\]]*)\]\(([^)]+)\)'
    matches = re.findall(link_pattern, markdown_content)
    
    for text, url in matches:
        links.append({
            'text': text,
            'url': url,
            'type': 'markdown_link'
        })
    
    return links

def analyze_links():
    """Analyze all links in the research page"""
    
    if not RESEARCH_FILE.exists():
        print(f"Research file not found: {RESEARCH_FILE}")
        return
    
    # Read research content
    with open(RESEARCH_FILE, 'r', encoding='utf-8') as f:
        content = json.load(f)
    
    print("=== RESEARCH PAGE LINK ANALYSIS ===\n")
    
    # Extract links from narrative
    if 'narrative_md' in content:
        links = extract_links_from_markdown(content['narrative_md'])
        
        # Categorize links
        categories = {
            'local_research': [],
            'external_necsi': [],
            'external_other': [],
            'image_links': [],
            'broken_links': []
        }
        
        for link in links:
            url = link['url']
            
            if url.startswith('/research/'):
                categories['local_research'].append(link)
            elif 'necsi.edu' in url:
                categories['external_necsi'].append(link)
            elif url.startswith('https://') or url.startswith('http://'):
                categories['external_other'].append(link)
            elif url.startswith('/') and not url.startswith('/research'):
                categories['broken_links'].append(link)
            elif url.startswith('/assets/'):
                categories['image_links'].append(link)
            else:
                # Assume it's a local research page without /research prefix
                categories['local_research'].append(link)
        
        # Print analysis
        print(f"📊 TOTAL LINKS FOUND: {len(links)}\n")
        
        print("✅ LOCAL RESEARCH LINKS:")
        for link in categories['local_research']:
            print(f"  • {link['text'][:50]}... → {link['url']}")
        print(f"  Count: {len(categories['local_research'])}\n")
        
        print("⚠️  EXTERNAL NECSI LINKS (need updating):")
        for link in categories['external_necsi']:
            print(f"  • {link['text'][:50]}... → {link['url']}")
        print(f"  Count: {len(categories['external_necsi'])}\n")
        
        print("🔗 EXTERNAL OTHER LINKS:")
        for link in categories['external_other']:
            print(f"  • {link['text'][:50]}... → {link['url']}")
        print(f"  Count: {len(categories['external_other'])}\n")
        
        print("🖼️  IMAGE LINKS:")
        for link in categories['image_links']:
            print(f"  • {link['text'][:50]}... → {link['url']}")
        print(f"  Count: {len(categories['image_links'])}\n")
        
        print("❌ BROKEN LINKS (need fixing):")
        for link in categories['broken_links']:
            print(f"  • {link['text'][:50]}... → {link['url']}")
        print(f"  Count: {len(categories['broken_links'])}\n")
        
        # Summary
        print("=== SUMMARY ===")
        print(f"✅ Working local links: {len(categories['local_research'])}")
        print(f"⚠️  External NECSI links to fix: {len(categories['external_necsi'])}")
        print(f"❌ Broken links to fix: {len(categories['broken_links'])}")
        print(f"🔗 External other links: {len(categories['external_other'])}")
        print(f"🖼️  Image links: {len(categories['image_links'])}")

if __name__ == "__main__":
    analyze_links()
