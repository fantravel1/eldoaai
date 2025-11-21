#!/usr/bin/env python3
"""
Extract practitioner data from PDF research files and convert to JSON format.
"""

import json
import re
from typing import Dict, List, Any
from datetime import datetime

def slugify(name: str) -> str:
    """Convert name to URL-friendly slug."""
    slug = name.lower()
    slug = re.sub(r'[^\w\s-]', '', slug)
    slug = re.sub(r'[-\s]+', '-', slug)
    return slug.strip('-')

def parse_level_to_int(level_str: str) -> int:
    """Extract numeric level from level string."""
    if not level_str:
        return None
    match = re.search(r'(\d+)', level_str)
    return int(match.group(1)) if match else None

def get_level_title(level: int) -> str:
    """Get standardized level title."""
    titles = {
        1: "Beginner Student",
        2: "Student Practitioner",
        3: "Advanced Student",
        4: "Certified Trainer / Master Instructor",
        5: "Certified Therapist",
        6: "Expert / Creator"
    }
    return titles.get(level, f"Level {level}")

def parse_years_experience(years_str: str) -> str:
    """Standardize years of experience format."""
    if not years_str:
        return None
    # Extract number
    match = re.search(r'(\d+)\+?', years_str)
    if match:
        num = match.group(1)
        return f"{num}+"
    return years_str

def parse_city_region(location_str: str) -> Dict[str, str]:
    """Parse city/region from location string."""
    result = {}
    if not location_str:
        return result

    # Handle formats like "Seal Beach, CA" or "Toronto, ON"
    parts = [p.strip() for p in location_str.split(',')]
    if len(parts) >= 1:
        result['city'] = parts[0]
    if len(parts) >= 2:
        # Check if it's a US state or country
        state_code = parts[1]
        if state_code in ['CA', 'TX', 'FL', 'AZ', 'GA', 'CT', 'CO', 'IL', 'ID', 'WA', 'NY']:
            result['state'] = state_code
            result['country'] = 'United States'
        elif state_code in ['ON', 'QC', 'BC', 'AB']:
            result['region'] = state_code
            result['country'] = 'Canada'
        else:
            result['country'] = parts[1]

    return result

# Manual extraction of key practitioners from ART8 PDF
# This is based on the PDF content we can see
practitioners_from_pdf = [
    # Level 6
    # Guy Voyer already in database, marked deceased

    # Level 5
    {
        "name": "Mike Christy",
        "level": "5.2",
        "years": "15+",
        "bio": "Fluidpower Health and Performance specialist, advanced spinal pathology expertise",
        "website": "fluidpowerkelowna.com",
        "location": "Kelowna, BC, Canada"
    },
    {
        "name": "Dr. Samarpan Ananda",
        "credentials": ["DC"],
        "level": "5.1, Pelviology Certified",
        "years": "12+",
        "bio": "Chiropractor combining ELDOA with yoga and pelviology at Chiroyoga Wellness Clinic",
        "website": "chiroyoga.janeapp.com",
        "location": "Pensacola Beach, FL"
    },
    {
        "name": "Laura Masserdotti",
        "level": "4 and 5.1",
        "years": "15+",
        "bio": "Founder of ELDOA Revolution, integrates Pilates with ELDOA, runs certification school in Italy",
        "website": "eldoarevolution.com",
        "location": "Brescia, Italy"
    },

    # Level 4 - California (sample from PDF)
    {
        "name": "Scott Herrera",
        "level": "4 - Director of ELDOA Certification Program",
        "years": "20+ (since 2003)",
        "bio": "Author of ELDOA Levels 1-3 course books, works with MLB/NHL teams (Atlanta Braves, Washington Nationals, Dallas Stars, LA Dodgers), founder Legacy Sport & Wellness",
        "website": "legacyperformwell.com",
        "location": "Dallas, TX"
    },
    {
        "name": "Bryce Turner",
        "level": "4, Soma Training/Therapy Graduate, Osteopathy Candidate",
        "years": "13+ (since 2012)",
        "bio": "Co-founder Beach Fitness and ELDOAUSA, one of elite few approved Level 1-4 instructors in US, works with NBA/NHL/NFL/MLB athletes",
        "website": "eldoausa.com",
        "location": "Seal Beach, CA"
    },
    {
        "name": "Petra Baethmann",
        "level": "4 Teacher Trainer",
        "years": "18+ (founded studio 2006)",
        "bio": "Owner Sphinx Pilates + ELDOA, combines Pilates with ELDOA, teaches certification courses internationally, B.Commerce McGill",
        "website": "sphinxpilates.com",
        "location": "Toronto, ON, Canada"
    },
    {
        "name": "Ben Hubers",
        "level": "4, Soma Trainer, CDO Candidate",
        "years": "10+",
        "bio": "Former Olympic Trials track athlete for Canada, multiple Georgia state champion, works with NHL players, teaches Nashville and California courses",
        "website": "bensomaperformance.com",
        "location": "Santa Monica, CA"
    },
    {
        "name": "Brent Meier",
        "level": "4",
        "years": "12+",
        "bio": "Soma Education West Coast, operates internationally between New Zealand and California",
        "email": "ghpoffice1@gmail.com",
        "location": "Auckland, NZ / Santa Monica, CA"
    },
    {
        "name": "Ilaria Cavagna",
        "level": "4, teaches Levels 1-4",
        "years": "15+ (since 2008)",
        "bio": "Founder of FEETNESS™ ('posture from the ground up'), teaches NYC/Milan, Pilates Anytime instructor, B.S. Movement Science, trained with Romana Kryzanowska",
        "website": "ilariacavagna.com, feetness.com",
        "location": "New York, NY / Milan, Italy"
    },
    {
        "name": "Peter Bodi",
        "level": "4",
        "years": "15+",
        "bio": "SomaTraining UK director, operates Bowskill Clinic",
        "website": "somatraining.co.uk",
        "location": "London, UK"
    },
    {
        "name": "Marcelle Jalkh",
        "level": "4",
        "years": "12+",
        "bio": "Middle East operations specialist",
        "website": "marcellejalkh.com",
        "location": "Zahra, Abu Dhabi"
    },
    {
        "name": "Clemens Dolinar",
        "level": "4",
        "years": "10+",
        "bio": "Austria operations director",
        "email": "somatraining.austria@gmail.com",
        "location": "Vienna, Austria"
    },
    {
        "name": "Sarah King",
        "level": "4",
        "years": "12+",
        "bio": "Germany operations, integrates ELDOA with classical Pilates, manual therapy background, podcast guest",
        "website": "authenticbodycontrol.com",
        "location": "Berlin, Germany"
    },
    {
        "name": "Justin Brien",
        "level": "4, Soma Trainer/Therapist, CHEK Practitioner",
        "years": "18+ exercise/rehab, 10+ ELDOA",
        "bio": "One of three approved Level 4 practical instructors, owner Natural Movement Solutions, hosts courses New Orleans/Sausalito",
        "website": "naturalmovementsolutions.com",
        "location": "Covington, LA / Oakland, CA"
    },
    {
        "name": "Dan Hellman",
        "level": "4, Licensed PT, Paul Chek Practitioner",
        "years": "15+",
        "bio": "Golf Digest '50 Best Golf Fitness Professionals,' co-creator 'ELDOA FOR GOLF' TPI course, trained Tiger Woods and NHL/NFL players, owner H3",
        "website": "h3bydan.com",
        "location": "Fort Myers, FL"
    },
    {
        "name": "Janet Alexander",
        "level": "4 Master, TPI Level 3",
        "years": "35+ health/fitness",
        "bio": "Co-creator 'ELDOA FOR GOLF' TPI course, co-owner Pacific Fitness and Health, featured Golf Channel, successful triathlete",
        "website": "pacificfitnesshealth.com",
        "location": "Encinitas, CA"
    },
]

