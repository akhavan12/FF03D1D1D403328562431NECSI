#!/usr/bin/env python3
"""
Ingest all webarchive files from the new_links folder to fix broken links.

This script:
1. Finds all .webarchive files in incoming/new_links/
2. Ingests them using the NECSI factory CLI
3. Builds them to BUILT state
4. Reports on success/failure
"""

import subprocess
import sys
from pathlib import Path
from typing import List, Tuple

BASE_DIR = Path(__file__).resolve().parents[1]
CLI_SCRIPT = BASE_DIR / "necsifactory" / "cli.py"
NEW_LINKS_DIR = BASE_DIR / "incoming" / "new_links"

def get_webarchive_files() -> List[Path]:
    """Get all webarchive files from new_links directory."""
    if not NEW_LINKS_DIR.exists():
        print(f"❌ Directory not found: {NEW_LINKS_DIR}")
        return []
    
    webarchives = list(NEW_LINKS_DIR.glob("*.webarchive"))
    print(f"📦 Found {len(webarchives)} webarchive files")
    return sorted(webarchives)

def ingest_webarchive(webarchive_path: Path) -> Tuple[bool, str]:
    """Ingest a single webarchive file."""
    print(f"🔄 Ingesting: {webarchive_path.name}")
    
    try:
        # Run the CLI command to ingest and build the webarchive
        result = subprocess.run([
            sys.executable, str(CLI_SCRIPT), "ingest", 
            "--webarchive", str(webarchive_path),
            "--build"
        ], capture_output=True, text=True, cwd=BASE_DIR, timeout=300)
        
        if result.returncode == 0:
            print(f"✅ Successfully ingested: {webarchive_path.name}")
            return True, "Success"
        else:
            error_msg = result.stderr.strip() or result.stdout.strip()
            print(f"❌ Failed to ingest {webarchive_path.name}: {error_msg}")
            return False, error_msg
            
    except subprocess.TimeoutExpired:
        error_msg = "Timeout after 5 minutes"
        print(f"⏰ Timeout ingesting {webarchive_path.name}")
        return False, error_msg
    except Exception as e:
        error_msg = str(e)
        print(f"❌ Error ingesting {webarchive_path.name}: {e}")
        return False, error_msg

def main():
    """Main function to ingest all webarchives."""
    print("🚀 Starting bulk ingestion of new webarchives...")
    print("=" * 80)
    
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
        print(f"\\n📄 Processing {i}/{len(webarchives)}: {webarchive_path.name}")
        
        success, message = ingest_webarchive(webarchive_path)
        
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
    print("📊 INGESTION SUMMARY")
    print("=" * 80)
    
    print(f"\\n✅ Successfully ingested: {len(results['success'])}")
    print(f"❌ Failed to ingest: {len(results['failed'])}")
    print(f"📈 Success rate: {len(results['success'])/len(webarchives)*100:.1f}%")
    
    if results['failed']:
        print(f"\\n❌ FAILED INGESTIONS:")
        for filename, error in results['failed'][:10]:  # Show first 10
            print(f"   • {filename}")
            print(f"     Error: {error}")
        if len(results['failed']) > 10:
            print(f"   ... and {len(results['failed']) - 10} more")
    
    # Save detailed report
    report_path = BASE_DIR / "jobs" / "reports" / "ingestion-results.txt"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("# Webarchive Ingestion Results\\n")
        f.write(f"# Total files: {len(webarchives)}\\n")
        f.write(f"# Successful: {len(results['success'])}\\n")
        f.write(f"# Failed: {len(results['failed'])}\\n")
        f.write(f"# Success rate: {len(results['success'])/len(webarchives)*100:.1f}%\\n\\n")
        
        f.write("## SUCCESSFUL INGESTIONS\\n\\n")
        for filename, message in results['success']:
            f.write(f"- {filename}\\n")
        
        f.write("\\n## FAILED INGESTIONS\\n\\n")
        for filename, error in results['failed']:
            f.write(f"- {filename}\\n")
            f.write(f"  Error: {error}\\n\\n")
    
    print(f"\\n💾 Detailed report saved: {report_path}")
    
    if len(results['success']) > 0:
        print(f"\\n🎉 Successfully ingested {len(results['success'])} webarchives!")
        print("   Next steps:")
        print("   1. Run link checker: python scripts/check_internal_links.py")
        print("   2. Check Astro site structure")
        print("   3. Fix remaining broken links")
    
    return 0 if len(results['failed']) == 0 else 1

if __name__ == "__main__":
    exit(main())
