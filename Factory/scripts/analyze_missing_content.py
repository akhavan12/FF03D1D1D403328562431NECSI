#!/usr/bin/env python3
"""
Analyze broken links to identify which content files are completely missing
and need to be downloaded/imported from webarchives.

This script:
1. Reads the link check report
2. Categorizes broken links by type
3. Identifies which are missing content files vs. path issues
4. Creates a prioritized list for import
"""

import json
import re
from pathlib import Path
from collections import defaultdict
from typing import Dict, List, Set

BASE_DIR = Path(__file__).resolve().parents[1]
CONTENT_DIR = BASE_DIR / "content"
REPORT_FILE = BASE_DIR / "jobs" / "reports" / "link-check-report.json"

def get_existing_slugs() -> Set[str]:
    """Get all existing content slugs."""
    slugs = set()
    for content_file in CONTENT_DIR.rglob("content.json"):
        try:
            with open(content_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                slug = data.get('slug')
                if slug:
                    slugs.add(slug)
                    slugs.add(f"/{slug}")
                    slugs.add(f"/research/{slug}")
        except Exception as e:
            print(f"⚠️  Error reading {content_file}: {e}")
    return slugs

def normalize_link(link: str) -> str:
    """Normalize a link for comparison."""
    # Remove anchor and query params
    if '#' in link:
        link = link.split('#')[0]
    if '?' in link:
        link = link.split('?')[0]
    
    # Remove trailing slash
    link = link.rstrip('/')
    
    # Ensure leading slash
    if link and not link.startswith('/'):
        link = f"/{link}"
    
    return link

def categorize_broken_links(broken_links: List[Dict], existing_slugs: Set[str]) -> Dict[str, List[str]]:
    """Categorize broken links by type."""
    categories = {
        'missing_content': [],      # Content files that don't exist
        'asset_files': [],          # PDFs, images, etc.
        'path_issues': [],          # Links that might work with path fixes
        'external_links': [],       # External URLs that got misclassified
        'duplicate_links': []       # Links that exist but are duplicated
    }
    
    for page in broken_links:
        for broken in page['broken_links']:
            link = broken['link']
            normalized = broken['normalized']
            
            # Skip external URLs
            if link.startswith(('http://', 'https://', 'www.', 'mailto:')):
                categories['external_links'].append(link)
                continue
            
            # Asset files (PDFs, images, etc.)
            if (link.startswith('/s/') or 
                link.endswith(('.pdf', '.jpg', '.png', '.gif', '.mp3', '.docx')) or
                '/assets/' in link):
                categories['asset_files'].append(link)
                continue
            
            # Check if it's a path issue (exists with different path)
            potential_paths = [
                normalized,
                normalized.lstrip('/'),
                f"/research{normalized}",
                f"/research/{normalized.lstrip('/')}"
            ]
            
            found_path = False
            for path in potential_paths:
                if path in existing_slugs:
                    categories['path_issues'].append(f"{link} -> {path}")
                    found_path = True
                    break
            
            if not found_path:
                # This is likely a missing content file
                categories['missing_content'].append(link)
    
    return categories

def analyze_missing_content():
    """Main analysis function."""
    print("🔍 Analyzing missing content files...")
    
    # Load the link check report
    if not REPORT_FILE.exists():
        print(f"❌ Report file not found: {REPORT_FILE}")
        print("   Run: python scripts/check_internal_links.py --save-report")
        return
    
    with open(REPORT_FILE, 'r', encoding='utf-8') as f:
        report = json.load(f)
    
    # Get existing slugs
    existing_slugs = get_existing_slugs()
    print(f"✅ Found {len(existing_slugs)} existing content slugs")
    
    # Categorize broken links
    broken_links = report.get('broken_links', [])
    categories = categorize_broken_links(broken_links, existing_slugs)
    
    print(f"\n📊 BROKEN LINK ANALYSIS")
    print("=" * 80)
    
    for category, links in categories.items():
        print(f"\n{category.upper().replace('_', ' ')}: {len(links)}")
        if links:
            for link in links[:10]:  # Show first 10
                print(f"  • {link}")
            if len(links) > 10:
                print(f"  ... and {len(links) - 10} more")
    
    # Focus on missing content
    missing_content = categories['missing_content']
    if missing_content:
        print(f"\n🎯 MISSING CONTENT FILES TO IMPORT: {len(missing_content)}")
        print("=" * 80)
        
        # Group by likely webarchive names
        webarchive_candidates = defaultdict(list)
        
        for link in missing_content:
            # Extract potential slug from link
            slug = link.lstrip('/')
            if slug.startswith('research/'):
                slug = slug[9:]  # Remove 'research/'
            
            # Clean up the slug
            slug = slug.replace('/', '-')
            webarchive_candidates[slug].append(link)
        
        # Sort by number of references
        sorted_candidates = sorted(
            webarchive_candidates.items(),
            key=lambda x: len(x[1]),
            reverse=True
        )
        
        print("\n📋 PRIORITY LIST FOR WEBARCHIVE IMPORT:")
        print("(Most referenced missing pages first)")
        print()
        
        for i, (slug, links) in enumerate(sorted_candidates[:20], 1):
            print(f"{i:2d}. {slug}")
            print(f"    Referenced by: {len(links)} links")
            for link in links[:3]:  # Show first 3 references
                print(f"       • {link}")
            if len(links) > 3:
                print(f"       ... and {len(links) - 3} more")
            print()
        
        # Save to file
        output_file = BASE_DIR / "jobs" / "reports" / "missing-content-to-import.txt"
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("# Missing Content Files - Import Priority List\n")
            f.write(f"# Found {len(missing_content)} missing content files\n")
            f.write("# Listed by number of references (most linked to first)\n\n")
            
            for slug, links in sorted_candidates:
                f.write(f"{slug}\t# {len(links)} references\n")
                for link in links:
                    f.write(f"#   -> {link}\n")
                f.write("\n")
        
        print(f"💾 Full list saved to: {output_file}")
        
        # Also create a simple list for bulk import
        simple_list_file = BASE_DIR / "jobs" / "reports" / "missing-slugs-simple.txt"
        with open(simple_list_file, 'w', encoding='utf-8') as f:
            for slug, _ in sorted_candidates:
                f.write(f"{slug}\n")
        
        print(f"📝 Simple slug list saved to: {simple_list_file}")
    
    else:
        print("\n✅ No missing content files found!")
        print("   All broken links appear to be path issues or asset files.")

if __name__ == "__main__":
    analyze_missing_content()
