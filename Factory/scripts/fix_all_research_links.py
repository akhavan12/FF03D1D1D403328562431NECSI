#!/usr/bin/env python3
"""
Fix all research links across all research content files to include /research/ prefix
"""

import json
import re
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
CONTENT_DIR = BASE_DIR / "content"

def fix_links_in_content(content, file_path):
    """Fix links in a single content file"""
    if 'narrative_md' not in content:
        return 0
    
    narrative = content['narrative_md']
    original_narrative = narrative
    
    # Find all markdown links
    link_pattern = r'\]\(/([^)]+)\)'
    matches = re.findall(link_pattern, narrative)
    
    links_fixed = 0
    
    for link in matches:
        # Skip if it's already a research link, external link, or asset link
        if (not link.startswith('research/') and 
            not link.startswith('assets/') and 
            not link.startswith('http') and
            not link.startswith('about') and
            not link.startswith('#')):
            
            # Check if this link corresponds to an existing research page
            potential_research_file = CONTENT_DIR / link / "content.json"
            if potential_research_file.exists():
                try:
                    with open(potential_research_file, 'r') as f:
                        research_content = json.load(f)
                        if research_content.get('type') == 'research':
                            old_link = f"/{link}"
                            new_link = f"/research/{link}"
                            narrative = narrative.replace(old_link, new_link)
                            links_fixed += 1
                            print(f"  ✅ {old_link} → {new_link}")
                except:
                    pass
    
    if links_fixed > 0:
        content['narrative_md'] = narrative
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(content, f, indent=2, ensure_ascii=False)
    
    return links_fixed

def fix_all_research_links():
    """Fix research links in all research content files"""
    
    print("🔧 FIXING RESEARCH LINKS ACROSS ALL RESEARCH CONTENT...")
    
    total_fixed = 0
    files_processed = 0
    
    # Get all research content files
    for item in CONTENT_DIR.iterdir():
        if item.is_dir() and (item / "content.json").exists():
            try:
                with open(item / "content.json", 'r', encoding='utf-8') as f:
                    content = json.load(f)
                
                if content.get('type') == 'research':
                    print(f"\n📄 Processing: {item.name}")
                    fixed_count = fix_links_in_content(content, item / "content.json")
                    total_fixed += fixed_count
                    files_processed += 1
                    
                    if fixed_count > 0:
                        print(f"  Fixed {fixed_count} links")
                    else:
                        print(f"  No links to fix")
                        
            except Exception as e:
                print(f"  ❌ Error processing {item.name}: {e}")
    
    print(f"\n📊 SUMMARY:")
    print(f"  📁 Files processed: {files_processed}")
    print(f"  🔗 Total links fixed: {total_fixed}")
    print(f"  ✅ Research links now properly formatted")

if __name__ == "__main__":
    fix_all_research_links()

