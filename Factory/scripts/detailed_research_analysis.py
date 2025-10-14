#!/usr/bin/env python3
"""
Detailed analysis of the research page and its links
"""

import json
import re
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
CONTENT_DIR = BASE_DIR / "content"
RESEARCH_FILE = CONTENT_DIR / "research" / "content.json"

def get_all_research_slugs():
    """Get all available research slugs"""
    slugs = []
    for item in CONTENT_DIR.iterdir():
        if item.is_dir() and (item / "content.json").exists():
            try:
                with open(item / "content.json", 'r') as f:
                    content = json.load(f)
                    if content.get('type') == 'research':
                        slugs.append(item.name)
            except:
                pass
    return sorted(slugs)

def analyze_research_page():
    """Analyze the research page in detail"""
    
    if not RESEARCH_FILE.exists():
        print(f"Research file not found: {RESEARCH_FILE}")
        return
    
    # Read research content
    with open(RESEARCH_FILE, 'r', encoding='utf-8') as f:
        content = json.load(f)
    
    print("=== DETAILED RESEARCH PAGE ANALYSIS ===\n")
    
    # Get available research slugs
    available_slugs = get_all_research_slugs()
    print(f"📚 AVAILABLE RESEARCH PAGES: {len(available_slugs)}")
    print("Available slugs:", ", ".join(available_slugs[:10]) + ("..." if len(available_slugs) > 10 else ""))
    print()
    
    # Analyze narrative content
    if 'narrative_md' in content:
        narrative = content['narrative_md']
        
        # Find all research page links (patterns like [/slug] or [/research/slug])
        research_link_pattern = r'\]\(/([^)]+)\)'
        research_links = re.findall(research_link_pattern, narrative)
        
        print("🔗 RESEARCH PAGE LINKS FOUND:")
        valid_links = []
        broken_links = []
        
        for link in set(research_links):
            if link.startswith('research/'):
                slug = link.replace('research/', '')
            else:
                slug = link
            
            if slug in available_slugs:
                valid_links.append(link)
                print(f"  ✅ {link} → EXISTS")
            else:
                broken_links.append(link)
                print(f"  ❌ {link} → MISSING")
        
        print(f"\n📊 LINK SUMMARY:")
        print(f"  ✅ Valid research links: {len(valid_links)}")
        print(f"  ❌ Broken research links: {len(broken_links)}")
        
        if broken_links:
            print(f"\n🔧 BROKEN LINKS TO FIX:")
            for link in broken_links:
                print(f"  • {link}")
        
        # Find image links
        image_pattern = r'\]\((/assets/[^)]+)\)'
        image_links = re.findall(image_pattern, narrative)
        print(f"\n🖼️  IMAGE LINKS: {len(image_links)}")
        
        # Find external links
        external_pattern = r'\]\((https?://[^)]+)\)'
        external_links = re.findall(external_pattern, narrative)
        print(f"🌐 EXTERNAL LINKS: {len(external_links)}")
        for link in external_links:
            print(f"  • {link}")

if __name__ == "__main__":
    analyze_research_page()
