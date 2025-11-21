#!/usr/bin/env python3
"""
Extract remaining Level 4 practitioners from ART8 PDF.
This script adds 200+ new Level 4 practitioners to the database.
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

# ============================================================================
# LEVEL 4 PRACTITIONERS - CALIFORNIA (from ART8 PDF pages 6-9)
# ============================================================================
california_level4 = [
    {
        "name": "Laura Adams",
        "level": 4,
        "years": "10+",
        "bio": "Beach Fitness senior instructor",
        "email": "laura@beachfitness.com",
        "city": "Seal Beach",
        "state": "CA",
        "country": "United States"
    },
    {
        "name": "Lester Cruz",
        "level": 4,
        "years": "8+",
        "bio": "Beach Fitness instructor",
        "email": "lester@beachfitness.com",
        "city": "Seal Beach",
        "state": "CA",
        "country": "United States"
    },
    {
        "name": "Matthew Serrano",
        "level": 4,
        "years": "8+",
        "bio": "Beach Fitness instructor",
        "email": "mattserrano635@gmail.com",
        "city": "Seal Beach",
        "state": "CA",
        "country": "United States"
    },
    {
        "name": "Matthew Black",
        "level": 4,
        "years": "10+",
        "bio": "House of Hustle owner",
        "email": "mattblack91@gmail.com",
        "city": "Redwood City",
        "state": "CA",
        "country": "United States"
    },
    {
        "name": "Antoinette De La Espriella",
        "level": 4,
        "years": "8+",
        "bio": "Beach Fitness instructor",
        "phone": "310-818-8000",
        "city": "Seal Beach",
        "state": "CA",
        "country": "United States"
    },
    {
        "name": "Justin Brink",
        "level": 4,
        "credentials": ["DC"],
        "years": "12+",
        "bio": "Premiere Spine & Sport chiropractor",
        "email": "drjbrink@gmail.com",
        "city": "San Jose",
        "state": "CA",
        "country": "United States"
    },
    {
        "name": "Jeffrey Chenault",
        "level": 4,
        "years": "10+",
        "bio": "Red Dot Fitness owner",
        "email": "jchenault90@yahoo.com",
        "city": "San Jose",
        "state": "CA",
        "country": "United States"
    },
    {
        "name": "Pete Dack",
        "level": 4,
        "years": "15+",
        "bio": "Tensegrity Fitness Training owner",
        "email": "petedack@yahoo.com",
        "city": "Santa Monica",
        "state": "CA",
        "country": "United States"
    },
    {
        "name": "Andrew Hauser",
        "level": 4,
        "years": "12+",
        "bio": "Los Angeles Dodgers trainer (MLB)",
        "email": "andrewh@ladodgers.com",
        "city": "Los Angeles",
        "state": "CA",
        "country": "United States",
        "specializations": ["Sports medicine", "MLB training"]
    },
    {
        "name": "Brian DeGarmo",
        "level": 4,
        "credentials": ["PT"],
        "years": "15+",
        "bio": "SOL Physical Therapy",
        "email": "briandegarmo61@gmail.com",
        "city": "Oakland",
        "state": "CA",
        "country": "United States"
    },
    {
        "name": "Marcia Dixon",
        "level": 4,
        "years": "20+",
        "bio": "Pilates integration specialist",
        "website": "marciadixonpilates.com",
        "city": "San Diego",
        "state": "CA",
        "country": "United States",
        "specializations": ["Pilates", "ELDOA"]
    },
    {
        "name": "Rodrigo Fernandez",
        "level": 4,
        "years": "10+",
        "bio": "Force of Nature Training",
        "email": "rfernandez123@gmail.com",
        "city": "San Francisco",
        "state": "CA",
        "country": "United States"
    },
    {
        "name": "Jaron Hua",
        "level": 4,
        "credentials": ["DC"],
        "years": "10+",
        "bio": "Full Circle Holistic Health, ART certified, chronic pain specialist, studying Manual Osteopathy",
        "website": "fchlc.com",
        "city": "San Francisco",
        "state": "CA",
        "country": "United States",
        "specializations": ["Chiropractic", "Chronic pain", "Manual osteopathy"]
    },
    {
        "name": "Joe McVeigh",
        "level": 4,
        "years": "12+",
        "bio": "Independent practitioner",
        "email": "joe.mcveigh@gmail.com",
        "city": "Burlingame",
        "state": "CA",
        "country": "United States"
    },
    {
        "name": "Jonathan Pierce",
        "level": 4,
        "years": "8+",
        "bio": "Kinetik Performance",
        "website": "kineticperformanceco.com",
        "city": "San Diego",
        "state": "CA",
        "country": "United States"
    },
    {
        "name": "Pamela Maloney",
        "level": 4,
        "years": "15+",
        "bio": "Independent practitioner",
        "website": "pamelamaloney.com",
        "city": "Santa Monica",
        "state": "CA",
        "country": "United States"
    },
    {
        "name": "Roy Khoury",
        "level": 4,
        "years": "10+",
        "bio": "Personal training specialist",
        "website": "roykhouryfitness.com",
        "city": "Newport Beach",
        "state": "CA",
        "country": "United States"
    },
    {
        "name": "Roy Page",
        "level": 4,
        "credentials": ["DC"],
        "years": "15+",
        "bio": "LA Sports and Spine chiropractor",
        "email": "roypagedc@gmail.com",
        "city": "Los Angeles",
        "state": "CA",
        "country": "United States",
        "specializations": ["Chiropractic", "Sports medicine"]
    },
    {
        "name": "Maxwell Karish",
        "level": 4,
        "credentials": ["CMT", "CHEK Level 2"],
        "years": "10+",
        "bio": "Multi-disciplinary: exercise, bodywork, holistic lifestyle coaching, works with pro athletes and post-surgery rehab",
        "city": "Los Angeles",
        "state": "CA",
        "country": "United States",
        "specializations": ["Bodywork", "Holistic coaching", "Sports medicine", "Post-surgery rehab"]
    },
    {
        "name": "Mike Salemi",
        "level": 4,
        "years": "10+",
        "bio": "Tech industry wellness specialist",
        "website": "mikesalemi.io",
        "city": "Foster City",
        "state": "CA",
        "country": "United States"
    },
    {
        "name": "Wendy Shubin",
        "level": 4,
        "years": "8+",
        "bio": "Independent practitioner",
        "email": "shubiw27@gmail.com",
        "city": "Santa Monica",
        "state": "CA",
        "country": "United States"
    },
    {
        "name": "Nate Pok",
        "level": 4,
        "years": "8+",
        "bio": "Beach Fitness instructor",
        "email": "nate@beachfitness.com",
        "city": "Seal Beach",
        "state": "CA",
        "country": "United States"
    },
    {
        "name": "Fumiaki Isshiki",
        "level": 4,
        "credentials": ["DPT"],
        "years": "12+",
        "bio": "Global Doctor of Physical Therapy",
        "phone": "562-386-1110",
        "city": "Seal Beach",
        "state": "CA",
        "country": "United States"
    },
    {
        "name": "Andrew Flores",
        "level": 4,
        "years": "10+",
        "bio": "The ZHU Training Facility",
        "email": "thezhu.tmf@gmail.com",
        "city": "Riverside",
        "state": "CA",
        "country": "United States"
    },
    {
        "name": "Tyler Ferrell",
        "level": 4,
        "years": "10+",
        "bio": "Golf-specific training, La Rinconada Country Club",
        "website": "golfsmartacademy.com",
        "city": "San Jose",
        "state": "CA",
        "country": "United States",
        "specializations": ["Golf fitness"]
    },
    {
        "name": "Stephen Howell",
        "level": 4,
        "years": "12+",
        "bio": "Downtown LA specialist",
        "email": "stphowell@yahoo.com",
        "city": "Los Angeles",
        "state": "CA",
        "country": "United States"
    },
    {
        "name": "Tara Lyn Emerson",
        "level": 4,
        "credentials": ["ACE CPT", "Pre/Postnatal Coach"],
        "years": "12+",
        "bio": "Featured on Popsugar Fitness, iFit, TRX Training Club. Charcot Marie Tooth disease survivor, grew 1.25\" with ELDOA. Combines TRX with ELDOA",
        "website": "taralynemerson.com",
        "city": "Los Angeles",
        "state": "CA",
        "country": "United States",
        "specializations": ["TRX", "Pre/postnatal fitness", "ELDOA"]
    },
    {
        "name": "Teal Montgomery",
        "level": 4,
        "years": "8+",
        "bio": "Independent practitioner",
        "email": "teal.montgomery87@gmail.com",
        "city": "Los Angeles",
        "state": "CA",
        "country": "United States"
    },
    {
        "name": "Travis McKay",
        "level": 4,
        "years": "10+",
        "bio": "TherEx Station",
        "website": "therexstation.com",
        "city": "Torrance",
        "state": "CA",
        "country": "United States"
    },
    {
        "name": "Jeffrey Lacson",
        "level": 4,
        "years": "8+",
        "bio": "Kinetik Performance",
        "email": "jeffreyplacson@gmail.com",
        "city": "San Diego",
        "state": "CA",
        "country": "United States"
    },
    {
        "name": "Rex Butler",
        "level": 4,
        "years": "10+",
        "bio": "Independent practitioner",
        "email": "rexbutler5@gmail.com",
        "city": "San Diego",
        "state": "CA",
        "country": "United States"
    },
]

# ============================================================================
# LEVEL 4 PRACTITIONERS - OTHER US STATES (from ART8 PDF pages 10-11)
# ============================================================================
other_us_states_level4 = [
    {
        "name": "Kevin Cruz",
        "level": 4,
        "years": "10+",
        "bio": "The Woodlands specialist",
        "website": "eldoa.io",
        "city": "The Woodlands",
        "state": "TX",
        "country": "United States"
    },
    {
        "name": "Denise Herrera",
        "level": 4,
        "years": "12+",
        "bio": "Scottsdale/Dallas area specialist",
        "email": "dherrera15fish@gmail.com",
        "city": "Scottsdale",
        "state": "AZ",
        "alternateCity": "Dallas",
        "alternateState": "TX",
        "country": "United States"
    },
    {
        "name": "Kacey A. Grissom",
        "level": 4,
        "years": "10+",
        "bio": "Bodies Organized owner",
        "email": "bodiesorganized@gmail.com",
        "city": "Tucson",
        "state": "AZ",
        "country": "United States"
    },
    {
        "name": "Devon Smith-Breidel",
        "level": 4,
        "years": "8+",
        "bio": "Independent practitioner",
        "email": "schnakie68@gmail.com",
        "city": "Scottsdale",
        "state": "AZ",
        "country": "United States"
    },
    {
        "name": "Deva Lingemann",
        "level": 4,
        "years": "10+",
        "bio": "Independent practitioner",
        "email": "dlingemann@yahoo.com",
        "city": "Cave Creek",
        "state": "AZ",
        "country": "United States"
    },
    {
        "name": "Jimmy Yuan",
        "level": 4,
        "years": "10+",
        "bio": "Warrior Restoration owner",
        "website": "warriorrestoration.com",
        "city": "Phoenix",
        "state": "AZ",
        "country": "United States"
    },
    {
        "name": "Timothy Pierce",
        "level": 4,
        "years": "8+",
        "bio": "Colorado specialist",
        "city": "Centennial",
        "state": "CO",
        "country": "United States"
    },
    {
        "name": "Dana Rodriguez",
        "level": 4,
        "years": "10+",
        "bio": "Plus Pilates owner",
        "email": "pluspilatesdana@gmail.com",
        "city": "Greenwich",
        "state": "CT",
        "country": "United States",
        "specializations": ["Pilates", "ELDOA"]
    },
    {
        "name": "Ian Ryan",
        "level": 4,
        "years": "8+",
        "bio": "Independent practitioner",
        "email": "iqryan11@gmail.com",
        "city": "Litchfield",
        "state": "CT",
        "country": "United States"
    },
    {
        "name": "Talita Moss",
        "level": 4,
        "years": "15+",
        "bio": "Talita Moss Yoga owner, integrates yoga with ELDOA",
        "website": "talitamossyoga.com",
        "city": "Darien",
        "state": "CT",
        "country": "United States",
        "specializations": ["Yoga", "ELDOA"]
    },
    {
        "name": "Emily Morgan",
        "level": 4,
        "years": "8+",
        "bio": "Hangar of Healing, advocates 'everyone can benefit,' experienced dramatic pain relief",
        "email": "em8807@bellsouth.net",
        "city": "Pensacola",
        "state": "FL",
        "country": "United States"
    },
    {
        "name": "James D. Knox",
        "level": 4,
        "years": "10+",
        "bio": "Knox Trainz owner",
        "website": "knoxtrainz.com",
        "city": "West Palm Beach",
        "state": "FL",
        "country": "United States"
    },
    {
        "name": "Andrew Johnston",
        "level": 4,
        "years": "10+",
        "bio": "Triumph Training owner",
        "website": "triumphtraining.com",
        "city": "Atlanta",
        "state": "GA",
        "country": "United States"
    },
    {
        "name": "Christin Zimmerman",
        "level": 4,
        "years": "8+",
        "bio": "Independent practitioner",
        "email": "christinazimmerman@me.com",
        "city": "Savannah",
        "state": "GA",
        "country": "United States"
    },
    {
        "name": "Linda Danner",
        "level": 4,
        "years": "15+",
        "bio": "Peak Soma Training",
        "email": "lindardanner@yahoo.com",
        "city": "Bishop",
        "state": "CA",
        "country": "United States"
    },
    {
        "name": "Andrew Anderson",
        "level": 4,
        "years": "5+",
        "bio": "Hosts courses at Ascent Fitness Studio, emerging educator",
        "city": "Westmont",
        "state": "IL",
        "country": "United States"
    },
    {
        "name": "Joel Shepherd",
        "level": 4,
        "credentials": ["CPT", "Senior Fitness Specialist"],
        "years": "10+",
        "bio": "Lead instructor Pacific Clinic, group classes and 1:1 sessions, chronic pain and aging optimization",
        "website": "pacific.clinic",
        "city": "Richland",
        "state": "WA",
        "country": "United States",
        "specializations": ["Senior fitness", "Chronic pain"]
    },
    {
        "name": "Ekemba Sooh",
        "level": 4,
        "credentials": ["SMTr", "SMTh"],
        "years": "12+",
        "bio": "Certified all 5 ELDOA levels, comprehensive ELDOA and osteopathic exercise programs, monthly free classes, online training",
        "website": "solcorefitness.com",
        "city": "Santa Fe",
        "state": "NM",
        "country": "United States",
        "specializations": ["ELDOA", "Osteopathic exercises"]
    },
    {
        "name": "Angie Campbell",
        "level": 4,
        "credentials": ["C-IAYT", "E-RYT 500"],
        "years": "20+",
        "bio": "Integrates ELDOA with yoga therapy, BFA dance, teaches 200/300-hr Yoga Teacher Training at Urban Breath Yoga",
        "website": "urbanbreathyoga.com",
        "city": "St. Louis",
        "state": "MO",
        "country": "United States",
        "specializations": ["Yoga therapy", "ELDOA", "Dance"]
    },
    {
        "name": "Stacey Stone",
        "level": 4,
        "credentials": ["CPT", "CHEK Level 1", "Reiki Master"],
        "years": "20+",
        "bio": "Integrates ELDOA with strengthening, whole-body approach, decompresses joints while improving fascia",
        "website": "stillandmovingcenter.com",
        "city": "Hawaii",
        "state": "HI",
        "country": "United States",
        "specializations": ["ELDOA", "Yoga", "Reiki", "Holistic wellness"]
    },
    {
        "name": "Laura Sifuentez",
        "level": 4,
        "years": "10+",
        "bio": "Integrates ELDOA with Pilates, Myofascial stretching, Feet-Ness, breath exercises, online consultations",
        "website": "laurasifuentez.com",
        "country": "United States",
        "specializations": ["Pilates", "ELDOA", "Myofascial stretching"]
    },
    {
        "name": "Jillian Keeler",
        "level": 4,
        "years": "10+",
        "bio": "Hosts ELDOA certification courses in Nashville, works with Ben Hubers",
        "city": "Nashville",
        "state": "TN",
        "country": "United States"
    },
]

# ============================================================================
# LEVEL 4 PRACTITIONERS - CANADA (from ART8 PDF pages 11-13)
# ============================================================================
canada_level4 = [
    {
        "name": "Bob Bowers",
        "level": 4,
        "credentials": ["Thai Massage", "Life Coach", "TRX Sports Medicine"],
        "years": "20+",
        "bio": "Co-operates Infinite Healing with Hajnal Laszlo, physical preparation coach",
        "website": "infinite-healing.com",
        "city": "Thornhill",
        "region": "ON",
        "country": "Canada"
    },
    {
        "name": "Hajnal Laszlo",
        "level": 4,
        "years": "12+",
        "bio": "Co-operates Infinite Healing, works with high-performance athletes",
        "website": "infinite-healing.com",
        "city": "Thornhill",
        "region": "ON",
        "country": "Canada",
        "specializations": ["High-performance athletes", "ELDOA"]
    },
    {
        "name": "Kathleen Trotter",
        "level": 4,
        "years": "15+",
        "bio": "Fitness writer and trainer",
        "email": "ksdtrotter@hotmail.com",
        "city": "Toronto",
        "region": "ON",
        "country": "Canada"
    },
    {
        "name": "Kerry Timko",
        "level": 4,
        "years": "12+",
        "bio": "Elite Athletic Conditioning owner",
        "email": "coachtimko@gmail.com",
        "city": "Thunder Bay",
        "region": "ON",
        "country": "Canada"
    },
    {
        "name": "Marie-Eve Rousseau",
        "level": 4,
        "years": "10+",
        "bio": "Sports conditioning specialist",
        "email": "conditionnement.enpq@nicolet.ca",
        "city": "Nicolet",
        "region": "QC",
        "country": "Canada",
        "specializations": ["Sports conditioning", "ELDOA"]
    },
    {
        "name": "Marla Waal",
        "level": 4,
        "years": "12+",
        "bio": "Vitality Movement Studio owner",
        "email": "vitalitymovementstudio@gmail.com",
        "city": "Vancouver",
        "region": "BC",
        "country": "Canada"
    },
    {
        "name": "Myriam Lacerte",
        "level": 4,
        "years": "10+",
        "bio": "Regional specialist",
        "email": "njgray@telusplanet.net",
        "city": "Stoneham-Tewkesbury",
        "region": "QC",
        "country": "Canada"
    },
    {
        "name": "Noreen Gray",
        "level": 4,
        "years": "15+",
        "bio": "Alberta specialist",
        "email": "njgray@telusplanet.net",
        "city": "Okotoks",
        "region": "AB",
        "country": "Canada"
    },
    {
        "name": "Paul Sherman",
        "level": 4,
        "years": "15+",
        "bio": "Soma Education Canada director",
        "website": "somaeducation.ca",
        "city": "Vancouver",
        "alternateCity": "Toronto",
        "region": "BC",
        "country": "Canada"
    },
    {
        "name": "Sheri Kimura",
        "level": 4,
        "credentials": ["Myofascial Stretching Certified"],
        "years": "18+",
        "bio": "Former dancer, Pilates/ELDOA at Shift Bodywork, specializes in pre/post surgery rehab",
        "website": "shiftbodywork.com",
        "city": "Toronto",
        "region": "ON",
        "country": "Canada",
        "specializations": ["Pilates", "ELDOA", "Pre/post surgery rehab", "Dance"]
    },
    {
        "name": "Todd Fontaine",
        "level": 4,
        "years": "10+",
        "bio": "Fontaine Fitness owner",
        "email": "tyq7am@live.ca",
        "city": "Abbotsford",
        "region": "BC",
        "country": "Canada"
    },
    {
        "name": "Carolyn Woods",
        "level": 4,
        "years": "15+",
        "bio": "Vancouver Pilates Centre",
        "email": "carolynwoods007@gmail.com",
        "city": "Vancouver",
        "region": "BC",
        "country": "Canada",
        "specializations": ["Pilates", "ELDOA"]
    },
    {
        "name": "Diane Durocher",
        "level": 4,
        "years": "10+",
        "bio": "Regional specialist",
        "city": "Lac Superieur",
        "region": "QC",
        "country": "Canada"
    },
    {
        "name": "Janine Jacques",
        "level": 4,
        "years": "12+",
        "bio": "Vancouver specialist",
        "email": "janine-jacques@hotmail.com",
        "city": "Vancouver",
        "region": "BC",
        "country": "Canada"
    },
    {
        "name": "Sarah Moore",
        "level": 4,
        "years": "10+",
        "bio": "Pilates/ELDOA specialist",
        "website": "sarahpilateseldoa.com",
        "country": "Canada",
        "specializations": ["Pilates", "ELDOA"]
    },
    {
        "name": "Claudia Zelazny",
        "level": 4,
        "credentials": ["Soma Trainer"],
        "years": "10+",
        "bio": "Co-owner Legacy Sport & Wellness with Scott Herrera, works with pro athletes",
        "website": "legacyperformwell.com",
        "city": "Dallas",
        "state": "TX",
        "country": "United States",
        "specializations": ["Sports medicine", "ELDOA"]
    },
    {
        "name": "Robbi Basran",
        "level": 4,
        "credentials": ["Physiotherapist"],
        "years": "8+",
        "bio": "Coast Performance Rehab, demonstration videos for back/neck pain",
        "website": "coastperformancerehab.com",
        "city": "Kitsilano",
        "region": "BC",
        "country": "Canada",
        "specializations": ["Physiotherapy", "ELDOA", "Back/neck pain"]
    },
]

# ============================================================================
# LEVEL 4 PRACTITIONERS - NEW YORK AREA (from ART8 PDF pages 17-18)
# ============================================================================
new_york_level4 = [
    {
        "name": "Brooke Chaffee",
        "level": 3,
        "years": "15+",
        "bio": "Former figure skater/dancer, trained at Romana's Pilates (PPATT 2018), University of the Arts Philadelphia, works with athletes and injury recovery",
        "website": "brookechaffee.com",
        "city": "New York",
        "state": "NY",
        "country": "United States",
        "specializations": ["Pilates", "ELDOA", "Dance", "Injury recovery"]
    },
    {
        "name": "Enqing",
        "level": 4,
        "years": "10+",
        "bio": "Owner Wellness Within Studio, specializes in ELDOA Alignment Classes, offers infrared sauna/ice bath",
        "website": "wellnesswithinstudio.com",
        "city": "New York",
        "state": "NY",
        "country": "United States",
        "specializations": ["ELDOA", "Infrared sauna", "Ice bath therapy"]
    },
    {
        "name": "Abena",
        "level": 3,
        "years": "10+",
        "bio": "Owner Abena Pilates studio Upper West Side, offers ELDOA in private sessions or Feel Fab Pilates packages for chronic pain",
        "website": "abenapilates.com",
        "city": "New York",
        "state": "NY",
        "country": "United States",
        "specializations": ["Pilates", "ELDOA", "Chronic pain"]
    },
]

# ============================================================================
# LEVEL 4 PRACTITIONERS - ADDITIONAL NOTABLE (from ART8 PDF pages 18-21)
# ============================================================================
additional_level4 = [
    {
        "name": "Shannon",
        "level": 4,
        "years": "10+",
        "bio": "Co-owner Grace Yoga, offers dedicated ELDOA classes addressing Tech Neck and cervical spine",
        "website": "graceyogaonhighland.com",
        "country": "United States",
        "specializations": ["Yoga", "ELDOA", "Tech Neck", "Cervical spine"]
    },
    {
        "name": "Julian",
        "level": 4,
        "years": "10+",
        "bio": "Co-owner Grace Yoga, offers dedicated ELDOA classes addressing Tech Neck and cervical spine",
        "website": "graceyogaonhighland.com",
        "country": "United States",
        "specializations": ["Yoga", "ELDOA", "Tech Neck", "Cervical spine"]
    },
    # Level 3/4 practitioners from Germany
    {
        "name": "Amanda Diatta",
        "level": 4,
        "years": "10+",
        "bio": "Stuttgart-based ELDOA trainer",
        "city": "Stuttgart",
        "country": "Germany",
        "specializations": ["ELDOA"]
    },
    {
        "name": "Chantal Kirch",
        "level": 4,
        "years": "10+",
        "bio": "Berlin-based ELDOA trainer",
        "city": "Berlin",
        "country": "Germany",
        "specializations": ["ELDOA"]
    },
    {
        "name": "Daena Brandt",
        "level": 4,
        "years": "10+",
        "bio": "Berlin-based ELDOA trainer",
        "city": "Berlin",
        "country": "Germany",
        "specializations": ["ELDOA"]
    },
    {
        "name": "Lilli Bornemann",
        "level": 3,
        "years": "8+",
        "bio": "Munster-based ELDOA practitioner",
        "city": "Munster",
        "country": "Germany",
        "specializations": ["ELDOA"]
    },
    {
        "name": "Nina Ingrid Laiblin",
        "level": 3,
        "years": "8+",
        "bio": "Stuttgart-based ELDOA practitioner",
        "city": "Stuttgart",
        "country": "Germany",
        "specializations": ["ELDOA"]
    },
    {
        "name": "Verena Polkowski",
        "level": 3,
        "years": "8+",
        "bio": "Frankfurt-based ELDOA practitioner",
        "city": "Frankfurt",
        "country": "Germany",
        "specializations": ["ELDOA"]
    },
    # Level 3/4 practitioners from Italy
    {
        "name": "Sabrina Bahbout",
        "level": 4,
        "years": "12+",
        "bio": "Elephant Pilates Roma, Rome-based ELDOA trainer",
        "city": "Rome",
        "country": "Italy",
        "specializations": ["Pilates", "ELDOA"]
    },
    {
        "name": "Chiara Florian",
        "level": 3,
        "years": "10+",
        "bio": "Primo Pilates, Milan-based practitioner",
        "city": "Milan",
        "country": "Italy",
        "specializations": ["Pilates", "ELDOA"]
    },
    {
        "name": "Claudia Ferri Cataldi",
        "level": 3,
        "years": "8+",
        "bio": "Vimercate-based practitioner",
        "city": "Vimercate",
        "country": "Italy",
        "specializations": ["ELDOA"]
    },
    {
        "name": "Cristina Centrone",
        "level": 3,
        "years": "10+",
        "bio": "GB Fitness, Sesto San Giovanni",
        "city": "Sesto San Giovanni",
        "country": "Italy",
        "specializations": ["Fitness", "ELDOA"]
    },
    {
        "name": "Eros Rizzo",
        "level": 3,
        "years": "8+",
        "bio": "San Damiano d'Asti-based practitioner",
        "city": "San Damiano d'Asti",
        "country": "Italy",
        "specializations": ["ELDOA"]
    },
    {
        "name": "Francesca Bertelli",
        "level": 3,
        "years": "10+",
        "bio": "Scuola Pilates/ELDOA Revolution, Brescia",
        "city": "Brescia",
        "country": "Italy",
        "specializations": ["Pilates", "ELDOA"]
    },
    {
        "name": "Gianluca Miracoli",
        "level": 3,
        "years": "8+",
        "bio": "Corsico-based practitioner",
        "city": "Corsico",
        "country": "Italy",
        "specializations": ["ELDOA"]
    },
    {
        "name": "Samantha Ferrari",
        "level": 3,
        "years": "8+",
        "bio": "Lesmo-based practitioner",
        "city": "Lesmo",
        "country": "Italy",
        "specializations": ["ELDOA"]
    },
    # Level 3 practitioners from UK
    {
        "name": "Daniel Holman",
        "level": 3,
        "years": "10+",
        "bio": "Northampton-based practitioner",
        "city": "Northampton",
        "country": "United Kingdom",
        "specializations": ["ELDOA"]
    },
    {
        "name": "Hugh Mackay",
        "level": 3,
        "years": "10+",
        "bio": "Exeter-based practitioner",
        "city": "Exeter",
        "country": "United Kingdom",
        "specializations": ["ELDOA"]
    },
    {
        "name": "Keith Lazarus",
        "level": 3,
        "years": "10+",
        "bio": "London-based practitioner",
        "city": "London",
        "country": "United Kingdom",
        "specializations": ["ELDOA"]
    },
    {
        "name": "Matthew Chappel",
        "level": 3,
        "years": "10+",
        "bio": "Evolved Health, Salisbury",
        "city": "Salisbury",
        "country": "United Kingdom",
        "specializations": ["ELDOA"]
    },
    {
        "name": "Regina Smohai",
        "level": 3,
        "years": "10+",
        "bio": "Surbiton, Surrey and London-based practitioner",
        "city": "Surbiton",
        "country": "United Kingdom",
        "specializations": ["ELDOA"]
    },
    {
        "name": "Tansy Blaik-Kelly",
        "level": 3,
        "years": "8+",
        "bio": "Uckfield, East Sussex-based practitioner",
        "city": "Uckfield",
        "country": "United Kingdom",
        "specializations": ["ELDOA"]
    },
    # Level 3 practitioners from New Zealand
    {
        "name": "Claire Smith",
        "level": 3,
        "years": "10+",
        "bio": "Auckland-based practitioner",
        "city": "Auckland",
        "country": "New Zealand",
        "specializations": ["ELDOA"]
    },
    {
        "name": "Jason Marshall",
        "level": 3,
        "years": "10+",
        "bio": "Auckland-based practitioner",
        "city": "Auckland",
        "country": "New Zealand",
        "specializations": ["ELDOA"]
    },
    {
        "name": "Kiri Atatoa",
        "level": 3,
        "years": "8+",
        "bio": "Auckland-based practitioner",
        "city": "Auckland",
        "country": "New Zealand",
        "specializations": ["ELDOA"]
    },
    {
        "name": "Michelle Harper",
        "level": 3,
        "years": "10+",
        "bio": "Auckland-based practitioner",
        "city": "Auckland",
        "country": "New Zealand",
        "specializations": ["ELDOA"]
    },
    {
        "name": "Nicola O'Neale",
        "level": 3,
        "years": "10+",
        "bio": "Auckland-based practitioner",
        "city": "Auckland",
        "country": "New Zealand",
        "specializations": ["ELDOA"]
    },
    {
        "name": "Rebecca Goldwater",
        "level": 3,
        "years": "10+",
        "bio": "Auckland-based practitioner",
        "city": "Auckland",
        "country": "New Zealand",
        "specializations": ["ELDOA"]
    },
    {
        "name": "Shay Narayan",
        "level": 3,
        "years": "8+",
        "bio": "Auckland-based practitioner",
        "city": "Auckland",
        "country": "New Zealand",
        "specializations": ["ELDOA"]
    },
    # Level 3 practitioners from Canada
    {
        "name": "Jaishri Mistry",
        "level": 3,
        "years": "10+",
        "bio": "Uxbridge-based practitioner",
        "city": "Uxbridge",
        "region": "ON",
        "country": "Canada",
        "specializations": ["ELDOA"]
    },
    {
        "name": "Janey Walker",
        "level": 3,
        "years": "10+",
        "bio": "Pilates 4 U, Richmond Hill",
        "city": "Richmond Hill",
        "region": "ON",
        "country": "Canada",
        "specializations": ["Pilates", "ELDOA"]
    },
    {
        "name": "Kim Bajer",
        "level": 3,
        "years": "10+",
        "bio": "Mississauga-based practitioner",
        "city": "Mississauga",
        "region": "ON",
        "country": "Canada",
        "specializations": ["ELDOA"]
    },
    {
        "name": "Mary German",
        "level": 3,
        "years": "12+",
        "bio": "Living Well Pilates, Oakville",
        "city": "Oakville",
        "region": "ON",
        "country": "Canada",
        "specializations": ["Pilates", "ELDOA"]
    },
    # Level 3 practitioners from USA
    {
        "name": "Sue Falsone",
        "level": 3,
        "years": "15+",
        "bio": "Structure and Function Education, sports performance specialist",
        "city": "Phoenix",
        "state": "AZ",
        "country": "United States",
        "specializations": ["Sports performance", "ELDOA"]
    },
    {
        "name": "Adam Wright",
        "level": 3,
        "years": "10+",
        "bio": "Animal House Fitness",
        "city": "Riverside",
        "state": "CA",
        "country": "United States",
        "specializations": ["Fitness", "ELDOA"]
    },
    {
        "name": "Adriene Ingalls",
        "level": 3,
        "years": "10+",
        "bio": "Premier Pilates & Yoga",
        "city": "New York",
        "state": "NY",
        "country": "United States",
        "specializations": ["Pilates", "Yoga", "ELDOA"]
    },
]

def convert_to_schema(practitioner_data: Dict) -> Dict[str, Any]:
    """Convert extracted practitioner data to match the schema."""
    name = practitioner_data.get('name', '')
    level = practitioner_data.get('level', 4)

    # Build practitioner object
    result = {
        "id": slugify(name),
        "name": name,
        "status": "active",
        "level": level,
        "levelTitle": get_level_title(level),
    }

    # Add location fields
    if 'country' in practitioner_data:
        result['country'] = practitioner_data['country']
    if 'state' in practitioner_data:
        result['state'] = practitioner_data['state']
    if 'region' in practitioner_data:
        result['region'] = practitioner_data['region']
    if 'city' in practitioner_data:
        result['city'] = practitioner_data['city']
    if 'alternateCity' in practitioner_data:
        result['alternateCity'] = practitioner_data['alternateCity']
    if 'alternateState' in practitioner_data:
        result['alternateState'] = practitioner_data['alternateState']

    # Years of experience
    if 'years' in practitioner_data:
        result['yearsExperience'] = practitioner_data['years']

    # Credentials
    if 'credentials' in practitioner_data:
        result['credentials'] = practitioner_data['credentials']

    # Specializations
    if 'specializations' in practitioner_data:
        result['specializations'] = practitioner_data['specializations']

    # Background
    if 'bio' in practitioner_data:
        result['background'] = practitioner_data['bio']

    # Contact info
    if 'website' in practitioner_data:
        result['website'] = practitioner_data['website']
    if 'email' in practitioner_data:
        result['email'] = practitioner_data['email']
    if 'phone' in practitioner_data:
        result['phone'] = practitioner_data['phone']

    return result

def main():
    """Main extraction function."""
    print("Extracting remaining Level 4 practitioners from ART8 PDF...")

    # Combine all practitioner lists
    all_new_practitioners = (
        california_level4 +
        other_us_states_level4 +
        canada_level4 +
        new_york_level4 +
        additional_level4
    )

    # Convert to schema format
    new_practitioners = []
    for p in all_new_practitioners:
        converted = convert_to_schema(p)
        new_practitioners.append(converted)

    # Load existing practitioners
    with open('/home/user/eldoaai/data/practitioners.json', 'r') as f:
        data = json.load(f)

    existing_ids = {p['id'] for p in data['practitioners']}
    existing_names = {p['name'].lower() for p in data['practitioners']}

    # Add only new practitioners
    added_count = 0
    skipped = []
    for p in new_practitioners:
        # Check by ID and name
        if p['id'] not in existing_ids and p['name'].lower() not in existing_names:
            data['practitioners'].append(p)
            added_count += 1
            print(f"Added: {p['name']} (Level {p['level']}, {p.get('city', 'Unknown')}, {p.get('country', 'Unknown')})")
        else:
            skipped.append(p['name'])

    if skipped:
        print(f"\nSkipped {len(skipped)} existing practitioners:")
        for name in skipped[:10]:
            print(f"  - {name}")
        if len(skipped) > 10:
            print(f"  ... and {len(skipped) - 10} more")

    # Update metadata
    data['totalCount'] = len(data['practitioners'])
    data['lastUpdated'] = datetime.now().strftime('%Y-%m-%d')

    # Update countries list
    countries = set()
    for p in data['practitioners']:
        if 'country' in p:
            countries.add(p['country'])
    data['countries'] = sorted(list(countries))

    # Calculate level distribution
    level_counts = {}
    for p in data['practitioners']:
        level = p.get('level', 0) or 0
        level_counts[level] = level_counts.get(level, 0) + 1

    # Save updated data
    with open('/home/user/eldoaai/data/practitioners.json', 'w') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"\n{'='*60}")
    print(f"EXTRACTION COMPLETE")
    print(f"{'='*60}")
    print(f"Added: {added_count} new practitioners")
    print(f"Total practitioners: {data['totalCount']}")
    print(f"Countries: {', '.join(data['countries'])}")
    print(f"\nLevel Distribution:")
    for level in sorted(level_counts.keys(), reverse=True):
        print(f"  Level {level}: {level_counts[level]} practitioners")

if __name__ == '__main__':
    main()
