#!/usr/bin/env python3
"""
Create root-level Astro pages for all research content to match the original website structure.

This script:
1. Finds all research content files
2. Creates root-level Astro pages (e.g., /steering-the-economy-toward-growth.astro)
3. Updates middleware to not redirect root-level research pages
4. Maintains backward compatibility with /research/ routes
"""

import json
import shutil
from pathlib import Path
from typing import List, Dict

BASE_DIR = Path(__file__).resolve().parents[1]
CONTENT_DIR = BASE_DIR / "content"
ASTRO_PAGES_DIR = BASE_DIR / "sites" / "necsi-site" / "src" / "pages"
MIDDLEWARE_FILE = BASE_DIR / "sites" / "necsi-site" / "src" / "middleware.ts"

def get_research_content() -> List[Dict]:
    """Get all research content files."""
    research_content = []
    
    for content_file in CONTENT_DIR.rglob("content.json"):
        try:
            with open(content_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            # Only process research content
            if data.get('type') == 'research' and data.get('slug'):
                research_content.append({
                    'slug': data['slug'],
                    'title': data.get('title', ''),
                    'file_path': content_file
                })
        except Exception as e:
            print(f"⚠️  Error reading {content_file}: {e}")
    
    return research_content

def create_root_page_template(slug: str, title: str) -> str:
    """Create the Astro page template for a root-level research page."""
    template = '''---
import { getResearchBySlug } from '../lib/content';
import { mdToHtml } from '../lib/markdown';
import BaseLayout from '../layouts/BaseLayout.astro';

const doc = await getResearchBySlug('{slug}');
---

<BaseLayout title="${doc.title} — NECSI">
  <!-- Full-bleed banner behind the sticky nav (nav is translucent) -->
  <section class="relative left-1/2 right-1/2 -ml-[50vw] -mr-[50vw] w-screen -mt-24 -mb-px">
    <div class="relative">
      {doc.hero_image && (
        <img src={doc.hero_image} alt="" class="absolute inset-0 h-full w-full object-cover" />
      )}
      <div class={`relative ${doc.hero_image ? 'bg-transparent' : 'bg-gradient-to-b from-slate-800 to-slate-700'}`}>
        <div class="max-w-6xl mx-auto px-6 md:px-8 lg:px-12 py-20 sm:py-28">
          <h1 class="text-4xl sm:text-5xl font-semibold tracking-tight text-white">{doc.title}</h1>
          {doc.subtitle && (
            <p class="mt-3 text-slate-200 text-lg max-w-3xl">{doc.subtitle}</p>
          )}
        </div>
      </div>
    </div>
  </section>

  <!-- Main Content Container with proper padding and max-width -->
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 sm:py-12">
    <div class="prose prose-lg prose-slate max-w-none">
      <div set:html={mdToHtml(doc.narrative_md)} />
    </div>
  </div>
</BaseLayout>
'''
    return template.format(slug=slug)

def update_middleware(research_slugs: List[str]):
    """Update middleware to not redirect root-level research pages."""
    if not MIDDLEWARE_FILE.exists():
        print(f"❌ Middleware file not found: {MIDDLEWARE_FILE}")
        return False
    
    # Read current middleware
    with open(MIDDLEWARE_FILE, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Create the new excluded paths list
    excluded_paths = [
        '/',
        '/about',
        '/research',
        '/do-we-need-to-age-extending-the-arc-of-life',
        '/index-original',
        '/index-simple',
    ]
    
    # Add all research slugs to excluded paths
    for slug in research_slugs:
        excluded_paths.append(f'/{slug}')
    
    # Sort for consistency
    excluded_paths.sort()
    
    # Create the new EXCLUDED_PATHS array
    excluded_paths_str = '\\n'.join([f"  '{path}'," for path in excluded_paths])
    
    # Replace the EXCLUDED_PATHS array
    import re
    pattern = r'const EXCLUDED_PATHS = \\[[\\s\\S]*?\\];'
    replacement = f'const EXCLUDED_PATHS = [\\n{excluded_paths_str}\\n];'
    
    new_content = re.sub(pattern, replacement, content)
    
    # Write back
    with open(MIDDLEWARE_FILE, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    return True

def main():
    """Main function to create root-level pages."""
    print("🚀 Creating root-level Astro pages for research content...")
    print("=" * 80)
    
    # Get all research content
    research_content = get_research_content()
    print(f"📋 Found {len(research_content)} research content files")
    
    if not research_content:
        print("❌ No research content found")
        return 1
    
    # Create root-level pages
    created_pages = []
    skipped_pages = []
    
    for item in research_content:
        slug = item['slug']
        title = item['title']
        page_file = ASTRO_PAGES_DIR / f"{slug}.astro"
        
        # Skip if page already exists
        if page_file.exists():
            print(f"⏭️  Skipping {slug} (already exists)")
            skipped_pages.append(slug)
            continue
        
        # Create the page
        try:
            page_content = create_root_page_template(slug, title)
            with open(page_file, 'w', encoding='utf-8') as f:
                f.write(page_content)
            
            print(f"✅ Created: {slug}.astro")
            created_pages.append(slug)
            
        except Exception as e:
            print(f"❌ Failed to create {slug}.astro: {e}")
    
    # Update middleware
    print(f"\\n🔧 Updating middleware...")
    all_slugs = [item['slug'] for item in research_content]
    if update_middleware(all_slugs):
        print(f"✅ Updated middleware with {len(all_slugs)} research slugs")
    else:
        print(f"❌ Failed to update middleware")
    
    # Summary
    print("\\n" + "=" * 80)
    print("📊 ROOT PAGE CREATION SUMMARY")
    print("=" * 80)
    
    print(f"\\n✅ Created pages: {len(created_pages)}")
    print(f"⏭️  Skipped pages: {len(skipped_pages)}")
    print(f"📈 Total research pages: {len(research_content)}")
    
    if created_pages:
        print(f"\\n📄 Created root-level pages:")
        for slug in created_pages[:10]:  # Show first 10
            print(f"   • /{slug}")
        if len(created_pages) > 10:
            print(f"   ... and {len(created_pages) - 10} more")
    
    if skipped_pages:
        print(f"\\n⏭️  Skipped pages (already exist):")
        for slug in skipped_pages[:10]:  # Show first 10
            print(f"   • /{slug}")
        if len(skipped_pages) > 10:
            print(f"   ... and {len(skipped_pages) - 10} more")
    
    print(f"\\n🎉 Root-level pages created successfully!")
    print("   The Astro site now matches the original website structure:")
    print("   • Research pages are available at root level (e.g., /steering-the-economy-toward-growth)")
    print("   • /research/ routes are still available for backward compatibility")
    print("   • Middleware updated to not redirect root-level research pages")
    
    return 0

if __name__ == "__main__":
    exit(main())
