#!/usr/bin/env python3
"""
Fix image paths for Astro - remove /public prefix since Astro serves from public/ without the prefix
"""

import json
import re
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
CONTENT_DIR = BASE_DIR / "content"
RESEARCH_FILE = CONTENT_DIR / "research" / "content.json"

def fix_astro_image_paths():
    """Fix image paths for Astro by removing /public prefix"""
    
    if not RESEARCH_FILE.exists():
        print(f"Research file not found: {RESEARCH_FILE}")
        return
    
    # Read research content
    with open(RESEARCH_FILE, 'r', encoding='utf-8') as f:
        content = json.load(f)
    
    print("🔧 FIXING IMAGE PATHS FOR ASTRO...")
    
    # Count original paths
    original_count = content['narrative_md'].count('/public/assets/')
    print(f"📊 Found {original_count} /public/assets/ paths to fix")
    
    # Fix hero_image path
    if content.get('hero_image', '').startswith('/public/assets/'):
        content['hero_image'] = content['hero_image'].replace('/public/assets/', '/assets/')
        print("✅ Fixed hero_image path")
    
    # Fix narrative_md paths
    if 'narrative_md' in content:
        # Replace all /public/assets/ with /assets/ in narrative
        content['narrative_md'] = content['narrative_md'].replace('/public/assets/', '/assets/')
        
        # Count fixed paths
        fixed_count = content['narrative_md'].count('/assets/')
        print(f"✅ Fixed {fixed_count} image paths in narrative")
    
    # Save updated content
    with open(RESEARCH_FILE, 'w', encoding='utf-8') as f:
        json.dump(content, f, indent=2, ensure_ascii=False)
    
    print("💾 Updated research content saved")
    print(f"🎯 Image paths fixed: /public/assets/ → /assets/")

if __name__ == "__main__":
    fix_astro_image_paths()