def convert_to_schema(practitioner_data: Dict) -> Dict[str, Any]:
    """Convert extracted practitioner data to match the schema."""
    name = practitioner_data.get('name', '')
    level_str = practitioner_data.get('level', '')

    # Parse level
    level_num = parse_level_to_int(level_str)

    # Parse location
    location = parse_city_region(practitioner_data.get('location', ''))

    # Build practitioner object
    result = {
        "id": slugify(name),
        "name": name,
        "status": "active",
        "level": level_num,
        "levelTitle": get_level_title(level_num) if level_num else None,
    }

    # Add location fields
    if 'country' in location:
        result['country'] = location['country']
    if 'state' in location:
        result['state'] = location['state']
    if 'region' in location:
        result['region'] = location['region']
    if 'city' in location:
        result['city'] = location['city']

    # Years of experience
    if 'years' in practitioner_data:
        result['yearsExperience'] = parse_years_experience(practitioner_data['years'])

    # Credentials
    if 'credentials' in practitioner_data:
        result['credentials'] = practitioner_data['credentials']

    # Specializations - extract from bio
    specializations = []
    bio = practitioner_data.get('bio', '')
    if 'Pilates' in bio:
        specializations.append('Pilates')
    if 'ELDOA' in bio or 'eldoa' in bio.lower():
        specializations.append('ELDOA')
    if 'golf' in bio.lower():
        specializations.append('Golf fitness')
    if 'sports' in bio.lower() or 'athlete' in bio.lower():
        specializations.append('Sports medicine')
    if 'yoga' in bio.lower():
        specializations.append('Yoga')

    if specializations:
        result['specializations'] = specializations

    # Background
    if bio:
        result['background'] = bio

    # Contact info
    if 'website' in practitioner_data:
        result['website'] = practitioner_data['website']
    if 'email' in practitioner_data:
        result['email'] = practitioner_data['email']
    if 'phone' in practitioner_data:
        result['phone'] = practitioner_data['phone']

    # Remove None values
    result = {k: v for k, v in result.items() if v is not None}

    return result

def main():
    """Main extraction function."""
    print("Extracting practitioner data from PDF research...")

    # Convert extracted data to schema format
    new_practitioners = []
    for p in practitioners_from_pdf:
        converted = convert_to_schema(p)
        new_practitioners.append(converted)

    # Load existing practitioners
    with open('/home/user/eldoaai/data/practitioners.json', 'r') as f:
        data = json.load(f)

    existing_ids = {p['id'] for p in data['practitioners']}

    # Add only new practitioners
    added_count = 0
    for p in new_practitioners:
        if p['id'] not in existing_ids:
            data['practitioners'].append(p)
            added_count += 1
            print(f"Added: {p['name']}")
        else:
            print(f"Skipped (already exists): {p['name']}")

    # Update metadata
    data['totalCount'] = len(data['practitioners'])
    data['lastUpdated'] = datetime.now().strftime('%Y-%m-%d')

    # Update countries list
    countries = set()
    for p in data['practitioners']:
        if 'country' in p:
            countries.add(p['country'])
    data['countries'] = sorted(list(countries))

    # Save updated data
    with open('/home/user/eldoaai/data/practitioners.json', 'w') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"\n✓ Added {added_count} new practitioners")
    print(f"✓ Total practitioners: {data['totalCount']}")
    print(f"✓ Countries: {', '.join(data['countries'])}")

if __name__ == '__main__':
    main()
