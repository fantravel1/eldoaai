#!/usr/bin/env python3
"""
Fix encyclopedia-data.json to have the correct structure for encyclopedia.html
Group entries by letter instead of flat array
"""

import json
from pathlib import Path
from collections import defaultdict

def fix_encyclopedia_data():
    """Restructure encyclopedia-data.json to group by letter"""

    # Read current data
    data_file = Path('/home/user/eldoaai/public/encyclopedia-data.json')

    with open(data_file, 'r', encoding='utf-8') as f:
        current_data = json.load(f)

    # Group entries by letter
    by_letter = defaultdict(list)

    for entry in current_data['entries']:
        letter = entry['letter']
        by_letter[letter].append({
            'title': entry['title'],
            'slug': entry['slug'],
            'file': entry['file']
        })

    # Sort entries within each letter
    for letter in by_letter:
        by_letter[letter].sort(key=lambda x: x['title'].lower())

    # Create new structure
    new_data = {
        'total_entries': current_data['total_entries'],
        'by_letter': dict(by_letter)
    }

    # Write back
    with open(data_file, 'w', encoding='utf-8') as f:
        json.dump(new_data, f, indent=2, ensure_ascii=False)

    print(f"✅ Fixed encyclopedia-data.json")
    print(f"   Total entries: {new_data['total_entries']}")
    print(f"   Letters: {sorted(by_letter.keys())}")
    print(f"   Letter counts: {', '.join(f'{letter}:{len(by_letter[letter])}' for letter in sorted(by_letter.keys()))}")

if __name__ == "__main__":
    fix_encyclopedia_data()
