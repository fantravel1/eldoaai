#!/usr/bin/env python3
"""
Add structured lists to encyclopedia pages for improved AEO (Answer Engine Optimization)
Answer engines like Google Featured Snippets, Bing AI, and ChatGPT favor bulleted/numbered lists
"""

import os
from pathlib import Path
from bs4 import BeautifulSoup
import re

# Content-specific lists to add to various topic types
LIST_CONTENT = {
    "spine": {
        "benefits": [
            "Creates space between vertebrae",
            "Reduces nerve compression",
            "Improves disc hydration and nutrition",
            "Enhances spinal mobility and flexibility",
            "Promotes better posture and alignment",
            "Relieves chronic tension and pain"
        ],
        "applications": [
            "Daily maintenance for spinal health",
            "Recovery from disc-related issues",
            "Prevention of degenerative changes",
            "Athletic performance enhancement",
            "Post-injury rehabilitation",
            "Chronic pain management"
        ]
    },
    "fascia": {
        "benefits": [
            "Improves tissue hydration and elasticity",
            "Releases fascial restrictions and adhesions",
            "Enhances proprioception and body awareness",
            "Promotes better force transmission",
            "Reduces compensatory movement patterns",
            "Supports overall tissue health"
        ],
        "applications": [
            "Movement quality improvement",
            "Injury prevention strategies",
            "Recovery from fascial restrictions",
            "Athletic performance optimization",
            "Chronic pain management",
            "Postural rehabilitation"
        ]
    },
    "condition": {
        "symptoms": [
            "Pain or discomfort in affected area",
            "Limited range of motion",
            "Muscle tension or stiffness",
            "Compensatory movement patterns",
            "Reduced functional capacity",
            "Impact on daily activities"
        ],
        "protocol": [
            "Start with gentle, modified positions",
            "Practice 3-5 times per week initially",
            "Hold positions for 30-60 seconds",
            "Focus on pain-free ranges of motion",
            "Gradually increase intensity and duration",
            "Monitor progress and adjust as needed"
        ]
    },
    "concept": {
        "key_points": [
            "Fundamental principle in ELDOA practice",
            "Based on scientific understanding of anatomy",
            "Requires precise execution and attention",
            "Progressive learning and skill development",
            "Integration with overall movement practice",
            "Applicable across diverse populations"
        ],
        "practice_tips": [
            "Focus on quality over quantity",
            "Maintain consistent breathing throughout",
            "Pay attention to body positioning",
            "Start slowly and build progressively",
            "Seek qualified instruction when possible",
            "Listen to your body's feedback"
        ]
    },
    "mechanism": {
        "how_it_works": [
            "Creates mechanical stimulus to tissues",
            "Triggers cellular-level responses",
            "Promotes tissue adaptation and remodeling",
            "Enhances neural feedback and learning",
            "Influences fluid dynamics and circulation",
            "Supports long-term structural changes"
        ],
        "evidence": [
            "Supported by biomechanical principles",
            "Clinical observations demonstrate effectiveness",
            "Aligns with current understanding of fascia",
            "Consistent with neuroplasticity research",
            "Validated through practitioner experience",
            "Ongoing research continues to emerge"
        ]
    }
}

def determine_topic_type(title, content):
    """Determine what type of topic this is to select appropriate lists"""
    title_lower = title.lower()
    content_lower = content.lower()

    # Check for spinal/vertebral content
    if any(word in title_lower for word in ['cervical', 'thoracic', 'lumbar', 'sacral', 'spine', 'vertebra', 'l1', 'l2', 'l3', 'l4', 'l5', 't1', 'c1']):
        return 'spine'

    # Check for fascial content
    if any(word in title_lower for word in ['fascia', 'myofascial', 'connective', 'chain', 'tissue']):
        return 'fascia'

    # Check for conditions/pathologies
    if any(word in title_lower for word in ['pain', 'syndrome', 'injury', 'pathology', 'disorder', 'dysfunction', 'tendinopathy', 'scoliosis', 'stenosis']):
        return 'condition'

    # Check for mechanisms
    if any(word in title_lower for word in ['mechanism', 'neuroplasticity', 'transduction', 'adaptation', 'response']):
        return 'mechanism'

    # Default to concept
    return 'concept'

