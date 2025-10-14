#!/usr/bin/env python3
"""
Match missing content files with available webarchive files and create
a prioritized import list.

This script:
1. Reads the missing content list
2. Matches with available webarchive files
3. Creates a prioritized import script
"""

import re
from pathlib import Path
from typing import Dict, List, Tuple

BASE_DIR = Path(__file__).resolve().parents[1]
INCOMING_DIR = BASE_DIR / "incoming"
MISSING_SLUGS_FILE = BASE_DIR / "jobs" / "reports" / "missing-slugs-simple.txt"

def normalize_for_matching(text: str) -> str:
    """Normalize text for matching."""
    # Convert to lowercase and replace special chars
    text = text.lower()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'\s+', '-', text.strip())
    return text

def get_webarchive_files() -> List[Path]:
    """Get all webarchive files."""
    return list(INCOMING_DIR.glob("*.webarchive"))

def extract_slug_from_webarchive(filename: str) -> str:
    """Extract a potential slug from webarchive filename."""
    # Remove .webarchive extension
    name = filename.replace('.webarchive', '')
    
    # Remove " — New England Complex Systems Institute" suffix
    name = re.sub(r'\s*—\s*New England Complex Systems Institute.*$', '', name)
    
    # Normalize for matching
    return normalize_for_matching(name)

def match_missing_with_webarchives(missing_slugs: List[str], webarchive_files: List[Path]) -> List[Tuple[str, Path, float]]:
    """Match missing slugs with webarchive files."""
    matches = []
    
    # Create a mapping of normalized webarchive names to files
    webarchive_map = {}
    for file_path in webarchive_files:
        normalized_name = extract_slug_from_webarchive(file_path.name)
        webarchive_map[normalized_name] = file_path
    
    for missing_slug in missing_slugs:
        normalized_missing = normalize_for_matching(missing_slug)
        
        # Try exact match first
        if normalized_missing in webarchive_map:
            matches.append((missing_slug, webarchive_map[normalized_missing], 1.0))
            continue
        
        # Try partial matches
        best_match = None
        best_score = 0.0
        
        for web_name, file_path in webarchive_map.items():
            # Check if missing slug is contained in webarchive name
            if normalized_missing in web_name:
                score = len(normalized_missing) / len(web_name)
                if score > best_score:
                    best_match = file_path
                    best_score = score
            
            # Check if webarchive name is contained in missing slug
            elif web_name in normalized_missing:
                score = len(web_name) / len(normalized_missing)
                if score > best_score:
                    best_match = file_path
                    best_score = score
        
        if best_match and best_score > 0.3:  # Minimum confidence threshold
            matches.append((missing_slug, best_match, best_score))
    
    return matches

