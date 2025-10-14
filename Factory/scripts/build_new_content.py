#!/usr/bin/env python3
"""
Build the newly ingested content with --replace flag to fix broken links.

This script:
1. Gets the list of newly downloaded webarchives from new_links folder
2. Builds them with --replace flag to overwrite existing content
3. Reports on success/failure
"""

import json
import subprocess
import sys
from pathlib import Path
from typing import List, Tuple, Set

BASE_DIR = Path(__file__).resolve().parents[1]
CONTENT_DIR = BASE_DIR / "content"
NEW_LINKS_DIR = BASE_DIR / "incoming" / "new_links"
VENV_PYTHON = BASE_DIR / ".venv" / "bin" / "python"

def get_new_webarchive_slugs() -> Set[str]:
    """Get slugs from the newly downloaded webarchives."""
    new_slugs = set()
    
    if not NEW_LINKS_DIR.exists():
        print(f"❌ New links directory not found: {NEW_LINKS_DIR}")
        return new_slugs
    
    for webarchive_file in NEW_LINKS_DIR.glob("*.webarchive"):
        filename = webarchive_file.name
        
        # Extract slug from filename
        name = filename.replace('.webarchive', '')
        if " — New England Complex Systems Institute" in name:
            name = name.split(" — New England Complex Systems Institute")[0]
        
        # Convert to slug format
        import re
        slug = re.sub(r'[^\w\s-]', '', name)
        slug = re.sub(r'[-\s]+', '-', slug)
        slug = slug.lower().strip('-')
        
        new_slugs.add(slug)
    
    return new_slugs

def build_content_with_replace(slug: str) -> Tuple[bool, str]:
    """Build a single content item with --replace flag."""
    print(f"🔄 Building: {slug}")
    
    try:
        # Use --replace flag to overwrite existing content
        result = subprocess.run([
            str(VENV_PYTHON), "-m", "necsifactory.cli", "run",
            slug,
            "--to", "BUILT",
            "--replace"
        ], capture_output=True, text=True, cwd=BASE_DIR, timeout=120)
        
        if result.returncode == 0:
            print(f"✅ Successfully built: {slug}")
            return True, "Success"
        else:
            error_msg = result.stderr.strip() or result.stdout.strip()
            print(f"❌ Failed to build {slug}: {error_msg}")
            return False, error_msg
            
    except subprocess.TimeoutExpired:
        error_msg = "Timeout after 2 minutes"
        print(f"⏰ Timeout building {slug}")
        return False, error_msg
    except Exception as e:
        error_msg = str(e)
        print(f"❌ Error building {slug}: {e}")
        return False, error_msg

def main():
    """Main function to build new content."""
    print("🚀 Building newly downloaded content with --replace flag...")
    print("=" * 80)
    
    # Check if virtual environment exists
    if not VENV_PYTHON.exists():
        print(f"❌ Virtual environment not found: {VENV_PYTHON}")
        return 1
    
    # Get slugs from new webarchives
    new_slugs = get_new_webarchive_slugs()
    print(f"📋 Found {len(new_slugs)} new webarchive slugs to build")
    
    if not new_slugs:
        print("❌ No new webarchive slugs found")
        return 1
    
    # Track results
    results = {
        'success': [],
        'failed': []
    }
    
    # Process each slug
    for i, slug in enumerate(sorted(new_slugs), 1):
        print(f"\\n📄 Building {i}/{len(new_slugs)}")
        
        success, message = build_content_with_replace(slug)
        
        if success:
            results['success'].append((slug, message))
        else:
            results['failed'].append((slug, message))
        
        # Progress indicator
        if i % 10 == 0:
            print(f"\\n📊 Progress: {i}/{len(new_slugs)} processed")
            print(f"   ✅ Success: {len(results['success'])}")
            print(f"   ❌ Failed: {len(results['failed'])}")
    
    # Final report
    print("\\n" + "=" * 80)
    print("📊 NEW CONTENT BUILD SUMMARY")
    print("=" * 80)
    
    print(f"\\n✅ Successfully built: {len(results['success'])}")
    print(f"❌ Failed to build: {len(results['failed'])}")
    print(f"📈 Success rate: {len(results['success'])/len(new_slugs)*100:.1f}%")
    
    if results['failed']:
        print(f"\\n❌ FAILED BUILDS:")
        for slug, error in results['failed'][:10]:  # Show first 10
            print(f"   • {slug}")
            print(f"     Error: {error}")
        if len(results['failed']) > 10:
            print(f"   ... and {len(results['failed']) - 10} more")
    
    # Save detailed report
    report_path = BASE_DIR / "jobs" / "reports" / "new-content-build-results.txt"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("# New Content Build Results\\n")
        f.write(f"# Total new items: {len(new_slugs)}\\n")
        f.write(f"# Successful: {len(results['success'])}\\n")
        f.write(f"# Failed: {len(results['failed'])}\\n")
        f.write(f"# Success rate: {len(results['success'])/len(new_slugs)*100:.1f}%\\n\\n")
        
        f.write("## SUCCESSFUL BUILDS\\n\\n")
        for slug, message in results['success']:
            f.write(f"- {slug}\\n")
        
        f.write("\\n## FAILED BUILDS\\n\\n")
        for slug, error in results['failed']:
            f.write(f"- {slug}\\n")
            f.write(f"  Error: {error}\\n\\n")
    
    print(f"\\n💾 Detailed report saved: {report_path}")
    
    if len(results['success']) > 0:
        print(f"\\n🎉 Successfully built {len(results['success'])} new content items!")
        print("   This should significantly reduce broken links!")
        print("   Next steps:")
        print("   1. Run link checker: python scripts/check_internal_links.py")
        print("   2. Check remaining broken links")
    
    return 0 if len(results['failed']) == 0 else 1

if __name__ == "__main__":
    exit(main())
