#!/usr/bin/env python3
"""
Extract encyclopedia entries from PDFs and create individual HTML files
"""

import os
import re
import PyPDF2
from pathlib import Path
from collections import defaultdict
import json

# Paths
ENCYCLOPEDIA_PDF_DIR = "/home/user/eldoaai/downloads/encyclopedia"
OUTPUT_HTML_DIR = "/home/user/eldoaai/public/encyclopedia"
OUTPUT_DATA_FILE = "/home/user/eldoaai/public/encyclopedia-data.json"

def extract_text_from_pdf(pdf_path):
    """Extract text from a PDF file"""
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            return text
    except Exception as e:
        print(f"Error reading {pdf_path}: {e}")
        return ""

def parse_entries(text):
    """Parse encyclopedia entries from text"""
    entries = []

    # Split by lines
    lines = text.split('\n')

    current_title = None
    current_content = []
    skip_headers = ['PILLAR', 'POCKETBOOK', 'ENCLOPEDIA', 'ENCYCLOPEDIA', 'WIKI']

    i = 0
    while i < len(lines):
        line = lines[i].strip()

        # Skip empty lines
        if not line:
            i += 1
            continue

        # Skip known headers
        if any(header in line for header in skip_headers):
            i += 1
            continue

        # Skip single letter headers (A, B, C, etc.)
        if len(line) == 1 and line.isalpha() and line.isupper():
            i += 1
            continue

        # Check if this is a title line (contains a colon early in the line)
        colon_pos = line.find(':')
        if colon_pos > 0 and colon_pos < 100:  # Title with colon
            potential_title = line[:colon_pos].strip()

            # Filter out obvious non-titles
            if (potential_title and
                not potential_title.startswith('http') and
                not any(skip in potential_title for skip in skip_headers)):

                # Save previous entry if exists
                if current_title and current_content:
                    content_text = ' '.join(current_content).strip()
                    if content_text:  # Only add if there's actual content
                        entries.append({
                            'title': current_title,
                            'content': content_text
                        })

                # Start new entry
                current_title = potential_title
                content_after_colon = line[colon_pos+1:].strip()
                current_content = [content_after_colon] if content_after_colon else []
            else:
                # Not a title, add to current content
                if current_title is not None:
                    current_content.append(line)
        else:
            # Regular content line
            if current_title is not None:
                current_content.append(line)

        i += 1

    # Don't forget the last entry
    if current_title and current_content:
        content_text = ' '.join(current_content).strip()
        if content_text:
            entries.append({
                'title': current_title,
                'content': content_text
            })

    return entries

def highlight_yellow_terms(content):
    """
    Identify terms that should be highlighted in yellow based on patterns
    This is a heuristic approach - we'll highlight important phrases
    """
    # Common patterns that were highlighted in the original
    patterns = [
        r'(Making sure all the bones in your body line up properly, like stacking blocks perfectly straight\.)',
        r'(Keeping the cushions between your back bones healthy\. These cushions are like jelly donuts that need to stay plump!)',
        r'(Learning about how your body works and why the exercises help\. The more you understand, the better you can take care of yourself!)',
        r'(A web of tissue that wraps around all your muscles and organs like plastic wrap\.)',
        r'(Using the fascia web to create helpful stretching in your body\.)',
        r'(Lines of connected muscles and fascia running through your body\.)',
        r'(When nerves get stretched too tight like guitar strings\.)',
        r'(Using Eldoa for brain and nerve problems\.)',
        r'(Teaching your muscles new, better ways to work\.)',
        r'(Grandparents and elderly people need gentler exercises\.)',
    ]

    highlighted = content
    for pattern in patterns:
        highlighted = re.sub(pattern, r'<mark>\1</mark>', highlighted)

    return highlighted