def add_lists_to_page(html_path):
    """Add structured lists to encyclopedia page for better AEO"""
    try:
        with open(html_path, 'r', encoding='utf-8') as f:
            content = f.read()

        soup = BeautifulSoup(content, 'html.parser')

        # Get title
        title_elem = soup.find('h1', class_='entry-title')
        if not title_elem:
            return False

        title = title_elem.get_text()

        # Find the content div
        content_div = soup.find('div', class_='entry-content')
        if not content_div:
            return False

        # Get detailed description section to check content
        detailed_section = content_div.find('div', class_='content-section')
        if not detailed_section:
            return False

        content_text = detailed_section.get_text()

        # Determine topic type
        topic_type = determine_topic_type(title, content_text)

        # Check if lists already exist
        existing_lists = content_div.find_all(['ul', 'ol'])
        # Exclude related-list and connections-list which are navigation
        existing_content_lists = [lst for lst in existing_lists if
                                 'related-list' not in str(lst.get('class', [])) and
                                 'connections-list' not in str(lst.get('class', []))]

        if existing_content_lists:
            # Already has lists, skip
            return False

        # Find where to insert (after detailed description, before related terms)
        detailed_section = None
        for section in content_div.find_all('div', class_='content-section'):
            h2 = section.find('h2')
            if h2 and 'Detailed Description' in h2.get_text():
                detailed_section = section
                break

        if not detailed_section:
            return False

        # Create new section with lists based on topic type
        lists_section = soup.new_tag('div', **{'class': 'content-section'})

        # Add appropriate lists based on topic type
        if topic_type == 'spine':
            # Add benefits list
            benefits_h3 = soup.new_tag('h3')
            benefits_h3.string = 'Key Benefits'
            lists_section.append(benefits_h3)

            benefits_ul = soup.new_tag('ul')
            for benefit in LIST_CONTENT['spine']['benefits']:
                li = soup.new_tag('li')
                li.string = benefit
                benefits_ul.append(li)
            lists_section.append(benefits_ul)

            # Add applications list
            apps_h3 = soup.new_tag('h3')
            apps_h3.string = 'Clinical Applications'
            lists_section.append(apps_h3)

            apps_ul = soup.new_tag('ul')
            for app in LIST_CONTENT['spine']['applications']:
                li = soup.new_tag('li')
                li.string = app
                apps_ul.append(li)
            lists_section.append(apps_ul)

        elif topic_type == 'fascia':
            # Add benefits
            benefits_h3 = soup.new_tag('h3')
            benefits_h3.string = 'Key Benefits'
            lists_section.append(benefits_h3)

            benefits_ul = soup.new_tag('ul')
            for benefit in LIST_CONTENT['fascia']['benefits']:
                li = soup.new_tag('li')
                li.string = benefit
                benefits_ul.append(li)
            lists_section.append(benefits_ul)

            # Add applications
            apps_h3 = soup.new_tag('h3')
            apps_h3.string = 'Practical Applications'
            lists_section.append(apps_h3)

            apps_ul = soup.new_tag('ul')
            for app in LIST_CONTENT['fascia']['applications']:
                li = soup.new_tag('li')
                li.string = app
                apps_ul.append(li)
            lists_section.append(apps_ul)

        elif topic_type == 'condition':
            # Add symptoms/signs
            symptoms_h3 = soup.new_tag('h3')
            symptoms_h3.string = 'Common Signs and Symptoms'
            lists_section.append(symptoms_h3)

            symptoms_ul = soup.new_tag('ul')
            for symptom in LIST_CONTENT['condition']['symptoms']:
                li = soup.new_tag('li')
                li.string = symptom
                symptoms_ul.append(li)
            lists_section.append(symptoms_ul)

            # Add ELDOA protocol
            protocol_h3 = soup.new_tag('h3')
            protocol_h3.string = 'ELDOA Protocol Guidelines'
            lists_section.append(protocol_h3)

            protocol_ol = soup.new_tag('ol')
            for step in LIST_CONTENT['condition']['protocol']:
                li = soup.new_tag('li')
                li.string = step
                protocol_ol.append(li)
            lists_section.append(protocol_ol)

        elif topic_type == 'mechanism':
            # Add how it works
            how_h3 = soup.new_tag('h3')
            how_h3.string = 'How It Works'
            lists_section.append(how_h3)

            how_ul = soup.new_tag('ul')
            for point in LIST_CONTENT['mechanism']['how_it_works']:
                li = soup.new_tag('li')
                li.string = point
                how_ul.append(li)
            lists_section.append(how_ul)

            # Add evidence
            evidence_h3 = soup.new_tag('h3')
            evidence_h3.string = 'Supporting Evidence'
            lists_section.append(evidence_h3)

            evidence_ul = soup.new_tag('ul')
            for item in LIST_CONTENT['mechanism']['evidence']:
                li = soup.new_tag('li')
                li.string = item
                evidence_ul.append(li)
            lists_section.append(evidence_ul)

        else:  # concept
            # Add key points
            points_h3 = soup.new_tag('h3')
            points_h3.string = 'Key Points'
            lists_section.append(points_h3)

            points_ul = soup.new_tag('ul')
            for point in LIST_CONTENT['concept']['key_points']:
                li = soup.new_tag('li')
                li.string = point
                points_ul.append(li)
            lists_section.append(points_ul)

            # Add practice tips
            tips_h3 = soup.new_tag('h3')
            tips_h3.string = 'Practice Tips'
            lists_section.append(tips_h3)

            tips_ul = soup.new_tag('ul')
            for tip in LIST_CONTENT['concept']['practice_tips']:
                li = soup.new_tag('li')
                li.string = tip
                tips_ul.append(li)
            lists_section.append(tips_ul)

        # Insert the new section after detailed description
        detailed_section.insert_after(lists_section)

        # Add CSS for h3 and lists if not already present
        style_tag = soup.find('style')
        if style_tag and 'content-section h3' not in style_tag.string:
            additional_css = """

        .content-section h3 {
            font-size: 1.25rem;
            font-weight: 600;
            color: #2f2fe6;
            margin-top: 1.5rem;
            margin-bottom: 0.75rem;
        }

        .content-section ul,
        .content-section ol {
            margin-left: 1.5rem;
            margin-bottom: 1rem;
        }

        .content-section li {
            margin-bottom: 0.5rem;
            line-height: 1.6;
        }

        .content-section ul li {
            list-style-type: disc;
        }

        .content-section ol li {
            list-style-type: decimal;
        }
"""
            style_tag.string += additional_css

        # Write back to file
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(str(soup))

        return True

    except Exception as e:
        print(f"Error processing {html_path}: {e}")
        return False

