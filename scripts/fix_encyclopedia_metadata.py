#!/usr/bin/env python3
"""
Fix Encyclopedia Pages SEO/AEO Metadata
Adds missing meta descriptions, Open Graph tags, Twitter Cards, Schema.org, and canonical URLs
"""

import os
import re
from pathlib import Path
from html.parser import HTMLParser
import json

class EncyclopediaHTMLParser(HTMLParser):
    """Parse encyclopedia HTML to extract key information"""

    def __init__(self):
        super().__init__()
        self.title = ""
        self.h1 = ""
        self.first_paragraph = ""
        self.in_title = False
        self.in_h1 = False
        self.in_p = False
        self.p_count = 0

    def handle_starttag(self, tag, attrs):
        if tag == 'title':
            self.in_title = True
        elif tag == 'h1':
            self.in_h1 = True
        elif tag == 'p' and not self.first_paragraph:
            self.in_p = True

    def handle_data(self, data):
        if self.in_title:
            self.title += data.strip()
        elif self.in_h1:
            self.h1 += data.strip()
        elif self.in_p and self.p_count < 2:
            self.first_paragraph += data.strip() + " "

    def handle_endtag(self, tag):
        if tag == 'title':
            self.in_title = False
        elif tag == 'h1':
            self.in_h1 = False
        elif tag == 'p':
            if self.in_p:
                self.p_count += 1
            self.in_p = False

def extract_page_info(html_content):
    """Extract title, h1, and first paragraph from HTML"""
    parser = EncyclopediaHTMLParser()
    parser.feed(html_content)
    return {
        'title': parser.title,
        'h1': parser.h1,
        'first_paragraph': parser.first_paragraph.strip()
    }

def generate_meta_description(page_info):
    """Generate a meta description from page content"""
    # Use first paragraph if available, otherwise use H1
    if page_info['first_paragraph']:
        desc = page_info['first_paragraph']
    elif page_info['h1']:
        desc = f"Learn about {page_info['h1']} in the ELDOA AI Encyclopedia. Comprehensive information on this ELDOA concept."
    else:
        desc = "Comprehensive ELDOA encyclopedia entry covering key concepts, techniques, and applications."

    # Truncate to 120-160 characters
    if len(desc) > 160:
        desc = desc[:157] + "..."
    elif len(desc) < 120:
        desc = desc + " Part of the comprehensive ELDOA AI Encyclopedia."
        if len(desc) > 160:
            desc = desc[:157] + "..."

    return desc

def generate_optimized_title(page_info):
    """Generate an optimized title tag (30-60 characters)"""
    if page_info['h1']:
        base_title = page_info['h1']
    else:
        # Extract from current title
        base_title = page_info['title'].replace(' - ELDOA AI Encyclopedia', '').strip()

    # Capitalize properly
    base_title = base_title.title()

    # Add suffix
    full_title = f"{base_title} – ELDOA Encyclopedia"

    # Check length
    if len(full_title) > 60:
        # Truncate base title
        max_base = 60 - len(" – ELDOA Encyclopedia")
        base_title = base_title[:max_base-3] + "..."
        full_title = f"{base_title} – ELDOA Encyclopedia"
    elif len(full_title) < 30:
        # Add more context
        full_title = f"{base_title} – ELDOA AI Encyclopedia"

    return full_title

def generate_slug(filename):
    """Generate URL slug from filename"""
    return filename.replace('.html', '')

