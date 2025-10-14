#!/usr/bin/env python3
"""
Find all missing PDF files referenced in research content.

This script:
1. Scans all research content files
2. Extracts PDF links from the content
3. Checks if the PDF files exist in the assets directory
4. Generates a list of missing PDFs with their source pages
5. Creates download URLs for the missing PDFs
"""

import json
import re
from pathlib import Path
from typing import List, Dict, Set
from urllib.parse import urljoin

BASE_DIR = Path(__file__).resolve().parents[1]
CONTENT_DIR = BASE_DIR / "content"
ASSETS_DIR = BASE_DIR.parents[0] / "sites" / "necsi-site" / "public" / "assets"
MISSING_PDFS_REPORT = BASE_DIR / "jobs" / "reports" / "missing-pdfs-report.txt"
MISSING_PDFS_SIMPLE = BASE_DIR / "jobs" / "reports" / "missing-pdfs-simple.txt"
DOWNLOAD_URLS_FILE = BASE_DIR / "jobs" / "reports" / "pdf-download-urls.txt"

def find_pdf_links_in_content(content: str) -> List[str]:
    """Extract all PDF links from content."""
    pdf_links = []
    
    # Pattern to match markdown links to PDFs: [text](/s/filename.pdf)
    pdf_pattern = r'\[([^\]]+)\]\(([^)]+\.pdf)\)'
    matches = re.findall(pdf_pattern, content)
    
    for link_text, link_url in matches:
        # Only include /s/ directory PDFs (these are the ones we need to download)
        if link_url.startswith('/s/'):
            pdf_links.append(link_url)
    
    return pdf_links

def check_pdf_exists(pdf_path: str) -> bool:
    """Check if a PDF file exists in the assets directory."""
    # Convert /s/filename.pdf to assets/filename.pdf
    if pdf_path.startswith('/s/'):
        filename = pdf_path[3:]  # Remove '/s/'
        # Check if file exists in assets directory
        asset_file = ASSETS_DIR / filename
        return asset_file.exists()
    return False

def get_all_research_content() -> Dict[str, Dict]:
    """Get all research content files."""
    research_content = {}
    
    for content_file in CONTENT_DIR.rglob("content.json"):
        try:
            with open(content_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            if data.get('type') == 'research':
                slug = data.get('slug')
                if slug:
                    research_content[slug] = {
                        'title': data.get('title', ''),
                        'content': data.get('narrative_md', ''),
                        'source_url': data.get('provenance', {}).get('source_url', '')
                    }
        except Exception as e:
            print(f"⚠️  Error reading {content_file}: {e}")
    
    return research_content

def find_missing_pdfs():
    """Find all missing PDF files and generate reports."""
    print("🔍 Scanning research content for PDF links...")
    
    research_content = get_all_research_content()
    print(f"📋 Found {len(research_content)} research content files")
    
    missing_pdfs = {}  # pdf_path -> list of pages that reference it
    existing_pdfs = set()
    total_pdf_links = 0
    
    for slug, content_data in research_content.items():
        content = content_data['content']
        title = content_data['title']
        source_url = content_data['source_url']
        
        # Find PDF links in this content
        pdf_links = find_pdf_links_in_content(content)
        total_pdf_links += len(pdf_links)
        
        for pdf_path in pdf_links:
            if check_pdf_exists(pdf_path):
                existing_pdfs.add(pdf_path)
            else:
                if pdf_path not in missing_pdfs:
                    missing_pdfs[pdf_path] = []
                missing_pdfs[pdf_path].append({
                    'slug': slug,
                    'title': title,
                    'source_url': source_url
                })
    
    print(f"\n📊 PDF ANALYSIS RESULTS")
    print("=" * 60)
    print(f"Total PDF links found: {total_pdf_links}")
    print(f"Existing PDFs: {len(existing_pdfs)}")
    print(f"Missing PDFs: {len(missing_pdfs)}")
    
    # Sort missing PDFs by number of references
    sorted_missing = sorted(
        missing_pdfs.items(),
        key=lambda x: len(x[1]),
        reverse=True
    )
    
    # Generate detailed report
    with open(MISSING_PDFS_REPORT, 'w', encoding='utf-8') as f_report, \
         open(MISSING_PDFS_SIMPLE, 'w', encoding='utf-8') as f_simple, \
         open(DOWNLOAD_URLS_FILE, 'w', encoding='utf-8') as f_urls:
        
        f_report.write("🔍 MISSING PDF FILES REPORT\n")
        f_report.write("=" * 60 + "\n\n")
        f_report.write(f"Total PDF links found: {total_pdf_links}\n")
        f_report.write(f"Existing PDFs: {len(existing_pdfs)}\n")
        f_report.write(f"Missing PDFs: {len(missing_pdfs)}\n\n")
        
        f_report.write("📋 MISSING PDFS (sorted by number of references):\n")
        f_report.write("-" * 60 + "\n\n")
        
        f_urls.write("# Download URLs for missing PDF files\n")
        f_urls.write("# Copy these URLs and download the PDFs to Factory/incoming/pdfs/\n\n")
        
        for i, (pdf_path, references) in enumerate(sorted_missing):
            pdf_filename = pdf_path[3:]  # Remove '/s/'
            
            print(f"{i+1:3d}. {pdf_filename}")
            print(f"     Referenced by: {len(references)} pages")
            
            f_report.write(f"{i+1:3d}. {pdf_path}\n")
            f_report.write(f"     Filename: {pdf_filename}\n")
            f_report.write(f"     Referenced by: {len(references)} pages\n")
            f_report.write("     Pages:\n")
            
            # Generate download URL (assuming necsi.edu structure)
            download_url = f"https://necsi.edu{pdf_path}"
            f_urls.write(f"{download_url}\n")
            
            for ref in references[:5]:  # Show first 5 references
                print(f"       • {ref['title'][:60]}...")
                f_report.write(f"       • {ref['slug']}: {ref['title']}\n")
            
            if len(references) > 5:
                print(f"       ... and {len(references) - 5} more")
                f_report.write(f"       ... and {len(references) - 5} more pages\n")
            
            print()
            f_report.write("\n")
        
        # Write simple list for easy copying
        f_simple.write("# Missing PDF filenames (one per line)\n")
        for pdf_path, _ in sorted_missing:
            pdf_filename = pdf_path[3:]  # Remove '/s/'
            f_simple.write(f"{pdf_filename}\n")
    
    print(f"\n💾 Reports saved:")
    print(f"   📄 Detailed report: {MISSING_PDFS_REPORT}")
    print(f"   📝 Simple list: {MISSING_PDFS_SIMPLE}")
    print(f"   🔗 Download URLs: {DOWNLOAD_URLS_FILE}")
    
    print(f"\n🚀 Next steps:")
    print(f"   1. Download PDFs using the URLs in: {DOWNLOAD_URLS_FILE}")
    print(f"   2. Save them to: Factory/incoming/pdfs/")
    print(f"   3. Run the PDF processing script to organize them")

if __name__ == "__main__":
    find_missing_pdfs()