def create_html_file(entry, output_path):
    """Create an individual HTML file for an encyclopedia entry"""
    title = entry['title']
    content = entry['content']

    # Apply highlighting
    content_html = highlight_yellow_terms(content)

    # Replace newlines with paragraphs
    paragraphs = content_html.split('. ')
    content_html = '</p><p>'.join(paragraphs)

    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - ELDOA Encyclopedia</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica Neue', Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            background-color: #f5f5f5;
        }}

        .container {{
            max-width: 800px;
            margin: 0 auto;
            padding: 2rem;
            background-color: white;
            min-height: 100vh;
        }}

        .header {{
            margin-bottom: 2rem;
        }}

        .pillar-logo {{
            color: #7c3aed;
            font-size: 2.5rem;
            font-weight: 900;
            letter-spacing: 0.05em;
            margin-bottom: 0.5rem;
        }}

        .pillar-underline {{
            width: 150px;
            height: 4px;
            background-color: #7c3aed;
            margin-bottom: 2rem;
        }}

        .entry-title {{
            font-size: 2rem;
            font-weight: 700;
            color: #1a1a1a;
            margin-bottom: 1.5rem;
        }}

        .entry-content {{
            font-size: 1.125rem;
            line-height: 1.8;
            color: #333;
        }}

        .entry-content p {{
            margin-bottom: 1rem;
        }}

        mark {{
            background-color: #fef08a;
            padding: 0.125rem 0.25rem;
        }}

        .back-link {{
            display: inline-block;
            margin-top: 2rem;
            color: #7c3aed;
            text-decoration: none;
            font-weight: 600;
        }}

        .back-link:hover {{
            text-decoration: underline;
        }}

        @media (max-width: 768px) {{
            .container {{
                padding: 1rem;
            }}

            .pillar-logo {{
                font-size: 2rem;
            }}

            .entry-title {{
                font-size: 1.5rem;
            }}

            .entry-content {{
                font-size: 1rem;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="pillar-logo">PILLAR</div>
            <div class="pillar-underline"></div>
        </div>

        <h1 class="entry-title">{title}</h1>

        <div class="entry-content">
            <p>{content_html}</p>
        </div>

        <a href="/encyclopedia" class="back-link">← Back to Encyclopedia</a>
    </div>
</body>
</html>'''

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)

def create_slug(title):
    """Create URL-friendly slug from title"""
    slug = title.lower()
    slug = re.sub(r'[^\w\s-]', '', slug)
    slug = re.sub(r'[-\s]+', '-', slug)
    return slug

def main():
    """Main function to extract and create HTML files"""
    print("Starting encyclopedia extraction...")

    # Create output directory
    os.makedirs(OUTPUT_HTML_DIR, exist_ok=True)

    # Get all PDF files
    pdf_files = sorted(Path(ENCYCLOPEDIA_PDF_DIR).glob("*.pdf"))
    print(f"Found {len(pdf_files)} PDF files")

    all_entries = []
    entries_by_letter = defaultdict(list)

    # Process each PDF
    for i, pdf_path in enumerate(pdf_files, 1):
        print(f"Processing {i}/{len(pdf_files)}: {pdf_path.name}")

        text = extract_text_from_pdf(pdf_path)
        if not text:
            continue

        entries = parse_entries(text)
        print(f"  Found {len(entries)} entries")

        for entry in entries:
            all_entries.append(entry)

            # Get first letter for categorization
            first_letter = entry['title'][0].upper() if entry['title'] else 'A'
            entries_by_letter[first_letter].append(entry)

    print(f"\nTotal entries extracted: {len(all_entries)}")

    # Create HTML files
    print("\nCreating HTML files...")
    created_files = []

    for entry in all_entries:
        slug = create_slug(entry['title'])
        output_path = os.path.join(OUTPUT_HTML_DIR, f"{slug}.html")

        create_html_file(entry, output_path)
        created_files.append({
            'title': entry['title'],
            'slug': slug,
            'file': f"{slug}.html",
            'letter': entry['title'][0].upper() if entry['title'] else 'A'
        })

    print(f"Created {len(created_files)} HTML files")

    # Create index data JSON
    index_data = {
        'total_entries': len(all_entries),
        'entries': created_files,
        'by_letter': {letter: [e for e in created_files if e['letter'] == letter]
                      for letter in sorted(set(e['letter'] for e in created_files))}
    }

    with open(OUTPUT_DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(index_data, f, indent=2)

    print(f"\nIndex data saved to {OUTPUT_DATA_FILE}")
    print("\nDone!")

    # Print summary by letter
    print("\nEntries by letter:")
    for letter in sorted(entries_by_letter.keys()):
        print(f"  {letter}: {len(entries_by_letter[letter])} entries")

if __name__ == "__main__":
    main()
