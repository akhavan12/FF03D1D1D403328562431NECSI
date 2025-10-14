#!/usr/bin/env python3
"""
Fix research page links to include /research/ prefix for proper routing
"""

import json
import re
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
CONTENT_DIR = BASE_DIR / "content"
RESEARCH_FILE = CONTENT_DIR / "research" / "content.json"

def fix_research_links():
    """Fix research page links to include /research/ prefix"""
    
    if not RESEARCH_FILE.exists():
        print(f"Research file not found: {RESEARCH_FILE}")
        return
    
    # Read research content
    with open(RESEARCH_FILE, 'r', encoding='utf-8') as f:
        content = json.load(f)
    
    print("🔧 FIXING RESEARCH PAGE LINKS...")
    
    if 'narrative_md' in content:
        narrative = content['narrative_md']
        
        # Count links that need fixing (links that start with / but don't start with /research/)
        # and are not external links or asset links
        links_to_fix = []
        
        # Find all markdown links
        link_pattern = r'\]\(/([^)]+)\)'
        matches = re.findall(link_pattern, narrative)
        
        for link in matches:
            # Skip if it's already a research link, external link, or asset link
            if (not link.startswith('research/') and 
                not link.startswith('assets/') and 
                not link.startswith('http')):
                links_to_fix.append(link)
        
        print(f"📊 Found {len(links_to_fix)} links to fix")
        
        # Fix each link
        for link in links_to_fix:
            old_link = f"/{link}"
            new_link = f"/research/{link}"
            narrative = narrative.replace(old_link, new_link)
            print(f"  ✅ {old_link} → {new_link}")
        
        content['narrative_md'] = narrative
        
        # Save updated content
        with open(RESEARCH_FILE, 'w', encoding='utf-8') as f:
            json.dump(content, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Updated research content saved")
        print(f"🎯 Fixed {len(links_to_fix)} research links")

if __name__ == "__main__":
    fix_research_links()

