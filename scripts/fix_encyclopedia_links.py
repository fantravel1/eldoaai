#!/usr/bin/env python3
"""
Script to find and fix broken links in encyclopedia pages.
"""

import os
import re
from pathlib import Path
from collections import defaultdict
import json

ENCYCLOPEDIA_DIR = Path("/home/user/eldoaai/encyclopedia")

def get_all_encyclopedia_files():
    """Get a set of all encyclopedia file slugs that exist."""
    files = set()
    for f in ENCYCLOPEDIA_DIR.glob("*.html"):
        files.add(f.stem)  # Get filename without extension
    return files

def extract_links_from_html(html_content):
    """Extract all links from related-terms and connections sections."""
    links = []

    # Pattern to find links in related-list and connections-list
    # Links look like: <a href="/encyclopedia/posterior-chain.html">Posterior Chain</a>
    pattern = r'<a href="/encyclopedia/([^"]+)\.html">([^<]+)</a>'

    # Find the related-terms section
    related_match = re.search(r'<div class="content-section related-terms">(.*?)</div>', html_content, re.DOTALL)
    if related_match:
        section_content = related_match.group(1)
        for match in re.finditer(pattern, section_content):
            links.append({
                'slug': match.group(1),
                'title': match.group(2),
                'section': 'related-terms'
            })

    # Find the connections section
    connections_match = re.search(r'<div class="content-section connections">(.*?)</div>', html_content, re.DOTALL)
    if connections_match:
        section_content = connections_match.group(1)
        for match in re.finditer(pattern, section_content):
            links.append({
                'slug': match.group(1),
                'title': match.group(2),
                'section': 'connections'
            })

    return links

def analyze_all_pages():
    """Analyze all encyclopedia pages and find broken links."""
    existing_files = get_all_encyclopedia_files()
    print(f"Found {len(existing_files)} encyclopedia files")

    broken_links = defaultdict(list)  # page -> list of broken links
    all_missing_slugs = defaultdict(int)  # slug -> count of times it's referenced

    for html_file in ENCYCLOPEDIA_DIR.glob("*.html"):
        try:
            with open(html_file, 'r', encoding='utf-8') as f:
                content = f.read()

            links = extract_links_from_html(content)

            for link in links:
                if link['slug'] not in existing_files:
                    broken_links[html_file.stem].append(link)
                    all_missing_slugs[link['slug']] += 1
        except Exception as e:
            print(f"Error processing {html_file}: {e}")

    return broken_links, all_missing_slugs, existing_files

def main():
    print("Analyzing encyclopedia pages for broken links...")
    broken_links, missing_slugs, existing_files = analyze_all_pages()

    print(f"\n=== SUMMARY ===")
    print(f"Total pages with broken links: {len(broken_links)}")
    print(f"Total unique missing slugs: {len(missing_slugs)}")

    print(f"\n=== MISSING SLUGS (sorted by frequency) ===")
    sorted_missing = sorted(missing_slugs.items(), key=lambda x: -x[1])
    for slug, count in sorted_missing:
        print(f"  {slug}: referenced {count} times")

    print(f"\n=== PAGES WITH BROKEN LINKS ===")
    for page, links in sorted(broken_links.items()):
        print(f"\n{page}.html:")
        for link in links:
            print(f"  - [{link['section']}] {link['title']} -> {link['slug']}.html (MISSING)")

    # Save detailed report
    report = {
        'total_pages_with_broken_links': len(broken_links),
        'total_missing_slugs': len(missing_slugs),
        'missing_slugs': dict(sorted_missing),
        'broken_links_by_page': {k: v for k, v in broken_links.items()}
    }

    with open('/home/user/eldoaai/scripts/broken_links_report.json', 'w') as f:
        json.dump(report, f, indent=2)

    print(f"\nDetailed report saved to broken_links_report.json")

if __name__ == "__main__":
    main()