def create_import_script(matches: List[Tuple[str, Path, float]]):
    """Create a script to import the matched webarchives."""
    
    # Sort by confidence score (highest first)
    matches.sort(key=lambda x: x[2], reverse=True)
    
    script_content = f"""#!/usr/bin/env python3
'''
Auto-generated script to import missing content from webarchives.
Generated from broken link analysis.

This script will import {len(matches)} webarchive files to fix broken links.
'''

import subprocess
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
CLI_SCRIPT = BASE_DIR / "necsifactory" / "cli.py"

# Matched webarchives to import (sorted by confidence)
WEBARCHIVES_TO_IMPORT = [
"""
    
    for missing_slug, webarchive_path, confidence in matches:
        script_content += f'    ("{missing_slug}", "{webarchive_path.name}", {confidence:.2f}),\n'
    
    script_content += """]

def import_webarchive(slug: str, filename: str, confidence: float):
    '''Import a single webarchive file.'''
    print(f"🔄 Importing: {slug} (confidence: {confidence:.2f})")
    
    try:
        # Run the CLI command to import the webarchive
        result = subprocess.run([
            sys.executable, str(CLI_SCRIPT), "ingest", 
            "--webarchive", str(BASE_DIR / "incoming" / filename),
            "--build"
        ], capture_output=True, text=True, cwd=BASE_DIR)
        
        if result.returncode == 0:
            print(f"✅ Successfully imported: {slug}")
            return True
        else:
            print(f"❌ Failed to import {slug}: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error importing {slug}: {e}")
        return False

def main():
    '''Import all matched webarchives.'''
    print(f"🚀 Starting import of {len(WEBARCHIVES_TO_IMPORT)} webarchive files...")
    print("=" * 80)
    
    success_count = 0
    for slug, filename, confidence in WEBARCHIVES_TO_IMPORT:
        if import_webarchive(slug, filename, confidence):
            success_count += 1
        print()
    
    print("=" * 80)
    print(f"📊 Import Summary:")
    print(f"   ✅ Successful: {success_count}")
    print(f"   ❌ Failed: {len(WEBARCHIVES_TO_IMPORT) - success_count}")
    print(f"   📈 Success Rate: {success_count/len(WEBARCHIVES_TO_IMPORT)*100:.1f}%")
    
    if success_count > 0:
        print(f"\\n🎉 Imported {success_count} webarchive files!")
        print("   Run the link checker again to see the improvement:")
        print("   python scripts/check_internal_links.py --save-report")

if __name__ == "__main__":
    main()
"""
    
    # Save the import script
    script_path = BASE_DIR / "scripts" / "import_missing_content.py"
    with open(script_path, 'w', encoding='utf-8') as f:
        f.write(script_content)
    
    return script_path

def main():
    """Main function."""
    print("🔍 Matching missing content with available webarchives...")
    
    # Read missing slugs
    if not MISSING_SLUGS_FILE.exists():
        print(f"❌ Missing slugs file not found: {MISSING_SLUGS_FILE}")
        print("   Run: python scripts/analyze_missing_content.py")
        return
    
    with open(MISSING_SLUGS_FILE, 'r', encoding='utf-8') as f:
        missing_slugs = [line.strip() for line in f if line.strip()]
    
    print(f"📋 Found {len(missing_slugs)} missing content files")
    
    # Get webarchive files
    webarchive_files = get_webarchive_files()
    print(f"📦 Found {len(webarchive_files)} webarchive files")
    
    # Match them
    matches = match_missing_with_webarchives(missing_slugs, webarchive_files)
    
    print(f"\\n🎯 MATCHING RESULTS")
    print("=" * 80)
    print(f"✅ Found matches: {len(matches)}")
    print(f"❌ No matches: {len(missing_slugs) - len(matches)}")
    
    if matches:
        print(f"\\n📊 TOP MATCHES (by confidence):")
        for i, (slug, file_path, confidence) in enumerate(matches[:10], 1):
            print(f"{i:2d}. {slug}")
            print(f"    -> {file_path.name}")
            print(f"    Confidence: {confidence:.2f}")
            print()
        
        # Create import script
        script_path = create_import_script(matches)
        print(f"💾 Import script created: {script_path}")
        print(f"\\n🚀 To import all matched webarchives, run:")
        print(f"   python {script_path}")
    
    # Save detailed report
    report_path = BASE_DIR / "jobs" / "reports" / "webarchive-matches.txt"
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("# Webarchive Matching Report\\n")
        f.write(f"# Missing content files: {len(missing_slugs)}\\n")
        f.write(f"# Available webarchives: {len(webarchive_files)}\\n")
        f.write(f"# Matches found: {len(matches)}\\n\\n")
        
        f.write("## MATCHES FOUND\\n\\n")
        for slug, file_path, confidence in matches:
            f.write(f"- {slug}\\n")
            f.write(f"  -> {file_path.name}\\n")
            f.write(f"  Confidence: {confidence:.2f}\\n\\n")
        
        f.write("## NO MATCHES\\n\\n")
        matched_slugs = {slug for slug, _, _ in matches}
        for slug in missing_slugs:
            if slug not in matched_slugs:
                f.write(f"- {slug}\\n")
    
    print(f"📄 Detailed report saved: {report_path}")

if __name__ == "__main__":
    main()
