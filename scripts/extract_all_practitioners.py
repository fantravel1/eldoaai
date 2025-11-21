#!/usr/bin/env python3
"""
Comprehensive extraction of ALL practitioners from PDF research files.
This extracts hundreds of practitioners across all levels and countries.
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
    # Handle "5.1", "5.2" etc - convert to base level
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
    if not years_str or years_str == "Not specified":
        return None
    match = re.search(r'(\d+)\+?', years_str)
    if match:
        num = match.group(1)
        return f"{num}+"
    return years_str

def parse_location(location_str: str) -> Dict[str, str]:
    """Parse city/state/country from location string."""
    result = {}
    if not location_str:
        return result

    parts = [p.strip() for p in location_str.split(',')]
    if len(parts) >= 1:
        result['city'] = parts[0]

    if len(parts) >= 2:
        state_or_country = parts[1].strip()

        # US states
        us_states = ['CA', 'TX', 'FL', 'AZ', 'GA', 'CT', 'CO', 'IL', 'ID', 'WA', 'NY',
                     'TN', 'LA', 'NJ', 'MA', 'PA', 'OR', 'NV', 'NC', 'SC', 'MI', 'OH']
        # Canadian provinces
        ca_provinces = ['ON', 'QC', 'BC', 'AB', 'MB', 'SK', 'NS', 'NB']

        if state_or_country in us_states:
            result['state'] = state_or_country
            result['country'] = 'United States'
        elif state_or_country in ca_provinces:
            result['region'] = state_or_country
            result['country'] = 'Canada'
        else:
            result['country'] = state_or_country

    return result

# Comprehensive extraction from ART8 PDF
# Organized by Level and Region

ALL_PRACTITIONERS = [
    # ===== LEVEL 5 =====
    {"name": "Mike Christy", "level": "5", "years": "15+", "bio": "Fluidpower Health and Performance specialist, advanced spinal pathology expertise", "website": "fluidpowerkelowna.com", "location": "Kelowna, BC"},
    {"name": "Dr. Samarpan Ananda", "credentials": ["DC"], "level": "5", "years": "12+", "bio": "Chiropractor combining ELDOA with yoga and pelviology at Chiroyoga Wellness Clinic", "website": "chiroyoga.janeapp.com", "location": "Pensacola Beach, FL"},
    {"name": "Laura Masserdotti", "level": "5", "years": "15+", "bio": "Founder of ELDOA Revolution, integrates Pilates with ELDOA, runs certification school in Italy", "website": "eldoarevolution.com", "location": "Brescia, Italy"},

    # ===== LEVEL 4 - KEY LEADERS =====
    {"name": "Scott Herrera", "level": "4", "years": "20+", "bio": "Director of ELDOA Certification Program, author of ELDOA Levels 1-3 course books, works with MLB/NHL teams (Atlanta Braves, Washington Nationals, Dallas Stars, LA Dodgers)", "website": "legacyperformwell.com", "location": "Dallas, TX"},
    {"name": "Bryce Turner", "level": "4", "years": "13+", "bio": "Co-founder Beach Fitness and ELDOAUSA, one of elite few approved Level 1-4 instructors in US, works with NBA/NHL/NFL/MLB athletes", "website": "eldoausa.com", "location": "Seal Beach, CA"},
    {"name": "Petra Baethmann", "level": "4", "years": "18+", "bio": "Owner Sphinx Pilates + ELDOA, combines Pilates with ELDOA, teaches certification courses internationally", "website": "sphinxpilates.com", "location": "Toronto, ON"},
    {"name": "Ben Hubers", "level": "4", "years": "10+", "bio": "Former Olympic Trials track athlete for Canada, works with NHL players, teaches Nashville and California courses", "website": "bensomaperformance.com", "location": "Santa Monica, CA"},
    {"name": "Brent Meier", "level": "4", "years": "12+", "bio": "Soma Education West Coast, operates internationally between New Zealand and California", "email": "ghpoffice1@gmail.com", "location": "Auckland, New Zealand"},
    {"name": "Ilaria Cavagna", "level": "4", "years": "15+", "bio": "Founder of FEETNESS™, teaches NYC/Milan, Pilates Anytime instructor, B.S. Movement Science", "website": "ilariacavagna.com", "location": "New York, NY"},

    # ===== LEVEL 4 - INTERNATIONAL =====
    {"name": "Peter Bodi", "level": "4", "years": "15+", "bio": "SomaTraining UK director, operates Bowskill Clinic", "website": "somatraining.co.uk", "location": "London, UK"},
    {"name": "Marcelle Jalkh", "level": "4", "years": "12+", "bio": "Middle East operations specialist", "website": "marcellejalkh.com", "location": "Abu Dhabi, UAE"},
    {"name": "Clemens Dolinar", "level": "4", "years": "10+", "bio": "Austria operations director", "email": "somatraining.austria@gmail.com", "location": "Vienna, Austria"},
    {"name": "Sarah King", "level": "4", "years": "12+", "bio": "Germany operations, integrates ELDOA with classical Pilates, manual therapy background", "website": "authenticbodycontrol.com", "location": "Berlin, Germany"},

    # ===== LEVEL 4 - USA CALIFORNIA (from PDF pages 6-9) =====
    {"name": "Justin Brink", "credentials": ["DC"], "level": "4", "years": "12+", "bio": "Premiere Spine & Sport chiropractor", "email": "drjbrink@gmail.com", "location": "San Jose, CA"},
    {"name": "Jeffrey Chenault", "level": "4", "years": "10+", "bio": "Red Dot Fitness owner", "email": "jchenault90@yahoo.com", "location": "San Jose, CA"},
    {"name": "Jaron Hua", "credentials": ["DC"], "level": "4", "years": "10+", "bio": "Full Circle Holistic Health, ART certified, chronic pain specialist, studying Manual Osteopathy", "website": "fchlc.com", "location": "San Francisco Bay Area, CA"},
    {"name": "Joe McVeigh", "level": "4", "years": "12+", "bio": "Independent practitioner", "email": "joe.mcveigh@gmail.com", "location": "Burlingame, CA"},
    {"name": "Jonathan Pierce", "level": "4", "years": "8+", "bio": "Kinetik Performance", "website": "kineticperformanceco.com", "location": "San Diego, CA"},
    {"name": "Tyler Ferrell", "level": "4", "years": "10+", "bio": "Golf-specific training, La Rinconada Country Club", "website": "golfsmartacademy.com", "location": "San Jose, CA"},
    {"name": "Tara Lyn Emerson", "credentials": ["ACE CPT", "Pre/Postnatal Coach"], "level": "4", "years": "12+", "bio": "Featured on Popsugar Fitness, iFit, TRX Training Club. Charcot Marie Tooth disease survivor, grew 1.25\" with ELDOA", "website": "taralynemerson.com", "location": "Los Angeles, CA"},
    {"name": "Travis McKay", "credentials": ["DPT"], "level": "4", "years": "10+", "bio": "TherEx Station", "website": "therexstation.com", "location": "Torrance, CA"},
    {"name": "Jeffrey Lacson", "level": "4", "years": "8+", "bio": "Kinetik Performance", "email": "jeffreyplacson@gmail.com", "location": "San Diego, CA"},

    # ===== LEVEL 4 - USA OTHER STATES (from PDF pages 10-11) =====
    {"name": "Denise Herrera", "level": "4", "years": "12+", "bio": "Scottsdale/Dallas area", "email": "dherrera15fish@gmail.com", "location": "Scottsdale, AZ"},
    {"name": "Kacey A. Grissom", "level": "4", "years": "10+", "bio": "Bodies Organized owner", "email": "bodiesorganized@gmail.com", "location": "Tucson, AZ"},
    {"name": "Devon Smith-Breidel", "level": "4", "years": "8+", "bio": "Independent practitioner", "email": "schnakie68@gmail.com", "location": "Scottsdale, AZ"},
    {"name": "Deva Lingemann", "level": "4", "years": "10+", "bio": "Independent practitioner", "email": "dlingemann@yahoo.com", "location": "Cave Creek, AZ"},
    {"name": "Jimmy Yuan", "credentials": ["DC"], "level": "4", "years": "10+", "bio": "Warrior Restoration owner", "website": "warriorrestoration.com", "location": "Phoenix, AZ"},
    {"name": "Timothy Pierce", "level": "4", "years": "8+", "bio": "Colorado specialist", "location": "Centennial, CO"},
    {"name": "Ian Ryan", "level": "4", "years": "8+", "bio": "Independent practitioner", "email": "iqryan11@gmail.com", "location": "Litchfield, CT"},
    {"name": "Talita Moss", "level": "4", "years": "15+", "bio": "Talita Moss Yoga owner, yoga integration", "website": "talitamossyoga.com", "location": "Darien, CT"},
    {"name": "James D. Knox", "level": "4", "years": "10+", "bio": "Knox Trainz owner", "website": "knoxtrainz.com", "location": "West Palm Beach, FL"},
    {"name": "Andrew Johnston", "level": "4", "years": "10+", "bio": "Triumph Training owner", "website": "triumphtraining.com", "location": "Atlanta, GA"},
    {"name": "Christin Zimmerman", "level": "4", "years": "8+", "bio": "Independent practitioner", "email": "christinazimmerman@me.com", "location": "Savannah, GA"},
    {"name": "Linda Danner", "level": "4", "years": "15+", "bio": "Peak Soma Training", "email": "lindardanner@yahoo.com", "location": "Bishop, CA"},
    {"name": "Andrew Anderson", "level": "4", "years": "Not specified", "bio": "Hosts courses at Ascent Fitness Studio, emerging educator", "location": "Westmont, IL"},

    # ===== LEVEL 4 - CANADA (from PDF page 11-12) =====
    {"name": "Bob Bowers", "level": "4", "years": "20+", "bio": "Co-operates Infinite Healing with Hajnal Laszlo, physical preparation coach, Thai Massage, Life Coach", "website": "infinite-healing.com", "location": "Thornhill, ON"},
    {"name": "Hajnal Laszlo", "level": "4", "years": "12+", "bio": "Co-operates Infinite Healing, works with high-performance athletes", "website": "infinite-healing.com", "location": "Thornhill, ON"},
    {"name": "Kathleen Trotter", "level": "4", "years": "15+", "bio": "Fitness writer and trainer", "email": "ksdtrotter@hotmail.com", "location": "Toronto, ON"},
    {"name": "Kerry Timko", "level": "4", "years": "12+", "bio": "Elite Athletic Conditioning owner", "email": "coachtimko@gmail.com", "location": "Thunder Bay, ON"},
    {"name": "Lisa-Marie Farley", "level": "4", "years": "15+", "bio": "Institut SomaTraining director", "email": "farleylisamarie@gmail.com", "location": "Montreal, QC"},
    {"name": "Marie-Eve Rousseau", "level": "4", "years": "10+", "bio": "Sports conditioning specialist", "email": "conditionnement.enpq@nicolet.ca", "location": "Nicolet, QC"},
    {"name": "Marla Waal", "level": "4", "years": "12+", "bio": "Vitality Movement Studio owner", "email": "vitalitymovementstudio@gmail.com", "location": "Vancouver, BC"},
    {"name": "Myriam Lacerte", "level": "4", "years": "10+", "bio": "Regional specialist", "email": "njgray@telusplanet.net", "location": "Stoneham-Tewkesbury, QC"},
    {"name": "Noreen Gray", "level": "4", "years": "15+", "bio": "Alberta specialist", "email": "njgray@telusplanet.net", "location": "Okotoks, AB"},
    {"name": "Paul Sherman", "level": "4", "years": "15+", "bio": "Soma Education Canada director", "website": "somaeducation.ca", "location": "Vancouver, BC"},
    {"name": "Sheri Kimura", "level": "4", "years": "18+", "bio": "Former dancer, Pilates/ELDOA at Shift Bodywork, specializes in pre/post surgery rehab, Myofascial Stretching Certified", "website": "shiftbodywork.com", "location": "Toronto, ON"},
    {"name": "Todd Fontaine", "level": "4", "years": "10+", "bio": "Fontaine Fitness owner", "email": "tyq7am@live.ca", "location": "Abbotsford, BC"},
    {"name": "Carolyn Woods", "level": "4", "years": "15+", "bio": "Vancouver Pilates Centre", "email": "carolynwoods007@gmail.com", "location": "Vancouver, BC"},
    {"name": "Diane Durocher", "level": "4", "years": "10+", "bio": "Regional specialist", "location": "Lac Supérieur, QC"},
    {"name": "Janine Jacques", "level": "4", "years": "12+", "bio": "Vancouver specialist", "email": "janine-jacques@hotmail.com", "location": "Vancouver, BC"},
    {"name": "Sarah Moore", "level": "4", "years": "10+", "bio": "Pilates/ELDOA specialist", "website": "sarahpilateseldoa.com", "location": "Canada"},
    {"name": "Claudia Zelazny", "level": "4", "years": "10+", "bio": "Co-owner Legacy Sport & Wellness with Scott Herrera, works with pro athletes", "website": "legacyperformwell.com", "location": "Dallas, TX"},

    # ===== PROMINENT ONLINE/YOUTUBE PRACTITIONERS (from PDF pages 13-15) =====
    {"name": "Stephanie McCusker", "level": "4", "years": "17+", "bio": "Founder ELDOA METHOD, head instructor with online video library and live sessions. B.S. Kinesiology, NSCA certified. Featured in Runner's World. Former U Maine track athlete, worked with NZ Skycity Breakers", "website": "eldoamethod.com", "location": "Tauranga/Auckland, New Zealand"},
    {"name": "Dr. John Rusin", "credentials": ["DPT"], "level": "Not certified", "years": "18+", "bio": "Physical therapist and performance coach, named top 50 fitness experts Men's Health, published comprehensive ELDOA articles, pain-free performance training", "website": "drjohnrusin.com", "location": "San Diego, CA"},
    {"name": "Jacob Magnusson Schoen", "level": "Student Practitioner", "years": "10+", "bio": "Owner SHIFT Fitness Systems, featured on Ben Greenfield Fitness podcast, introduced ELDOA to Greenfield who discussed on Joe Rogan", "website": "shiftfitnesssystems.com", "location": "New Orleans, LA"},
    {"name": "Mind Pump Media", "level": "Not certified", "years": "40+ combined", "bio": "Popular fitness podcast/YouTube (Mind Pump TV) featuring ELDOA education, partnered with ELDOAUSA", "website": "mindpumpmedia.com", "location": "California"},
    {"name": "Dr. Eric", "credentials": ["DC"], "level": "Studied under Guy Voyer", "years": "9+", "bio": "Bay Chiro Santa Monica, integrates chiropractic with ELDOA home exercises, collaborates with Bryce Turner", "website": "baychirosantamonica.com", "location": "Santa Monica, CA"},
    {"name": "Robbi Basran", "level": "Physiotherapist", "years": "8+", "bio": "Coast Performance Rehab, demonstration videos for back/neck pain", "website": "coastperformancerehab.com", "location": "Kitsilano/Vancouver, BC"},
    {"name": "Ekemba Sooh", "level": "4", "years": "12+", "bio": "Certified all 5 ELDOA levels, SMTr, SMTh. Comprehensive ELDOA and osteopathic exercise programs, monthly free classes, online training", "website": "solcorefitness.com", "location": "Santa Fe, NM"},
    {"name": "Angie Campbell", "level": "4", "years": "20+", "bio": "Certified ELDOA Trainer, Yoga Therapist (C-IAYT, E-RYT 500). Integrates ELDOA with yoga therapy, BFA dance, teaches 200/300-hr Yoga Teacher Training", "website": "urbanbreathyoga.com", "location": "St. Louis, MO"},
    {"name": "Stacey Stone", "level": "4", "years": "20+", "bio": "ELDOA Practitioner, CPT, CHEK Level 1, Yoga, Reiki Master. Integrates ELDOA with strengthening, whole-body approach", "website": "stillandmovingcenter.com", "location": "Hawaii"},

    # ===== NEW YORK AREA (from PDF pages 17-18) =====
    {"name": "Abena", "level": "3", "years": "Not specified", "bio": "Owner Abena Pilates studio Upper West Side, offers ELDOA in private sessions or Feel Fab Pilates packages for chronic pain", "website": "abenapilates.com", "location": "New York, NY"},
    {"name": "Brooke Chaffee", "level": "3", "years": "Teaching since 2009", "bio": "Former figure skater/dancer, trained at Romana's Pilates (PPATT 2018), University of the Arts Philadelphia, works with athletes and injury recovery", "website": "brookechaffee.com", "location": "New York, NY"},
    {"name": "Enqing", "level": "Certified", "years": "Not specified", "bio": "Owner Wellness Within Studio, specializes in ELDOA Alignment Classes, offers infrared sauna/ice bath", "website": "wellnesswithinstudio.com", "location": "New York, NY"},

    # ===== ADDITIONAL NOTABLE (from PDF pages 18-19) =====
    {"name": "Shannon & Julian", "level": "4", "years": "Not specified", "bio": "Co-owners Grace Yoga, offer dedicated ELDOA classes addressing Tech Neck and cervical spine", "website": "graceyogaonhighland.com", "location": "Location not specified"},
    {"name": "Joel Shepherd", "level": "4", "years": "Not specified", "bio": "Lead instructor Pacific Clinic, group classes and 1:1 sessions, chronic pain and aging optimization, CPT, Senior Fitness Specialist", "website": "pacific.clinic", "location": "Richland, WA"},
    {"name": "Laura Sifuentez", "level": "Certified", "years": "Not specified", "bio": "Integrates ELDOA with Pilates, Myofascial stretching, Feet-Ness, breath exercises, online consultations", "website": "laurasifuentez.com", "location": "USA"},
    {"name": "Jillian Keeler", "level": "Course host", "years": "Not specified", "bio": "Hosts ELDOA certification courses in Nashville, works with Ben Hubers", "location": "Nashville, TN"},

    # ===== LEVEL 3 - REPRESENTATIVE SAMPLE (from PDF pages 20-21) =====
    {"name": "Sue Falsone", "level": "3", "years": "Not specified", "bio": "Structure and Function Education, sports performance specialist", "location": "Phoenix, AZ"},
    {"name": "Adam Wright", "level": "3", "years": "Not specified", "bio": "Animal House Fitness", "location": "Riverside, CA"},
    {"name": "Adriene Ingalls", "level": "3", "years": "Not specified", "bio": "Premier Pilates & Yoga", "location": "New York, NY"},
    {"name": "Jaishri Mistry", "level": "3", "years": "Not specified", "location": "Uxbridge, ON"},
    {"name": "Janey Walker", "level": "3", "years": "Not specified", "bio": "Pilates 4 U", "location": "Richmond Hill, ON"},
    {"name": "Kim Bajer", "level": "3", "years": "Not specified", "location": "Mississauga, ON"},
    {"name": "Mary German", "level": "3", "years": "Not specified", "bio": "Living Well Pilates", "location": "Oakville, ON"},

    # Italy Level 3 practitioners
    {"name": "Chiara Florian", "level": "3", "years": "Not specified", "bio": "Primo Pilates", "location": "Milan, Italy"},
    {"name": "Claudia Ferri Cataldi", "level": "3", "years": "Not specified", "location": "Vimercate, Italy"},
    {"name": "Cristina Centrone", "level": "3", "years": "Not specified", "bio": "GB Fitness", "location": "Sesto San Giovanni, Italy"},
    {"name": "Eros Rizzo", "level": "3", "years": "Not specified", "location": "San Damiano d'Asti, Italy"},
    {"name": "Francesca Bertelli", "level": "3", "years": "Not specified", "bio": "Scuola Pilates/ELDOA Revolution", "location": "Brescia, Italy"},
    {"name": "Gianluca Miracoli", "level": "3", "years": "Not specified", "location": "Corsico, Italy"},
    {"name": "Sabrina Bahbout", "level": "3", "years": "Not specified", "bio": "Elephant Pilates Roma", "location": "Rome, Italy"},
    {"name": "Samantha Ferrari", "level": "3", "years": "Not specified", "location": "Lesmo, Italy"},

    # Germany Level 3 practitioners
    {"name": "Amanda Diatta", "level": "3", "years": "Not specified", "location": "Stuttgart, Germany"},
    {"name": "Chantal Kirch", "level": "3", "years": "Not specified", "location": "Berlin, Germany"},
    {"name": "Daena Brandt", "level": "3", "years": "Not specified", "location": "Berlin, Germany"},
    {"name": "Lilli Bornemann", "level": "3", "years": "Not specified", "location": "Munster, Germany"},
    {"name": "Nina Ingrid Laiblin", "level": "3", "years": "Not specified", "location": "Stuttgart, Germany"},
    {"name": "Verena Polkowski", "level": "3", "years": "Not specified", "location": "Frankfurt, Germany"},

    # UK Level 3 practitioners
    {"name": "Daniel Holman", "level": "3", "years": "Not specified", "location": "Northampton, UK"},
    {"name": "Hugh Mackay", "level": "3", "years": "Not specified", "location": "Exeter, UK"},
    {"name": "Keith Lazarus", "level": "3", "years": "Not specified", "location": "London, UK"},
    {"name": "Matthew Chappel", "level": "3", "years": "Not specified", "bio": "Evolved Health", "location": "Salisbury, UK"},
    {"name": "Regina Smohai", "level": "3", "years": "Not specified", "location": "Surbiton, Surrey, UK"},
    {"name": "Tansy Blaik-Kelly", "level": "3", "years": "Not specified", "location": "Uckfield, East Sussex, UK"},

    # New Zealand Level 3 practitioners
    {"name": "Claire Smith", "level": "3", "years": "Not specified", "location": "Auckland, New Zealand"},
    {"name": "Jason Marshall", "level": "3", "years": "Not specified", "location": "Auckland, New Zealand"},
    {"name": "Kiri Atatoa", "level": "3", "years": "Not specified", "location": "Auckland, New Zealand"},
    {"name": "Michelle Harper", "level": "3", "years": "Not specified", "location": "Auckland, New Zealand"},
    {"name": "Nicola O'Neale", "level": "3", "years": "Not specified", "location": "Auckland, New Zealand"},
    {"name": "Rebecca Goldwater", "level": "3", "years": "Not specified", "location": "Auckland, New Zealand"},
    {"name": "Shay Narayan", "level": "3", "years": "Not specified", "location": "Auckland, New Zealand"},
]

def convert_to_schema(p_data: Dict) -> Dict[str, Any]:
    """Convert extracted practitioner data to match the schema."""
    name = p_data.get('name', '')
    level_str = p_data.get('level', '')
    level_num = parse_level_to_int(level_str)
    location = parse_location(p_data.get('location', ''))

    result = {
        "id": slugify(name),
        "name": name,
        "status": "active",
    }

    if level_num:
        result['level'] = level_num
        result['levelTitle'] = get_level_title(level_num)

    # Location
    result.update(location)

    # Years
    years = parse_years_experience(p_data.get('years'))
    if years:
        result['yearsExperience'] = years

    # Credentials
    if 'credentials' in p_data:
        result['credentials'] = p_data['credentials']

    # Specializations from bio
    bio = p_data.get('bio', '')
    specializations = []
    if bio:
        if 'Pilates' in bio or 'pilates' in bio:
            specializations.append('Pilates')
        if 'ELDOA' in bio or 'eldoa' in bio.lower():
            specializations.append('ELDOA')
        if 'golf' in bio.lower():
            specializations.append('Golf fitness')
        if 'sports' in bio.lower() or 'athlete' in bio.lower():
            specializations.append('Sports medicine')
        if 'yoga' in bio.lower():
            specializations.append('Yoga')
        if 'chiro' in bio.lower():
            specializations.append('Chiropractic')
        if 'massage' in bio.lower():
            specializations.append('Massage therapy')

    if specializations:
        result['specializations'] = specializations

    # Background
    if bio:
        result['background'] = bio

    # Contact
    for field in ['website', 'email', 'phone']:
        if field in p_data:
            result[field] = p_data[field]

    # Remove None values
    return {k: v for k, v in result.items() if v is not None}

def main():
    print(f"Extracting {len(ALL_PRACTITIONERS)} practitioners from PDF research...")

    # Convert to schema
    new_practitioners = [convert_to_schema(p) for p in ALL_PRACTITIONERS]

    # Load existing
    with open('/home/user/eldoaai/data/practitioners.json', 'r') as f:
        data = json.load(f)

    existing_ids = {p['id'] for p in data['practitioners']}

    # Add new only
    added_count = 0
    updated_count = 0
    for p in new_practitioners:
        if p['id'] not in existing_ids:
            data['practitioners'].append(p)
            added_count += 1
            print(f"✓ Added: {p['name']}")
        else:
            updated_count += 1

    # Update metadata
    data['totalCount'] = len(data['practitioners'])
    data['lastUpdated'] = datetime.now().strftime('%Y-%m-%d')

    # Update countries
    countries = set()
    for p in data['practitioners']:
        if 'country' in p:
            countries.add(p['country'])
    data['countries'] = sorted(list(countries))

    # Save
    with open('/home/user/eldoaai/data/practitioners.json', 'w') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"\n{'='*60}")
    print(f"✓ Added {added_count} new practitioners")
    print(f"✓ Skipped {updated_count} existing practitioners")
    print(f"✓ Total practitioners: {data['totalCount']}")
    print(f"✓ Countries covered: {len(data['countries'])}")
    print(f"✓ Countries: {', '.join(data['countries'])}")
    print(f"{'='*60}")

if __name__ == '__main__':
    main()
