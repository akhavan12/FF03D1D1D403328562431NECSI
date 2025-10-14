#!/usr/bin/env python3
"""
Check all internal links in content files to ensure they point to existing pages.

Usage:
  python scripts/check_internal_links.py
  python scripts/check_internal_links.py --fix-suggestions

This script will:
1. Scan all content.json files
2. Extract internal links from narrative_md and sections
3. Check if those links point to existing pages
4. Report broken links with suggestions for fixes
"""
import argparse
import json
import re
from pathlib import Path
from collections import defaultdict
from typing import Dict, List, Set, Tuple

# Base directory
BASE_DIR = Path(__file__).resolve().parents[1]
CONTENT_DIR = BASE_DIR / "content"

# Regex patterns for finding links
MD_LINK_PATTERN = re.compile(r'\[([^\]]+)\]\(([^\)]+)\)')
HTML_LINK_PATTERN = re.compile(r'<a\s+[^>]*href=["\'](.*?)["\']', re.IGNORECASE)


class LinkChecker:
    def __init__(self):
        self.all_slugs: Set[str] = set()
        self.slug_to_path: Dict[str, Path] = {}
        self.broken_links: List[Dict] = []
        self.link_stats = defaultdict(int)
        
    def discover_all_pages(self):
        """Discover all available content pages and their slugs."""
        print(f"🔍 Scanning content directory: {CONTENT_DIR}")
        
        for content_file in CONTENT_DIR.rglob("content.json"):
            try:
                with open(content_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    slug = data.get('slug')
                    if slug:
                        self.all_slugs.add(slug)
                        self.slug_to_path[slug] = content_file
                        # Also add with leading slash
                        self.all_slugs.add(f"/{slug}")
            except Exception as e:
                print(f"⚠️  Error reading {content_file}: {e}")
        
        print(f"✅ Found {len(self.all_slugs)} pages")
        return self.all_slugs
    
    def extract_links_from_markdown(self, text: str) -> List[str]:
        """Extract all links from Markdown text."""
        if not text:
            return []
        
        links = []
        # Markdown links: [text](url)
        for match in MD_LINK_PATTERN.finditer(text):
            url = match.group(2)
            links.append(url)
        
        # HTML links in markdown: <a href="url">
        for match in HTML_LINK_PATTERN.finditer(text):
            url = match.group(1)
            links.append(url)
        
        return links
    
    def is_internal_link(self, url: str) -> bool:
        """Check if a URL is an internal link."""
        if not url:
            return False
        
        # Skip external URLs
        if url.startswith(('http://', 'https://', 'mailto:', 'tel:', 'ftp://')):
            return False
        
        # Skip anchors only
        if url.startswith('#'):
            return False
        
        # Skip assets
        if url.startswith('/assets/') or '/assets/' in url:
            return False
        
        return True
    
    def normalize_link(self, url: str) -> str:
        """Normalize a link by removing anchors and query params."""
        # Remove anchor
        if '#' in url:
            url = url.split('#')[0]
        
        # Remove query params
        if '?' in url:
            url = url.split('?')[0]
        
        # Remove trailing slash
        url = url.rstrip('/')
        
        # Ensure leading slash
        if url and not url.startswith('/'):
            url = f"/{url}"
        
        return url
    
    def check_link_exists(self, link: str) -> bool:
        """Check if an internal link points to an existing page."""
        normalized = self.normalize_link(link)
        
        # Check exact match
        if normalized in self.all_slugs:
            return True
        
        # Check without leading slash
        if normalized.lstrip('/') in self.all_slugs:
            return True
        
        # Check /research/ prefix
        if not normalized.startswith('/research/'):
            research_link = f"/research{normalized}"
            if research_link in self.all_slugs or research_link.lstrip('/') in self.all_slugs:
                return True
        
        return False
    
    def find_suggestions(self, broken_link: str) -> List[str]:
        """Find possible suggestions for a broken link."""
        normalized = self.normalize_link(broken_link).lower()
        suggestions = []
        
        # Look for similar slugs
        for slug in self.all_slugs:
            slug_lower = slug.lower()
            
            # Exact substring match
            if normalized in slug_lower or slug_lower in normalized:
                suggestions.append(slug)
            
            # Word overlap
            broken_words = set(normalized.strip('/').split('-'))
            slug_words = set(slug_lower.strip('/').split('-'))
            overlap = broken_words & slug_words
            if len(overlap) >= 2:  # At least 2 words in common
                suggestions.append(slug)
        
        return suggestions[:5]  # Return top 5 suggestions
    
    def check_page(self, content_file: Path) -> Dict:
        """Check all links in a single page."""
        try:
            with open(content_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except Exception as e:
            return {'error': str(e)}
        
        slug = data.get('slug', 'unknown')
        title = data.get('title', 'Unknown')
        
        # Extract links from narrative_md
        narrative = data.get('narrative_md', '')
        links = self.extract_links_from_markdown(narrative)
        
        # Extract links from sections
        sections = data.get('sections', {})
        for section_name, items in sections.items():
            if isinstance(items, list):
                for item in items:
                    if isinstance(item, dict) and 'url' in item:
                        links.append(item['url'])
        
        # Check each link
        page_broken_links = []
        for link in links:
            if self.is_internal_link(link):
                self.link_stats['internal'] += 1
                if not self.check_link_exists(link):
                    self.link_stats['broken'] += 1
                    suggestions = self.find_suggestions(link)
                    page_broken_links.append({
                        'link': link,
                        'normalized': self.normalize_link(link),
                        'suggestions': suggestions
                    })
                else:
                    self.link_stats['valid'] += 1
            else:
                self.link_stats['external'] += 1
        
        if page_broken_links:
            return {
                'slug': slug,
                'title': title,
                'file': str(content_file),
                'broken_links': page_broken_links
            }
        
        return None
    
    def check_all_pages(self):
        """Check links in all pages."""
        print(f"\n🔗 Checking internal links in all pages...\n")
        
        content_files = list(CONTENT_DIR.rglob("content.json"))
        
        for i, content_file in enumerate(content_files, 1):
            result = self.check_page(content_file)
            if result and not result.get('error'):
                if result.get('broken_links'):
                    self.broken_links.append(result)
            
            # Progress indicator
            if i % 20 == 0:
                print(f"  Checked {i}/{len(content_files)} pages...")
        
        print(f"  Checked {len(content_files)}/{len(content_files)} pages ✓\n")
    
    def print_report(self, show_suggestions: bool = False):
        """Print a report of all broken links."""
        print("=" * 80)
        print("📊 LINK CHECK REPORT")
        print("=" * 80)
        
        print(f"\n📈 Statistics:")
        print(f"  • Total internal links found: {self.link_stats['internal']}")
        print(f"  • Valid links: {self.link_stats['valid']} ✅")
        print(f"  • Broken links: {self.link_stats['broken']} ❌")
        print(f"  • External links (not checked): {self.link_stats['external']}")
        
        if not self.broken_links:
            print(f"\n🎉 All internal links are valid!")
            return
        
        print(f"\n❌ Found {len(self.broken_links)} pages with broken links:\n")
        
        for page in self.broken_links:
            print(f"📄 {page['title']} ({page['slug']})")
            print(f"   File: {page['file']}")
            
            for broken in page['broken_links']:
                print(f"   ❌ {broken['link']}")
                if broken['normalized'] != broken['link']:
                    print(f"      (normalized: {broken['normalized']})")
                
                if show_suggestions and broken['suggestions']:
                    print(f"      💡 Did you mean:")
                    for suggestion in broken['suggestions']:
                        print(f"         • {suggestion}")
            
            print()
        
        print("=" * 80)
    
    def save_report(self, output_file: str = "link-check-report.json"):
        """Save report to JSON file."""
        report = {
            'statistics': dict(self.link_stats),
            'broken_links': self.broken_links,
            'total_pages_checked': len(list(CONTENT_DIR.rglob("content.json"))),
            'pages_with_broken_links': len(self.broken_links)
        }
        
        output_path = BASE_DIR / "jobs" / "reports" / output_file
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2)
        
        print(f"💾 Report saved to: {output_path}")


def main():
    parser = argparse.ArgumentParser(description='Check internal links in content files')
    parser.add_argument('--fix-suggestions', action='store_true',
                       help='Show suggestions for fixing broken links')
    parser.add_argument('--save-report', action='store_true',
                       help='Save report to JSON file')
    
    args = parser.parse_args()
    
    checker = LinkChecker()
    
    # Discover all pages
    checker.discover_all_pages()
    
    # Check all links
    checker.check_all_pages()
    
    # Print report
    checker.print_report(show_suggestions=args.fix_suggestions)
    
    # Save report if requested
    if args.save_report:
        checker.save_report()
    
    # Exit with error code if broken links found
    if checker.broken_links:
        return 1
    
    return 0


if __name__ == '__main__':
    exit(main())

