#!/usr/bin/env python3
"""
Generate necsi.edu URLs for missing content files so they can be downloaded
as webarchives and imported to fix broken links.

This script:
1. Reads the missing content list
2. Generates proper necsi.edu URLs for each missing file
3. Creates a prioritized download list
4. Generates a script to help with bulk downloading
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Tuple
from urllib.parse import urljoin

BASE_DIR = Path(__file__).resolve().parents[1]
MISSING_SLUGS_FILE = BASE_DIR / "jobs" / "reports" / "missing-slugs-simple.txt"
LINK_REPORT_FILE = BASE_DIR / "jobs" / "reports" / "link-check-report.json"

# Base URL for NECSI website
NECSI_BASE_URL = "https://necsi.edu"

def load_missing_slugs() -> List[str]:
    """Load the list of missing slugs."""
    if not MISSING_SLUGS_FILE.exists():
        print(f"❌ Missing slugs file not found: {MISSING_SLUGS_FILE}")
        return []
    
    with open(MISSING_SLUGS_FILE, 'r', encoding='utf-8') as f:
        return [line.strip() for line in f if line.strip()]

def load_link_references() -> Dict[str, int]:
    """Load how many times each missing link is referenced."""
    if not LINK_REPORT_FILE.exists():
        return {}
    
    with open(LINK_REPORT_FILE, 'r', encoding='utf-8') as f:
        report = json.load(f)
    
    # Count references for each broken link
    link_counts = {}
    for page in report.get('broken_links', []):
        for broken in page.get('broken_links', []):
            link = broken['link']
            if link not in link_counts:
                link_counts[link] = 0
            link_counts[link] += 1
    
    return link_counts

def generate_url_for_slug(slug: str) -> str:
    """Generate the necsi.edu URL for a given slug."""
    # Clean up the slug
    slug = slug.strip()
    
    # Handle special cases
    if slug == "yaneer-bar-yam":
        return f"{NECSI_BASE_URL}/yaneer-bar-yam"
    elif slug == "hiroki-tasaka":
        return f"{NECSI_BASE_URL}/hiroki-tasaka"
    elif slug == "engage-1":
        return f"{NECSI_BASE_URL}/engage"
    elif slug == "winter-school":
        return f"{NECSI_BASE_URL}/winter-school"
    elif slug == "about":
        return f"{NECSI_BASE_URL}/about"
    elif slug == "search":
        return f"{NECSI_BASE_URL}/search"
    elif slug == "current-students":
        return f"{NECSI_BASE_URL}/current-students"
    elif slug == "academics":
        return f"{NECSI_BASE_URL}/academics"
    elif slug == "graduate-programs":
        return f"{NECSI_BASE_URL}/graduate-programs"
    elif slug == "admissions":
        return f"{NECSI_BASE_URL}/admissions"
    elif slug == "libraries":
        return f"{NECSI_BASE_URL}/libraries"
    elif slug == "opportunities-for-students":
        return f"{NECSI_BASE_URL}/opportunities-for-students"
    elif slug == "student-experience":
        return f"{NECSI_BASE_URL}/student-experience"
    elif slug == "student-life-arts":
        return f"{NECSI_BASE_URL}/student-life/arts"
    elif slug == "about-mission-vision":
        return f"{NECSI_BASE_URL}/about/mission-vision"
    elif slug == "about-university-leadership":
        return f"{NECSI_BASE_URL}/about/university-leadership"
    elif slug == "president":
        return f"{NECSI_BASE_URL}/president"
    elif slug == "about-offices-and-services":
        return f"{NECSI_BASE_URL}/about/offices-and-services"
    elif slug == "about-contact-us":
        return f"{NECSI_BASE_URL}/about/contact-us"
    elif slug == "about-privacy":
        return f"{NECSI_BASE_URL}/about/privacy"
    
    # Handle research pages
    if slug.startswith("research-"):
        # Remove "research-" prefix and use /research/ path
        research_slug = slug[9:]  # Remove "research-"
        return f"{NECSI_BASE_URL}/research/{research_slug}"
    
    # Handle wiki pages
    if slug.startswith("wiki/"):
        return f"{NECSI_BASE_URL}/{slug}"
    
    # Handle radio pages
    if slug.startswith("radio/"):
        return f"{NECSI_BASE_URL}/{slug}"
    
    # Handle about pages
    if slug.startswith("about/"):
        return f"{NECSI_BASE_URL}/{slug}"
    
    # Handle academic pages
    if slug.startswith("academics/"):
        return f"{NECSI_BASE_URL}/{slug}"
    
    if slug.startswith("admissions/"):
        return f"{NECSI_BASE_URL}/{slug}"
    
    if slug.startswith("student-life/"):
        return f"{NECSI_BASE_URL}/{slug}"
    
    # Default: assume it's a research page
    return f"{NECSI_BASE_URL}/research/{slug}"

def create_download_script(urls_with_priority: List[Tuple[str, str, int]]):
    """Create a script to help with downloading webarchives."""
    
    script_content = f"""#!/usr/bin/env python3
'''
Auto-generated script to download missing content from necsi.edu as webarchives.

This script contains {len(urls_with_priority)} URLs to download.
Priority is based on number of broken link references.

Usage:
1. Install Safari or use a web browser that can save as .webarchive
2. Open each URL and save as .webarchive in Factory/incoming/
3. Or use this script as a reference for manual downloading

Priority order (most referenced first):
'''