def main():
    """Add structured lists to all encyclopedia pages"""
    encyclopedia_dir = Path('/home/user/eldoaai/public/encyclopedia')

    if not encyclopedia_dir.exists():
        print(f"Error: Encyclopedia directory not found at {encyclopedia_dir}")
        return

    html_files = sorted(encyclopedia_dir.glob('*.html'))

    print(f"Found {len(html_files)} encyclopedia pages")
    print("Adding structured lists for AEO optimization...\n")

    success_count = 0
    skipped_count = 0
    error_count = 0

    for i, html_file in enumerate(html_files, 1):
        if html_file.name == 'index.html':
            continue

        result = add_lists_to_page(html_file)

        if result:
            success_count += 1
        elif result is False:
            skipped_count += 1
        else:
            error_count += 1

        if i % 50 == 0:
            print(f"Progress: {i}/{len(html_files)} files processed")
            print(f"Enhanced: {success_count}, Skipped: {skipped_count}, Errors: {error_count}\n")

    print(f"\n{'='*60}")
    print(f"AEO Enhancement Complete!")
    print(f"Total files processed: {len(html_files)}")
    print(f"Successfully enhanced: {success_count}")
    print(f"Skipped (already had lists): {skipped_count}")
    print(f"Errors: {error_count}")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()
