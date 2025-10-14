#!/usr/bin/env python3
"""
Ingest all new webarchive files and build them to fix broken links.

This script:
1. Finds all .webarchive files in incoming/
2. Ingests them using the NECSI factory CLI with virtual environment
3. Builds them to BUILT state
4. Reports on success/failure
"""

import subprocess
import sys
from pathlib import Path
from typing import List, Tuple

BASE_DIR = Path(__file__).resolve().parents[1]
INCOMING_DIR = BASE_DIR / "incoming"
VENV_PYTHON = BASE_DIR / ".venv" / "bin" / "python"

def get_webarchive_files() -> List[Path]:
    """Get all webarchive files from incoming directory."""
    if not INCOMING_DIR.exists():
        print(f"❌ Directory not found: {INCOMING_DIR}")
        return []
    
    webarchives = list(INCOMING_DIR.glob("*.webarchive"))
    print(f"📦 Found {len(webarchives)} webarchive files")
    return sorted(webarchives)

def extract_slug_from_filename(filename: str) -> str:
    """Extract slug from webarchive filename."""
    # Remove .webarchive extension
    name = filename.replace('.webarchive', '')
    
    # Remove " — New England Complex Systems Institute" suffix
    if " — New England Complex Systems Institute" in name:
        name = name.split(" — New England Complex Systems Institute")[0]
    
    # Convert to slug format
    import re
    slug = re.sub(r'[^\w\s-]', '', name)
    slug = re.sub(r'[-\s]+', '-', slug)
    slug = slug.lower().strip('-')
    
    return slug

def ingest_and_build_webarchive(webarchive_path: Path) -> Tuple[bool, str]:
    """Ingest and build a single webarchive file."""
    filename = webarchive_path.name
    slug = extract_slug_from_filename(filename)
    
    print(f"🔄 Processing: {filename}")
    print(f"   Slug: {slug}")
    
    try:
        # Step 1: Ingest
        ingest_result = subprocess.run([
            str(VENV_PYTHON), "-m", "necsifactory.cli", "ingest", 
            "--add", str(webarchive_path),
            "--slug", slug
        ], capture_output=True, text=True, cwd=BASE_DIR, timeout=60)
        
        if ingest_result.returncode != 0:
            error_msg = ingest_result.stderr.strip() or ingest_result.stdout.strip()
            print(f"❌ Failed to ingest {filename}: {error_msg}")
            return False, f"Ingest failed: {error_msg}"
        
        print(f"   ✅ Ingested successfully")
        
        # Step 2: Build
        build_result = subprocess.run([
            str(VENV_PYTHON), "-m", "necsifactory.cli", "run",
            "--slug", slug,
            "--target-state", "BUILT"
        ], capture_output=True, text=True, cwd=BASE_DIR, timeout=120)
        
        if build_result.returncode != 0:
            error_msg = build_result.stderr.strip() or build_result.stdout.strip()
            print(f"❌ Failed to build {filename}: {error_msg}")
            return False, f"Build failed: {error_msg}"
        
        print(f"   ✅ Built successfully")
        return True, "Success"
        
    except subprocess.TimeoutExpired:
        error_msg = "Timeout"
        print(f"⏰ Timeout processing {filename}")
        return False, error_msg
    except Exception as e:
        error_msg = str(e)
        print(f"❌ Error processing {filename}: {e}")
        return False, error_msg

def main():
    """Main function to ingest and build all webarchives."""
    print("🚀 Starting bulk ingestion and building of webarchives...")
    print("=" * 80)
    
    # Check if virtual environment exists
    if not VENV_PYTHON.exists():
        print(f"❌ Virtual environment not found: {VENV_PYTHON}")
        return 1
    
    # Get all webarchive files
    webarchives = get_webarchive_files()
    if not webarchives:
        print("❌ No webarchive files found to ingest")
        return 1
    
    # Track results
    results = {
        'success': [],
        'failed': []
    }
    
    # Process each webarchive
    for i, webarchive_path in enumerate(webarchives, 1):
        print(f"\\n📄 Processing {i}/{len(webarchives)}")
        
        success, message = ingest_and_build_webarchive(webarchive_path)
        
        if success:
            results['success'].append((webarchive_path.name, message))
        else:
            results['failed'].append((webarchive_path.name, message))
        
        # Progress indicator
        if i % 10 == 0:
            print(f"\\n📊 Progress: {i}/{len(webarchives)} processed")
            print(f"   ✅ Success: {len(results['success'])}")
            print(f"   ❌ Failed: {len(results['failed'])}")
    
    # Final report
    print("\\n" + "=" * 80)
    print("📊 INGESTION & BUILD SUMMARY")
    print("=" * 80)
    
    print(f"\\n✅ Successfully processed: {len(results['success'])}")
    print(f"❌ Failed to process: {len(results['failed'])}")
    print(f"📈 Success rate: {len(results['success'])/len(webarchives)*100:.1f}%")
    
    if results['failed']:
        print(f"\\n❌ FAILED PROCESSING:")
        for filename, error in results['failed'][:10]:  # Show first 10
            print(f"   • {filename}")
            print(f"     Error: {error}")
        if len(results['failed']) > 10:
            print(f"   ... and {len(results['failed']) - 10} more")
    
    # Save detailed report
    report_path = BASE_DIR / "jobs" / "reports" / "bulk-ingestion-results.txt"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("# Bulk Webarchive Ingestion & Build Results\\n")
        f.write(f"# Total files: {len(webarchives)}\\n")
        f.write(f"# Successful: {len(results['success'])}\\n")
        f.write(f"# Failed: {len(results['failed'])}\\n")
        f.write(f"# Success rate: {len(results['success'])/len(webarchives)*100:.1f}%\\n\\n")
        
        f.write("## SUCCESSFUL PROCESSING\\n\\n")
        for filename, message in results['success']:
            f.write(f"- {filename}\\n")
        
        f.write("\\n## FAILED PROCESSING\\n\\n")
        for filename, error in results['failed']:
            f.write(f"- {filename}\\n")
            f.write(f"  Error: {error}\\n\\n")
    
    print(f"\\n💾 Detailed report saved: {report_path}")
    
    if len(results['success']) > 0:
        print(f"\\n🎉 Successfully processed {len(results['success'])} webarchives!")
        print("   Next steps:")
        print("   1. Run link checker: python scripts/check_internal_links.py")
        print("   2. Fix Astro site structure to match original website")
        print("   3. Check remaining broken links")
    
    return 0 if len(results['failed']) == 0 else 1

if __name__ == "__main__":
    exit(main())
