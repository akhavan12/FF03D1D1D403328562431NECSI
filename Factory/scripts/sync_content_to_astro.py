#!/usr/bin/env python3
"""
Sync built content from Factory to Astro site.

This script:
1. Finds all BUILT content in Factory
2. Copies it to the Astro site's content directory
3. Ensures the Astro site has the latest content
"""

import json
import shutil
from pathlib import Path
from typing import List, Dict

BASE_DIR = Path(__file__).resolve().parents[1]
FACTORY_CONTENT_DIR = BASE_DIR / "content"
ASTRO_CONTENT_DIR = BASE_DIR.parents[0] / "sites" / "necsi-site" / "content"

def get_built_content() -> List[Path]:
    """Get all content that has been built to BUILT state."""
    built_content = []
    state_dir = BASE_DIR / "orchestrator" / "state"
    
    for state_file in state_dir.glob("*.json"):
        try:
            with open(state_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            # Check if content is in BUILT state
            if data.get('status') == 'BUILT':
                slug = data.get('slug')
                if slug:
                    content_dir = FACTORY_CONTENT_DIR / slug
                    if content_dir.exists():
                        built_content.append(content_dir)
                
        except Exception:
            pass
    
    return built_content

def sync_content_to_astro():
    """Sync built content to Astro site."""
    print("🔄 Syncing built content to Astro site...")
    
    # Get all built content
    built_content_dirs = get_built_content()
    print(f"📋 Found {len(built_content_dirs)} built content directories")
    
    # Ensure Astro content directory exists
    ASTRO_CONTENT_DIR.mkdir(parents=True, exist_ok=True)
    
    synced_count = 0
    
    for content_dir in built_content_dirs:
        try:
            # Get the slug from the content.json
            content_file = content_dir / "content.json"
            with open(content_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            slug = data.get('slug')
            if not slug:
                continue
                
            # Destination directory in Astro site
            dest_dir = ASTRO_CONTENT_DIR / slug
            
            # Copy the entire content directory
            if dest_dir.exists():
                shutil.rmtree(dest_dir)
            
            shutil.copytree(content_dir, dest_dir)
            synced_count += 1
            
            if synced_count % 50 == 0:
                print(f"✅ Synced {synced_count} content directories...")
                
        except Exception as e:
            print(f"❌ Error syncing {content_dir}: {e}")
    
    print(f"\n🎉 Successfully synced {synced_count} content directories to Astro site")
    print(f"   Content is now available at: {ASTRO_CONTENT_DIR}")

if __name__ == "__main__":
    sync_content_to_astro()
