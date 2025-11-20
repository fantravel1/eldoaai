#!/usr/bin/env python3
"""
Remove duplicate entries from encyclopedia-data.json
"""

import json
from collections import defaultdict

# Paths
INPUT_FILE = "/home/user/eldoaai/public/encyclopedia-data.json"
OUTPUT_FILE = "/home/user/eldoaai/public/encyclopedia-data.json"

def main():
    """Remove duplicates from encyclopedia data"""
    print("Loading encyclopedia data...")

    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)

    old_total = data['total_entries']
    print(f"Current total entries: {old_total}")

    # Collect all entries from by_letter structure
    all_entries = []
    for letter, entries in data['by_letter'].items():
        all_entries.extend(entries)

    print(f"Found {len(all_entries)} total entries across all letters")

    # Deduplicate entries using slug as the unique key
    seen_slugs = set()
    unique_entries = []

    for entry in all_entries:
        slug = entry['slug']
        if slug not in seen_slugs:
            seen_slugs.add(slug)
            unique_entries.append(entry)

    # Rebuild by_letter with unique entries
    by_letter = defaultdict(list)
    for entry in unique_entries:
        # Get letter from entry or from title
        letter = entry.get('letter', entry['title'][0].upper() if entry['title'] else 'A')
        by_letter[letter].append(entry)

    # Sort entries within each letter alphabetically
    for letter in by_letter:
        by_letter[letter].sort(key=lambda x: x['title'].lower())

    # Create new data structure
    new_data = {
        'total_entries': len(unique_entries),
        'by_letter': dict(by_letter)
    }

    # Save deduplicated data
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(new_data, f, indent=2)

    new_total = len(unique_entries)
    duplicates_removed = old_total - new_total

    print(f"\n✅ Deduplication complete!")
    print(f"   Original entries: {old_total}")
    print(f"   Unique entries: {new_total}")
    print(f"   Duplicates removed: {duplicates_removed}")
    print(f"\nSaved to: {OUTPUT_FILE}")

    # Print summary by letter
    print("\nEntries by letter:")
    for letter in sorted(by_letter.keys()):
        print(f"  {letter}: {len(by_letter[letter])} entries")

if __name__ == "__main__":
    main()
