#!/usr/bin/env python3
"""
Crawl the local dev site and find all missing pages (404s).

This script:
1. Crawls pages from your local dev server (http://localhost:4321)
2. Extracts all internal links
3. Tests each link to see if it returns 404
4. Reports which pages are missing so you can import them

Usage:
  python scripts/find_missing_pages.py
  python scripts/find_missing_pages.py --base-url http://localhost:4321
  python scripts/find_missing_pages.py --start-urls /,/research,/about
  python scripts/find_missing_pages.py --output missing-pages.txt
"""
import argparse
import requests
import re
from collections import defaultdict
from pathlib import Path
from typing import Set, Dict, List
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
import time

BASE_DIR = Path(__file__).resolve().parents[1]


class SiteCrawler:
    def __init__(self, base_url: str = "http://localhost:4321", max_pages: int = 500):
        self.base_url = base_url.rstrip('/')
        self.max_pages = max_pages
        self.visited: Set[str] = set()
        self.to_visit: List[str] = []
        self.missing_pages: Dict[str, List[str]] = defaultdict(list)  # missing_url -> [pages that link to it]
        self.checked_urls: Set[str] = set()
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'NECSI Link Checker/1.0'
        })
    
    def is_internal_url(self, url: str) -> bool:
        """Check if a URL is internal to the site."""
        if not url:
            return False
        
        # Skip external protocols
        if url.startswith(('mailto:', 'tel:', 'javascript:', 'data:')):
            return False
        
        # Skip anchors only
        if url.startswith('#'):
            return False
        
        # Parse URL
        parsed = urlparse(url)
        
        # If absolute URL, check domain
        if parsed.netloc:
            return parsed.netloc in ['localhost:4321', 'localhost']
        
        # Relative URLs are internal
        return True
    
    def normalize_url(self, url: str, base_page: str) -> str:
        """Convert a URL to absolute form."""
        # Join with base URL
        full_url = urljoin(base_page, url)
        
        # Parse and clean
        parsed = urlparse(full_url)
        
        # Remove fragment
        path = parsed.path
        
        # Normalize path
        if path and not path.startswith('/'):
            path = '/' + path
        
        # Build clean URL
        clean_url = f"{parsed.scheme}://{parsed.netloc}{path}"
        
        return clean_url.rstrip('/')
    
    def extract_links(self, html: str, page_url: str) -> List[str]:
        """Extract all internal links from HTML."""
        links = []
        
        try:
            soup = BeautifulSoup(html, 'html.parser')
            
            # Find all <a> tags
            for a_tag in soup.find_all('a', href=True):
                href = a_tag['href']
                
                if self.is_internal_url(href):
                    normalized = self.normalize_url(href, page_url)
                    links.append(normalized)
        
        except Exception as e:
            print(f"⚠️  Error parsing HTML from {page_url}: {e}")
        
        return links
    
    def check_url(self, url: str) -> int:
        """Check if a URL returns 200, 404, or other status."""
        try:
            # Follow redirects
            resp = self.session.get(url, allow_redirects=True, timeout=10)
            return resp.status_code
        except Exception as e:
            print(f"⚠️  Error checking {url}: {e}")
            return -1
    
    def crawl_page(self, url: str) -> bool:
        """Crawl a single page and extract its links."""
        if url in self.visited or len(self.visited) >= self.max_pages:
            return False
        
        print(f"🔍 Crawling: {url}")
        self.visited.add(url)
        
        try:
            resp = self.session.get(url, timeout=10)
            
            if resp.status_code != 200:
                print(f"   ⚠️  Got {resp.status_code}")
                return False
            
            # Extract links
            links = self.extract_links(resp.text, url)
            print(f"   Found {len(links)} links")
            
            # Check each link
            for link in links:
                # Skip if already checked
                if link in self.checked_urls:
                    continue
                
                self.checked_urls.add(link)
                
                # Check status
                status = self.check_url(link)
                
                if status == 404:
                    # Extract path for reporting
                    path = urlparse(link).path
                    self.missing_pages[path].append(url)
                    print(f"   ❌ 404: {path}")
                elif status == 200 or status in [301, 302]:
                    # Add to crawl queue if it's a page we haven't visited
                    if link not in self.visited and link not in self.to_visit:
                        self.to_visit.append(link)
                
                # Rate limiting
                time.sleep(0.05)
            
            return True
        
        except Exception as e:
            print(f"   ❌ Error: {e}")
            return False
    
    def crawl(self, start_urls: List[str]):
        """Crawl the site starting from given URLs."""
        # Add start URLs to queue
        for url in start_urls:
            full_url = urljoin(self.base_url, url)
            self.to_visit.append(full_url)
        
        print(f"🚀 Starting crawl from {len(start_urls)} URL(s)...\n")
        
        # Crawl pages
        while self.to_visit and len(self.visited) < self.max_pages:
            url = self.to_visit.pop(0)
            self.crawl_page(url)
            time.sleep(0.1)  # Be nice to the dev server
        
        print(f"\n✅ Crawled {len(self.visited)} pages")
        print(f"✅ Checked {len(self.checked_urls)} unique URLs\n")
    
    def print_report(self):
        """Print a report of all missing pages."""
        print("=" * 80)
        print("📊 MISSING PAGES REPORT")
        print("=" * 80)
        
        if not self.missing_pages:
            print("\n🎉 No missing pages found! All internal links are working.\n")
            return
        
        print(f"\n❌ Found {len(self.missing_pages)} missing pages:\n")
        
        # Sort by number of references (most linked to first)
        sorted_missing = sorted(
            self.missing_pages.items(),
            key=lambda x: len(x[1]),
            reverse=True
        )
        
        for missing_path, referrers in sorted_missing:
            ref_count = len(referrers)
            print(f"❌ {missing_path}")
            print(f"   Referenced by {ref_count} page(s):")
            
            # Show first 5 referrers
            for i, ref_url in enumerate(referrers[:5], 1):
                ref_path = urlparse(ref_url).path
                print(f"      {i}. {ref_path}")
            
            if len(referrers) > 5:
                print(f"      ... and {len(referrers) - 5} more")
            
            print()
        
        print("=" * 80)
    
    def save_slug_list(self, output_file: str):
        """Save a list of missing slugs to a text file."""
        if not self.missing_pages:
            print("No missing pages to save.")
            return
        
        # Extract slugs from paths
        slugs = []
        for path in self.missing_pages.keys():
            # Remove leading slash and /research/ prefix if present
            slug = path.lstrip('/')
            if slug.startswith('research/'):
                slug = slug[9:]  # Remove 'research/'
            
            if slug and slug not in ['assets', 's']:  # Skip non-content paths
                slugs.append(slug)
        
        # Sort by most referenced
        slugs_sorted = sorted(
            slugs,
            key=lambda s: len(self.missing_pages.get(f"/{s}", []) + self.missing_pages.get(f"/research/{s}", [])),
            reverse=True
        )
        
        output_path = BASE_DIR / "jobs" / "reports" / output_file
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w') as f:
            f.write("# Missing Pages - Import Priority List\n")
            f.write(f"# Found {len(slugs_sorted)} missing pages\n")
            f.write("# Listed by number of references (most linked to first)\n\n")
            
            for slug in slugs_sorted:
                # Count references
                ref_count = len(self.missing_pages.get(f"/{slug}", []) + 
                              self.missing_pages.get(f"/research/{slug}", []))
                f.write(f"{slug}\t# {ref_count} references\n")
        
        print(f"\n💾 Missing slugs saved to: {output_path}")
        print(f"   Import these webarchives to fix broken links!\n")


def main():
    parser = argparse.ArgumentParser(description='Find missing pages on the local dev site')
    parser.add_argument('--base-url', default='http://localhost:4321',
                       help='Base URL of the dev server')
    parser.add_argument('--start-urls', default='/',
                       help='Comma-separated list of URLs to start crawling from')
    parser.add_argument('--max-pages', type=int, default=500,
                       help='Maximum number of pages to crawl')
    parser.add_argument('--output', default='missing-pages-to-import.txt',
                       help='Output file for missing slugs list')
    
    args = parser.parse_args()
    
    # Parse start URLs
    start_urls = [url.strip() for url in args.start_urls.split(',')]
    
    crawler = SiteCrawler(base_url=args.base_url, max_pages=args.max_pages)
    
    # Crawl
    crawler.crawl(start_urls)
    
    # Print report
    crawler.print_report()
    
    # Save list
    crawler.save_slug_list(args.output)
    
    return 0


if __name__ == '__main__':
    exit(main())


