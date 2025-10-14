#!/usr/bin/env python3
"""
Build all ingested content to BUILT state to fix broken links.

This script:
1. Finds all ingested content (INGESTED state)
2. Builds them to BUILT state using correct CLI syntax
3. Reports on success/failure
"""

import json
import subprocess
import sys
from pathlib import Path
from typing import List, Tuple

BASE_DIR = Path(__file__).resolve().parents[1]
CONTENT_DIR = BASE_DIR / "content"
VENV_PYTHON = BASE_DIR / ".venv" / "bin" / "python"

def get_ingested_content() -> List[str]:
    """Get all content that has been ingested but not built."""
    ingested_slugs = []
    
    for content_file in CONTENT_DIR.rglob("content.json"):
        try:
            with open(content_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            slug = data.get('slug')
            if slug:
                # Check if there's a state file indicating it's ingested
                state_file = content_file.parent / "state.json"
                if state_file.exists():
                    try:
                        with open(state_file, 'r', encoding='utf-8') as f:
                            state_data = json.load(f)
                        current_state = state_data.get('state', '')
                        
                        # If it's INGESTED but not BUILT, add to list
                        if current_state == 'INGESTED':
                            ingested_slugs.append(slug)
                    except:
                        # If no state file or error reading, assume it needs building
                        ingested_slugs.append(slug)
                else:
                    # No state file, assume it needs building
                    ingested_slugs.append(slug)
                    
        except Exception as e:
            print(f"⚠️  Error reading {content_file}: {e}")
    
    return ingested_slugs

def build_content(slug: str) -> Tuple[bool, str]:
    """Build a single content item to BUILT state."""
    print(f"🔄 Building: {slug}")
    
    try:
        # Use correct CLI syntax: run SLUG --to BUILT
        result = subprocess.run([
            str(VENV_PYTHON), "-m", "necsifactory.cli", "run",
            slug,
            "--to", "BUILT"
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
    """Main function to build all ingested content."""
    print("🚀 Building all ingested content to BUILT state...")
    print("=" * 80)
    
    # Check if virtual environment exists
    if not VENV_PYTHON.exists():
        print(f"❌ Virtual environment not found: {VENV_PYTHON}")
        return 1
    
    # Get all content that needs building
    content_slugs = get_ingested_content()
    print(f"📋 Found {len(content_slugs)} content items to build")
    
    if not content_slugs:
        print("❌ No content found to build")
        return 1
    
    # Track results
    results = {
        'success': [],
        'failed': []
    }
    
    # Process each content item
    for i, slug in enumerate(content_slugs, 1):
        print(f"\\n📄 Building {i}/{len(content_slugs)}")
        
        success, message = build_content(slug)
        
        if success:
            results['success'].append((slug, message))
        else:
            results['failed'].append((slug, message))
        
        # Progress indicator
        if i % 10 == 0:
            print(f"\\n📊 Progress: {i}/{len(content_slugs)} processed")
            print(f"   ✅ Success: {len(results['success'])}")
            print(f"   ❌ Failed: {len(results['failed'])}")
    
    # Final report
    print("\\n" + "=" * 80)
    print("📊 BUILD SUMMARY")
    print("=" * 80)
    
    print(f"\\n✅ Successfully built: {len(results['success'])}")
    print(f"❌ Failed to build: {len(results['failed'])}")
    print(f"📈 Success rate: {len(results['success'])/len(content_slugs)*100:.1f}%")
    
    if results['failed']:
        print(f"\\n❌ FAILED BUILDS:")
        for slug, error in results['failed'][:10]:  # Show first 10
            print(f"   • {slug}")
            print(f"     Error: {error}")
        if len(results['failed']) > 10:
            print(f"   ... and {len(results['failed']) - 10} more")
    
    # Save detailed report
    report_path = BASE_DIR / "jobs" / "reports" / "build-results.txt"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("# Content Build Results\\n")
        f.write(f"# Total items: {len(content_slugs)}\\n")
        f.write(f"# Successful: {len(results['success'])}\\n")
        f.write(f"# Failed: {len(results['failed'])}\\n")
        f.write(f"# Success rate: {len(results['success'])/len(content_slugs)*100:.1f}%\\n\\n")
        
        f.write("## SUCCESSFUL BUILDS\\n\\n")
        for slug, message in results['success']:
            f.write(f"- {slug}\\n")
        
        f.write("\\n## FAILED BUILDS\\n\\n")
        for slug, error in results['failed']:
            f.write(f"- {slug}\\n")
            f.write(f"  Error: {error}\\n\\n")
    
    print(f"\\n💾 Detailed report saved: {report_path}")
    
    if len(results['success']) > 0:
        print(f"\\n🎉 Successfully built {len(results['success'])} content items!")
        print("   Next steps:")
        print("   1. Run link checker: python scripts/check_internal_links.py")
        print("   2. Check remaining broken links")
        print("   3. Fix Astro site structure")
    
    return 0 if len(results['failed']) == 0 else 1

if __name__ == "__main__":
    exit(main())
