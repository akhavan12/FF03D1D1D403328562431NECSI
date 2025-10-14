#!/usr/bin/env python3
"""
Fix incorrect links that have double /research/research/ prefixes.

This script:
1. Finds all content files with links that have /research/research/ prefix
2. Removes the duplicate /research/ prefix to make them correct
3. Updates the content files with corrected links
"""

import json
import re
from pathlib import Path
from typing import List, Dict, Set

BASE_DIR = Path(__file__).resolve().parents[1]
CONTENT_DIR = BASE_DIR / "content"

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
        except Exception:
            pass
    return slugs

def fix_double_research_links_in_file(content_file: Path) -> int:
    """Fix /research/research/ prefix links in a single content.json file."""
    fixed_count = 0
    try:
        with open(content_file, 'r', encoding='utf-8') as f:
            content_data = json.load(f)
        
        original_content_str = json.dumps(content_data)
        modified_content_str = original_content_str

        # Find all potential links in the narrative_md
        if 'narrative_md' in content_data and content_data['narrative_md']:
            # Markdown links: [text](/research/research/slug)
            modified_content_str = re.sub(
                r'\[([^\]]+)\]\(/research/research/([^/\)]+)\)',
                r'[\1](/research/\2)',
                modified_content_str
            )
            
            # HTML links: <a href="/research/research/slug">
            modified_content_str = re.sub(
                r'<a href="/research/research/([^"/]+)"',
                r'<a href="/research/\1"',
                modified_content_str
            )
            
            # Handle more complex patterns like /research/research/food-crisis
            modified_content_str = re.sub(
                r'\[([^\]]+)\]\(/research/research/([^)]+)\)',
                r'[\1](/research/\2)',
                modified_content_str
            )
            
            # Handle HTML links with more complex patterns
            modified_content_str = re.sub(
                r'<a href="/research/research/([^"]+)"',
                r'<a href="/research/\1"',
                modified_content_str
            )
            
            # Also check for any other fields that might contain links
            for field_name in ['subtitle', 'description', 'excerpt']:
                if field_name in content_data and content_data[field_name]:
                    modified_content_str = re.sub(
                        r'\[([^\]]+)\]\(/research/research/([^)]+)\)',
                        r'[\1](/research/\2)',
                        modified_content_str
                    )
                    modified_content_str = re.sub(
                        r'<a href="/research/research/([^"]+)"',
                        r'<a href="/research/\1"',
                        modified_content_str
                    )

        if modified_content_str != original_content_str:
            modified_content_data = json.loads(modified_content_str)
            with open(content_file, 'w', encoding='utf-8') as f:
                json.dump(modified_content_data, f, ensure_ascii=False, indent=2)
            
            # Count the number of fixes made
            original_double_research = original_content_str.count('/research/research/')
            modified_double_research = modified_content_str.count('/research/research/')
            fixed_count = original_double_research - modified_double_research
            
            print(f"✅ Fixed {fixed_count} double /research/ links in: {content_file.parent.name}")
            
    except Exception as e:
        print(f"❌ Error fixing links in {content_file}: {e}")
    return fixed_count

def find_double_research_links():
    """Find all content files with double /research/research/ links."""
    print("🔍 Scanning for double /research/research/ links...")
    
    files_with_issues = []
    total_issues = 0
    
    for content_file in CONTENT_DIR.rglob("content.json"):
        try:
            with open(content_file, 'r', encoding='utf-8') as f:
                content_data = json.load(f)
            
            content_str = json.dumps(content_data)
            double_research_count = content_str.count('/research/research/')
            
            if double_research_count > 0:
                files_with_issues.append({
                    'file': content_file,
                    'count': double_research_count,
                    'slug': content_data.get('slug', 'unknown')
                })
                total_issues += double_research_count
                
        except Exception as e:
            print(f"⚠️ Error reading {content_file}: {e}")
    
    return files_with_issues, total_issues

def main():
    print("🔧 Fixing double /research/research/ links...")
    
    # First, find all files with the issue
    files_with_issues, total_issues = find_double_research_links()
    
    if not files_with_issues:
        print("✅ No double /research/research/ links found!")
        return
    
    print(f"\n📊 FOUND {len(files_with_issues)} files with {total_issues} double /research/research/ links:")
    print("=" * 80)
    
    for item in files_with_issues:
        print(f"  • {item['slug']}: {item['count']} double /research/ links")
    
    print(f"\n🔧 Fixing {len(files_with_issues)} files...")
    print("=" * 80)
    
    total_fixed_links = 0
    
    for item in files_with_issues:
        total_fixed_links += fix_double_research_links_in_file(item['file'])
    
    print(f"\n🎉 Fixed {total_fixed_links} double /research/research/ links across {len(files_with_issues)} files!")
    print("   All links now use the correct /research/slug format")
    
    # Verify the fix
    print("\n🔍 Verifying fix...")
    remaining_issues, remaining_count = find_double_research_links()
    
    if remaining_issues:
        print(f"⚠️  {len(remaining_issues)} files still have {remaining_count} double /research/ links")
    else:
        print("✅ All double /research/research/ links have been fixed!")

if __name__ == "__main__":
    main()
