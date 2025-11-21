#!/usr/bin/env python3
"""
Clean up and standardize practitioner data.
"""

import json
from datetime import datetime

def cleanup_country(practitioner):
    """Fix and standardize country names."""
    country = practitioner.get('country', '')

    # Fix incorrect country values that are actually regions/cities
    fixes = {
        'Abu Dhabi': 'United Arab Emirates',
        'LA / Oakland': 'United States',
        'NY / Milan': 'United States',  # Primary location appears to be NY
        'NZ / Santa Monica': 'New Zealand',  # Primary location
        'Surrey': 'United Kingdom',
        'East Sussex': 'United Kingdom',
        'MO': 'United States',
        'NM': 'United States',
        'Austria': 'Austria',
        'Germany': 'Germany',
        'Italy': 'Italy',
        'France': 'France',
        'Canada': 'Canada',
        'United States': 'United States',
        'United Kingdom': 'United Kingdom',
        'New Zealand': 'New Zealand',
        'UK': 'United Kingdom',
    }

    if country in fixes:
        practitioner['country'] = fixes[country]

    # Handle special cases with dual locations
    if practitioner.get('name') == 'Ilaria Cavagna' and country == 'United States':
        # She operates in both NYC and Milan
        practitioner['country'] = 'United States'
        practitioner['alternateCity'] = 'Milan'
        practitioner['alternateCountry'] = 'Italy'

    if practitioner.get('name') == 'Brent Meier':
        # Operates between NZ and CA
        practitioner['country'] = 'New Zealand'
        practitioner['alternateCity'] = 'Santa Monica'
        practitioner['alternateState'] = 'CA'
        practitioner['alternateCountry'] = 'United States'

    return practitioner

def main():
    print("Cleaning up practitioner data...")

    # Load data
    with open('/home/user/eldoaai/data/practitioners.json', 'r') as f:
        data = json.load(f)

    # Clean each practitioner
    for p in data['practitioners']:
        p = cleanup_country(p)

    # Update countries list
    countries = set()
    for p in data['practitioners']:
        if 'country' in p:
            countries.add(p['country'])
    data['countries'] = sorted(list(countries))

    # Update metadata
    data['lastUpdated'] = datetime.now().strftime('%Y-%m-%d')

    # Count by level
    level_counts = {}
    for p in data['practitioners']:
        level = p.get('level')
        if level:
            level_counts[level] = level_counts.get(level, 0) + 1

    # Count by country
    country_counts = {}
    for p in data['practitioners']:
        country = p.get('country')
        if country:
            country_counts[country] = country_counts.get(country, 0) + 1

    # Save
    with open('/home/user/eldoaai/data/practitioners.json', 'w') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"\n{'='*60}")
    print(f"✓ Data cleaned successfully")
    print(f"✓ Total practitioners: {data['totalCount']}")
    print(f"✓ Countries: {', '.join(data['countries'])}")
    print(f"\nBreakdown by level:")
    for level in sorted(level_counts.keys()):
        print(f"  Level {level}: {level_counts[level]} practitioners")
    print(f"\nTop 5 countries by practitioner count:")
    sorted_countries = sorted(country_counts.items(), key=lambda x: x[1], reverse=True)[:5]
    for country, count in sorted_countries:
        print(f"  {country}: {count} practitioners")
    print(f"{'='*60}")

if __name__ == '__main__':
    main()