import webbrowser
import time
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
INCOMING_DIR = BASE_DIR / "incoming"

# URLs to download (sorted by priority)
URLS_TO_DOWNLOAD = [
"""
    
    for i, (slug, url, ref_count) in enumerate(urls_with_priority, 1):
        script_content += f'    ("{slug}", "{url}", {ref_count}),  # Priority {i}\n'
    
    script_content += """]

def open_urls_in_browser():
    '''Open all URLs in the default browser for manual downloading.'''
    print(f"🌐 Opening {len(URLS_TO_DOWNLOAD)} URLs in browser...")
    print("📋 Instructions:")
    print("   1. For each URL that opens:")
    print("   2. Save the page as .webarchive")
    print("   3. Save to Factory/incoming/ directory")
    print("   4. Use filename format: 'Page Title — New England Complex Systems Institute.webarchive'")
    print("   5. Press Enter to continue to next URL")
    print()
    
    for i, (slug, url, ref_count) in enumerate(URLS_TO_DOWNLOAD, 1):
        print(f"📄 {i}/{len(URLS_TO_DOWNLOAD)}: {slug}")
        print(f"   URL: {url}")
        print(f"   References: {ref_count} broken links")
        print(f"   Opening in browser...")
        
        webbrowser.open(url)
        
        # Wait for user input
        input("   Press Enter when you've saved this page as .webarchive...")
        print()

def print_url_list():
    '''Print all URLs for manual copying.'''
    print("📋 ALL URLs TO DOWNLOAD:")
    print("=" * 80)
    
    for i, (slug, url, ref_count) in enumerate(URLS_TO_DOWNLOAD, 1):
        print(f"{i:3d}. {slug}")
        print(f"     {url}")
        print(f"     References: {ref_count}")
        print()

def main():
    '''Main function.'''
    print("🚀 NECSI Missing Content Download Helper")
    print("=" * 80)
    print(f"📊 Total URLs to download: {len(URLS_TO_DOWNLOAD)}")
    print()
    
    choice = input("Choose option:\\n1. Open URLs in browser (one by one)\\n2. Print all URLs\\n3. Exit\\nChoice (1-3): ")
    
    if choice == "1":
        open_urls_in_browser()
    elif choice == "2":
        print_url_list()
    else:
        print("👋 Goodbye!")

if __name__ == "__main__":
    main()
"""
    
    # Save the download script
    script_path = BASE_DIR / "scripts" / "download_missing_content.py"
    with open(script_path, 'w', encoding='utf-8') as f:
        f.write(script_content)
    
    return script_path

def main():
    """Main function."""
    print("🔗 Generating necsi.edu URLs for missing content files...")
    
    # Load missing slugs
    missing_slugs = load_missing_slugs()
    if not missing_slugs:
        return
    
    print(f"📋 Found {len(missing_slugs)} missing content files")
    
    # Load link references for priority
    link_counts = load_link_references()
    
    # Generate URLs and calculate priority
    urls_with_priority = []
    for slug in missing_slugs:
        url = generate_url_for_slug(slug)
        
        # Calculate priority based on references
        ref_count = 0
        # Check various link formats
        for link_format in [f"/{slug}", f"/research/{slug}"]:
            ref_count += link_counts.get(link_format, 0)
        
        urls_with_priority.append((slug, url, ref_count))
    
    # Sort by priority (most referenced first)
    urls_with_priority.sort(key=lambda x: x[2], reverse=True)
    
    print(f"\\n🎯 GENERATED DOWNLOAD URLs")
    print("=" * 80)
    
    # Show top 20 URLs
    print("📊 TOP 20 PRIORITY URLs (most referenced first):")
    for i, (slug, url, ref_count) in enumerate(urls_with_priority[:20], 1):
        print(f"{i:2d}. {slug}")
        print(f"    {url}")
        print(f"    References: {ref_count} broken links")
        print()
    
    # Create download script
    script_path = create_download_script(urls_with_priority)
    print(f"💾 Download helper script created: {script_path}")
    
    # Save URL list to file
    url_list_path = BASE_DIR / "jobs" / "reports" / "download-urls.txt"
    with open(url_list_path, 'w', encoding='utf-8') as f:
        f.write("# NECSI Missing Content Download URLs\\n")
        f.write(f"# Generated for {len(urls_with_priority)} missing content files\\n")
        f.write("# Priority order (most referenced first)\\n\\n")
        
        for i, (slug, url, ref_count) in enumerate(urls_with_priority, 1):
            f.write(f"{i:3d}. {slug}\\n")
            f.write(f"     URL: {url}\\n")
            f.write(f"     References: {ref_count}\\n\\n")
    
    print(f"📄 URL list saved: {url_list_path}")
    
    # Save simple URL list for bulk processing
    simple_urls_path = BASE_DIR / "jobs" / "reports" / "urls-simple.txt"
    with open(simple_urls_path, 'w', encoding='utf-8') as f:
        for slug, url, ref_count in urls_with_priority:
            f.write(f"{url}\\n")
    
    print(f"📝 Simple URL list saved: {simple_urls_path}")
    
    print(f"\\n🚀 NEXT STEPS:")
    print(f"1. Run the download helper: python {script_path}")
    print(f"2. Or manually copy URLs from: {url_list_path}")
    print(f"3. Download each URL as .webarchive to Factory/incoming/")
    print(f"4. Run: python scripts/import_missing_content.py")
    print(f"5. Check results: python scripts/check_internal_links.py")

if __name__ == "__main__":
    main()