def inject_metadata(html_content, page_info, slug):
    """Inject SEO/AEO metadata into HTML"""

    # Generate metadata
    meta_description = generate_meta_description(page_info)
    optimized_title = generate_optimized_title(page_info)
    canonical_url = f"https://eldoa.ai/encyclopedia/{slug}"

    # Generate keywords
    keywords = f"ELDOA, {page_info['h1'] if page_info['h1'] else slug.replace('-', ' ')}, Guy Voyer, fascia, spinal decompression"

    # Create Schema.org structured data
    schema_data = {
        "@context": "https://schema.org",
        "@type": "DefinedTerm",
        "name": page_info['h1'] if page_info['h1'] else optimized_title,
        "description": meta_description,
        "inDefinedTermSet": {
            "@type": "DefinedTermSet",
            "name": "ELDOA AI Encyclopedia",
            "url": "https://eldoa.ai/encyclopedia/"
        },
        "url": canonical_url
    }

    # Create breadcrumb schema
    breadcrumb_schema = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": 1,
                "name": "Home",
                "item": "https://eldoa.ai/"
            },
            {
                "@type": "ListItem",
                "position": 2,
                "name": "Encyclopedia",
                "item": "https://eldoa.ai/encyclopedia/"
            },
            {
                "@type": "ListItem",
                "position": 3,
                "name": page_info['h1'] if page_info['h1'] else optimized_title,
                "item": canonical_url
            }
        ]
    }

    # Build metadata HTML
    metadata_html = f"""    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <!-- Primary Meta Tags -->
    <title>{optimized_title}</title>
    <meta name="title" content="{optimized_title}">
    <meta name="description" content="{meta_description}">
    <meta name="keywords" content="{keywords}">
    <meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1,max-video-preview:-1">

    <!-- Canonical URL -->
    <link rel="canonical" href="{canonical_url}">

    <!-- Open Graph / Facebook -->
    <meta property="og:type" content="article">
    <meta property="og:url" content="{canonical_url}">
    <meta property="og:title" content="{optimized_title}">
    <meta property="og:description" content="{meta_description}">
    <meta property="og:image" content="https://eldoa.ai/images/og-encyclopedia.jpg">
    <meta property="og:site_name" content="ELDOA AI">

    <!-- Twitter -->
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:url" content="{canonical_url}">
    <meta name="twitter:title" content="{optimized_title}">
    <meta name="twitter:description" content="{meta_description}">
    <meta name="twitter:image" content="https://eldoa.ai/images/og-encyclopedia.jpg">

    <!-- Favicon -->
    <link rel="icon" type="image/png" href="/favicon.png">
    <link rel="apple-touch-icon" href="/apple-touch-icon.png">

    <!-- Theme Color -->
    <meta name="theme-color" content="#1a1a1a">
    <meta name="theme-color" content="#ffffff" media="(prefers-color-scheme: light)">
    <meta name="theme-color" content="#1a1a1a" media="(prefers-color-scheme: dark)">

    <!-- Schema.org Structured Data -->
    <script type="application/ld+json">
{json.dumps(schema_data, indent=8)}
    </script>

    <!-- Breadcrumb Schema -->
    <script type="application/ld+json">
{json.dumps(breadcrumb_schema, indent=8)}
    </script>
"""

    # Replace existing head content
    # Find the head section
    head_pattern = r'<head>(.*?)</head>'
    head_match = re.search(head_pattern, html_content, re.DOTALL)

    if head_match:
        old_head_content = head_match.group(1)

        # Extract style section if it exists
        style_pattern = r'(<style>.*?</style>)'
        style_match = re.search(style_pattern, old_head_content, re.DOTALL)

        if style_match:
            style_section = style_match.group(1)
            new_head_content = metadata_html + "\n    " + style_section
        else:
            new_head_content = metadata_html

        # Replace head content
        new_html = html_content.replace(old_head_content, new_head_content)
        return new_html

    return html_content

def process_encyclopedia_file(file_path):
    """Process a single encyclopedia file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            html_content = f.read()

        # Extract page information
        page_info = extract_page_info(html_content)

        # Generate slug from filename
        slug = generate_slug(file_path.name)

        # Inject metadata
        updated_html = inject_metadata(html_content, page_info, slug)

        # Write back
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(updated_html)

        return {
            'file': str(file_path),
            'status': 'success',
            'title': page_info['h1'] if page_info['h1'] else page_info['title']
        }

    except Exception as e:
        return {
            'file': str(file_path),
            'status': 'error',
            'error': str(e)
        }

def main():
    """Main execution"""
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    encyclopedia_dir = project_root / 'public' / 'encyclopedia'

    print("=" * 70)
    print("ELDOA Encyclopedia Metadata Fixer")
    print("Adding SEO/AEO metadata to encyclopedia pages")
    print("=" * 70)

    # Find all HTML files
    html_files = list(encyclopedia_dir.glob('*.html'))

    print(f"\nFound {len(html_files)} encyclopedia pages to process\n")

    # Process files
    results = []
    success_count = 0
    error_count = 0

    for i, file_path in enumerate(html_files, 1):
        rel_path = file_path.relative_to(project_root)
        print(f"[{i}/{len(html_files)}] Processing: {rel_path.name}...", end=' ')

        result = process_encyclopedia_file(file_path)
        results.append(result)

        if result['status'] == 'success':
            print(f"✓ {result['title'][:50]}")
            success_count += 1
        else:
            print(f"✗ Error: {result['error']}")
            error_count += 1

    # Summary
    print("\n" + "=" * 70)
    print(f"Processing Complete!")
    print(f"  ✓ Success: {success_count} pages")
    print(f"  ✗ Errors:  {error_count} pages")
    print("=" * 70)

    # Save results log
    log_path = project_root / 'encyclopedia-metadata-fix-log.json'
    with open(log_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2)

    print(f"\nDetailed log saved to: {log_path}")

    print("\n" + "=" * 70)
    print("NEXT STEPS:")
    print("1. Review the updated pages")
    print("2. Run the audit script again to verify improvements")
    print("3. Commit and push the changes")
    print("4. Expected score improvement: 78.9 → ~95+")
    print("=" * 70)

if __name__ == '__main__':
    main()
