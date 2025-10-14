#!/usr/bin/env python3
"""
Fix internal links in content files by adding /research/ prefix where needed.

This script:
1. Identifies all content pages
2. Finds internal links in narrative_md
3. Checks if links need /research/ prefix
4. Updates the content files with corrected links

Usage:
  python scripts/fix_internal_links.py --dry-run  # Show what would change
  python scripts/fix_internal_links.py            # Actually fix the links
"""
import argparse
import json
import re
from pathlib import Path
from typing import Dict, Set, List

BASE_DIR = Path(__file__).resolve().parents[1]
CONTENT_DIR = BASE_DIR / "content"

# Pattern to find markdown links
MD_LINK_PATTERN = re.compile(r'\[([^\]]+)\]\((/[^\)]+)\)')


class LinkFixer:
    def __init__(self, dry_run=False):
        self.dry_run = dry_run
        self.all_slugs: Set[str] = set()
        self.root_level_pages: Set[str] = set()
        self.changes_made = 0
        self.files_changed = 0
        
    def discover_pages(self):
        """Discover all pages and determine which are at root level."""
        print(f"🔍 Discovering all pages...")
        
        # Check which pages have dedicated root-level .astro files in sites/necsi-site
        site_pages_dir = BASE_DIR.parent / "sites" / "necsi-site" / "src" / "pages"
        
        if site_pages_dir.exists():
            for astro_file in site_pages_dir.glob("*.astro"):
                if astro_file.stem not in ['index', 'about', 'index-original', 'index-simple']:
                    self.root_level_pages.add(astro_file.stem)
                    print(f"  ✓ Root-level page: /{astro_file.stem}")
        
        # Discover all content slugs
        for content_file in CONTENT_DIR.rglob("content.json"):
            try:
                with open(content_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    slug = data.get('slug')
                    if slug:
                        self.all_slugs.add(slug)
            except:
                pass
        
        print(f"✅ Found {len(self.all_slugs)} total pages")
        print(f"✅ Found {len(self.root_level_pages)} root-level pages\n")
    
    def should_add_research_prefix(self, link: str) -> bool:
        """Determine if a link needs /research/ prefix."""
        # Remove leading slash and anchor
        clean_link = link.lstrip('/').split('#')[0].split('?')[0]
        
        # Skip if already has /research/
        if link.startswith('/research/'):
            return False
        
        # Skip external links, assets, etc
        if any(link.startswith(prefix) for prefix in ['http://', 'https://', '/assets/', '/s/', 'mailto:', 'tel:']):
            return False
        
        # Skip anchors only
        if link.startswith('#'):
            return False
        
        # If it's a root-level page, don't add prefix
        if clean_link in self.root_level_pages:
            return False
        
        # If the slug exists and it's not a root-level page, add /research/
        if clean_link in self.all_slugs:
            return True
        
        return False
    
    def fix_links_in_markdown(self, text: str) -> tuple[str, int]:
        """Fix internal links in markdown text."""
        if not text:
            return text, 0
        
        changes = 0
        
        def replace_link(match):
            nonlocal changes
            link_text = match.group(1)
            url = match.group(2)
            
            if self.should_add_research_prefix(url):
                changes += 1
                new_url = f"/research{url}"
                if not self.dry_run:
                    print(f"    {url} → {new_url}")
                return f"[{link_text}]({new_url})"
            
            return match.group(0)
        
        fixed_text = MD_LINK_PATTERN.sub(replace_link, text)
        return fixed_text, changes
    
    def fix_content_file(self, content_file: Path):
        """Fix links in a single content file."""
        try:
            with open(content_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except Exception as e:
            print(f"⚠️  Error reading {content_file}: {e}")
            return
        
        slug = data.get('slug', 'unknown')
        title = data.get('title', 'Unknown')
        
        # Fix links in narrative_md
        narrative = data.get('narrative_md', '')
        fixed_narrative, changes = self.fix_links_in_markdown(narrative)
        
        if changes > 0:
            self.files_changed += 1
            self.changes_made += changes
            
            if self.dry_run:
                print(f"📄 {title} ({slug})")
                print(f"   Would fix {changes} link(s) in narrative_md")
            else:
                print(f"📄 {title} ({slug})")
                data['narrative_md'] = fixed_narrative
                
                # Write back to file
                with open(content_file, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
                
                print(f"   ✓ Fixed {changes} link(s)")
            
            print()
    
    def fix_all_files(self):
        """Fix links in all content files."""
        print("🔧 Fixing internal links in all content files...\n")
        
        content_files = list(CONTENT_DIR.rglob("content.json"))
        
        for content_file in content_files:
            self.fix_content_file(content_file)
        
        print("=" * 80)
        if self.dry_run:
            print("📊 DRY RUN SUMMARY")
        else:
            print("📊 SUMMARY")
        print("=" * 80)
        print(f"Files that would be changed: {self.files_changed}")
        print(f"Total links that would be fixed: {self.changes_made}")
        
        if self.dry_run:
            print("\n💡 Run without --dry-run to actually make these changes")
        else:
            print("\n✅ All links fixed!")


def main():
    parser = argparse.ArgumentParser(description='Fix internal links in content files')
    parser.add_argument('--dry-run', action='store_true',
                       help='Show what would be changed without making changes')
    
    args = parser.parse_args()
    
    fixer = LinkFixer(dry_run=args.dry_run)
    
    # Discover all pages
    fixer.discover_pages()
    
    # Fix all links
    fixer.fix_all_files()
    
    return 0


if __name__ == '__main__':
    exit(main())

