#!/usr/bin/env python3
"""
Process ELDOA Video Library CSV and generate:
1. Enhanced video-library.json with full metadata
2. Individual HTML pages for each video with SEO/AEO optimization
3. Video sitemap for SEO
"""

import csv
import json
import re
import os
from urllib.parse import urlparse, parse_qs
from pathlib import Path

# Mapping for extracting metadata from titles/descriptions
SEGMENT_PATTERNS = {
    'C1-C2': r'C1[-/]C2',
    'C2-C3': r'C2[-/]C3',
    'C3-C4': r'C3[-/]C4',
    'C4-C5': r'C4[-/]C5',
    'C5-C6': r'C5[-/]C6',
    'C6-C7': r'C6[-/]C7',
    'C7-T1': r'C7[-/]T1',
    'T1-T2': r'T1[-/]T2',
    'T2-T3': r'T2[-/]T3',
    'T3-T4': r'T3[-/]T4',
    'T4-T5': r'T4[-/]T5',
    'T5-T6': r'T5[-/]T6',
    'T6-T7': r'T6[-/]T7',
    'T7-T8': r'T7[-/]T8',
    'T8-T9': r'T8[-/]T9',
    'T9-T10': r'T9[-/]T10',
    'T10-T11': r'T10[-/]T11',
    'T11-T12': r'T11[-/]T12',
    'T12-L1': r'T12[-/]L1',
    'L1-L2': r'L1[-/]L2',
    'L2-L3': r'L2[-/]L3',
    'L3-L4': r'L3[-/]L4',
    'L4-L5': r'L4[-/]L5',
    'L5-S1': r'L5[-/]S1',
    'S1-S2': r'S1[-/]S2',
    'S5-Coccyx': r'S5[-/]Coccyx',
}

REGION_MAP = {
    'C1-C2': 'Cervical', 'C2-C3': 'Cervical', 'C3-C4': 'Cervical', 'C4-C5': 'Cervical',
    'C5-C6': 'Cervical', 'C6-C7': 'Cervical', 'C7-T1': 'Cervicothoracic',
    'T1-T2': 'Upper Thoracic', 'T2-T3': 'Upper Thoracic', 'T3-T4': 'Upper Thoracic',
    'T4-T5': 'Upper Thoracic', 'T5-T6': 'Mid Thoracic', 'T6-T7': 'Mid Thoracic',
    'T7-T8': 'Mid Thoracic', 'T8-T9': 'Mid Thoracic', 'T9-T10': 'Lower Thoracic',
    'T10-T11': 'Lower Thoracic', 'T11-T12': 'Lower Thoracic', 'T12-L1': 'Thoracolumbar',
    'L1-L2': 'Lumbar', 'L2-L3': 'Lumbar', 'L3-L4': 'Lumbar', 'L4-L5': 'Lumbar',
    'L5-S1': 'Lumbosacral', 'S1-S2': 'Sacral', 'S5-Coccyx': 'Coccygeal'
}

DIFFICULTY_KEYWORDS = {
    'Beginner': ['beginner', 'intro', 'basic', 'first', 'start'],
    'Intermediate': ['intermediate', 'int'],
    'Advanced': ['advanced', 'expert', 'master']
}

AILMENT_KEYWORDS = {
    'Low Back Pain': ['low back pain', 'back pain', 'lower back'],
    'Sciatica': ['sciatica', 'sciatic'],
    'Neck Pain': ['neck pain', 'text neck', 'tight neck'],
    'Shoulder Pain': ['shoulder pain', 'shoulder'],
    'Hip Pain': ['hip pain', 'coxo'],
    'Disc Herniation': ['disc herniation', 'herniation', 'disc'],
    'Scoliosis': ['scoliosis'],
    'Hyperkyphosis': ['hyperkyphosis', 'kyphosis'],
    'Hyperlordosis': ['hyperlordosis', 'lordosis'],
    'Spinal Stenosis': ['spinal stenosis', 'stenosis'],
    'Piriformis Syndrome': ['piriformis'],
    'Radiculopathy': ['radiculopathy', 'pinched nerve'],
    'Carpal Tunnel': ['carpal tunnel'],
    'Postural Issues': ['posture', 'postural'],
    'Knee Pain': ['knee pain', 'valgus knees', 'bow legs'],
    'Foot Pain': ['flat feet', 'foot pain'],
    'Elbow Pain': ['elbow pain'],
    'Wrist Pain': ['wrist pain'],
    'Pelvic Issues': ['pelvic', 'anterior pelvic tilt', 'rotated pelvis'],
    'Rib Flare': ['rib flare']
}

def extract_youtube_id(url):
    """Extract YouTube video ID from URL"""
    if 'youtube.com/watch' in url:
        parsed = urlparse(url)
        return parse_qs(parsed.query).get('v', [None])[0]
    elif 'youtube.com/shorts' in url or 'youtu.be' in url:
        return url.split('/')[-1].split('?')[0]
    return None

def extract_segments(text):
    """Extract spinal segments from text"""
    segments = []
    for segment, pattern in SEGMENT_PATTERNS.items():
        if re.search(pattern, text, re.IGNORECASE):
            segments.append(segment)
    return segments if segments else ['General']

def extract_difficulty(text):
    """Extract difficulty level from text"""
    text_lower = text.lower()
    for difficulty, keywords in DIFFICULTY_KEYWORDS.items():
        if any(keyword in text_lower for keyword in keywords):
            return difficulty
    return 'All Levels'

def extract_ailments(text):
    """Extract ailments/conditions from text"""
    ailments = []
    text_lower = text.lower()
    for ailment, keywords in AILMENT_KEYWORDS.items():
        if any(keyword in text_lower for keyword in keywords):
            ailments.append(ailment)
    return ailments if ailments else ['General Spinal Health']

def parse_duration(duration_str):
    """Parse duration string to seconds and return MM:SS format"""
    if not duration_str or duration_str.strip() == '':
        return '0:00', 0

    # Handle different formats
    duration_str = duration_str.strip()

    # Format: HH:MM:SS or MM:SS or M:SS
    parts = duration_str.split(':')

    try:
        if len(parts) == 3:  # HH:MM:SS
            h, m, s = int(parts[0]), int(parts[1]), int(parts[2])
            total_seconds = h * 3600 + m * 60 + s
            return f"{m + h * 60}:{s:02d}", total_seconds
        elif len(parts) == 2:  # MM:SS
            m, s = int(parts[0]), int(parts[1])
            total_seconds = m * 60 + s
            return f"{m}:{s:02d}", total_seconds
        elif len(parts) == 1:  # Just seconds
            s = int(parts[0])
            return f"{s // 60}:{s % 60:02d}", s
    except:
        return '0:00', 0

    return '0:00', 0

def generate_slug(title):
    """Generate URL-friendly slug from title"""
    slug = title.lower()
    slug = re.sub(r'[^\w\s-]', '', slug)
    slug = re.sub(r'[-\s]+', '-', slug)
    return slug[:100]  # Limit length

def process_csv_to_json(csv_path, output_json_path):
    """Process CSV and create enhanced video library JSON"""
    videos = []

    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)

        for idx, row in enumerate(reader, 1):
            title = row['Title'].strip()
            channel = row['Channel'].strip()
            duration_str = row['Duration'].strip()
            focus = row['Focus'].strip()
            link = row['Link'].strip()

            # Extract metadata
            combined_text = f"{title} {focus}"
            segments = extract_segments(combined_text)
            difficulty = extract_difficulty(combined_text)
            ailments = extract_ailments(combined_text)

            # Parse duration
            duration, duration_seconds = parse_duration(duration_str)

            # Generate unique ID
            video_id = generate_slug(title)

            # Extract YouTube ID for thumbnail
            youtube_id = extract_youtube_id(link)
            thumbnail = f"https://img.youtube.com/vi/{youtube_id}/maxresdefault.jpg" if youtube_id else ""

            # Determine region from first segment
            region = REGION_MAP.get(segments[0] if segments[0] != 'General' else 'L5-S1', 'Full Spine')

            # Create video object
            video = {
                'id': video_id,
                'title': title,
                'instructor': channel,
                'duration': duration,
                'duration_seconds': duration_seconds,
                'segment': segments[0] if len(segments) == 1 else ', '.join(segments),
                'segments': segments,
                'region': region,
                'difficulty': difficulty,
                'description': focus,
                'ailment': ailments,
                'url': link,
                'youtube_id': youtube_id,
                'thumbnail': thumbnail,
                'tags': list(set([s.lower() for s in segments] + [a.lower().replace(' ', '-') for a in ailments])),
                'equipment': 'Mat or comfortable surface',
                'source': 'YouTube',
                'date_added': '2025-01-18'
            }

            videos.append(video)

    # Write to JSON
    with open(output_json_path, 'w', encoding='utf-8') as f:
        json.dump(videos, f, indent=2, ensure_ascii=False)

    print(f"✓ Generated {len(videos)} video entries in {output_json_path}")
    return videos

def generate_video_page(video, output_dir):
    """Generate individual video page with full SEO metadata"""

    # Create filename from ID
    filename = f"{video['id']}.html"
    filepath = os.path.join(output_dir, filename)

    # Generate Schema.org VideoObject structured data
    schema_data = {
        "@context": "https://schema.org",
        "@type": "VideoObject",
        "name": video['title'],
        "description": video['description'],
        "thumbnailUrl": video['thumbnail'],
        "uploadDate": video['date_added'],
        "duration": f"PT{video['duration_seconds']}S",
        "contentUrl": video['url'],
        "embedUrl": f"https://www.youtube.com/embed/{video['youtube_id']}" if video['youtube_id'] else video['url'],
        "publisher": {
            "@type": "Organization",
            "name": "ELDOA AI",
            "logo": {
                "@type": "ImageObject",
                "url": "https://eldoa.ai/images/logo.png"
            }
        },
        "author": {
            "@type": "Person",
            "name": video['instructor']
        }
    }

    # Generate keywords
    keywords = ', '.join([
        video['title'],
        video['instructor'],
        'ELDOA',
        video['region'],
        video['difficulty']
    ] + video['ailment'] + video['segments'])

    # Generate meta description
    meta_description = f"{video['title']} by {video['instructor']}. {video['description'][:140]}..."

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
                "name": "Video Library",
                "item": "https://eldoa.ai/videos/"
            },
            {
                "@type": "ListItem",
                "position": 3,
                "name": video['title'],
                "item": f"https://eldoa.ai/videos/{filename}"
            }
        ]
    }

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">

    <!-- Primary Meta Tags -->
    <title>{video['title']} - ELDOA Video Tutorial | ELDOA AI</title>
    <meta name="title" content="{video['title']} - ELDOA Video Tutorial | ELDOA AI">
    <meta name="description" content="{meta_description}">
    <meta name="keywords" content="{keywords}">
    <meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1,max-video-preview:-1">
    <meta name="author" content="{video['instructor']}">

    <!-- Canonical URL -->
    <link rel="canonical" href="https://eldoa.ai/videos/{filename}">

    <!-- Open Graph / Facebook -->
    <meta property="og:type" content="video.other">
    <meta property="og:url" content="https://eldoa.ai/videos/{filename}">
    <meta property="og:title" content="{video['title']} - ELDOA Video Tutorial">
    <meta property="og:description" content="{meta_description}">
    <meta property="og:image" content="{video['thumbnail']}">
    <meta property="og:video" content="{video['url']}">
    <meta property="og:site_name" content="ELDOA AI">

    <!-- Twitter -->
    <meta name="twitter:card" content="player">
    <meta name="twitter:url" content="https://eldoa.ai/videos/{filename}">
    <meta name="twitter:title" content="{video['title']} - ELDOA Video Tutorial">
    <meta name="twitter:description" content="{meta_description}">
    <meta name="twitter:image" content="{video['thumbnail']}">
    <meta name="twitter:player" content="https://www.youtube.com/embed/{video['youtube_id'] if video['youtube_id'] else ''}">
    <meta name="twitter:player:width" content="1280">
    <meta name="twitter:player:height" content="720">

    <!-- Favicon -->
    <link rel="icon" type="image/png" href="/favicon.png">
    <link rel="apple-touch-icon" href="/apple-touch-icon.png">

    <!-- Theme Color -->
    <meta name="theme-color" content="#1a1a1a">
    <meta name="theme-color" content="#ffffff" media="(prefers-color-scheme: light)">
    <meta name="theme-color" content="#1a1a1a" media="(prefers-color-scheme: dark)">

    <!-- Schema.org Structured Data -->
    <script type="application/ld+json">
{json.dumps(schema_data, indent=4)}
    </script>

    <!-- Breadcrumb Schema -->
    <script type="application/ld+json">
{json.dumps(breadcrumb_schema, indent=4)}
    </script>

    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        :root {{
            --primary-color: #2c3e50;
            --accent-color: #3498db;
            --text-color: #333;
            --bg-color: #fff;
            --card-bg: #f8f9fa;
            --border-color: #ddd;
        }}

        @media (prefers-color-scheme: dark) {{
            :root {{
                --text-color: #e0e0e0;
                --bg-color: #1a1a1a;
                --card-bg: #2a2a2a;
                --border-color: #444;
            }}
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            line-height: 1.6;
            color: var(--text-color);
            background-color: var(--bg-color);
            padding: 20px;
            max-width: 1200px;
            margin: 0 auto;
        }}

        header {{
            margin-bottom: 30px;
            padding-bottom: 20px;
            border-bottom: 2px solid var(--border-color);
        }}

        .breadcrumb {{
            font-size: 0.9rem;
            margin-bottom: 15px;
            color: #666;
        }}

        .breadcrumb a {{
            color: var(--accent-color);
            text-decoration: none;
        }}

        .breadcrumb a:hover {{
            text-decoration: underline;
        }}

        h1 {{
            font-size: 2rem;
            margin-bottom: 15px;
            color: var(--primary-color);
        }}

        @media (prefers-color-scheme: dark) {{
            h1 {{
                color: var(--accent-color);
            }}
        }}

        .video-meta {{
            display: flex;
            flex-wrap: wrap;
            gap: 15px;
            margin-bottom: 20px;
            font-size: 0.95rem;
        }}

        .meta-item {{
            display: flex;
            align-items: center;
            gap: 5px;
        }}

        .meta-label {{
            font-weight: 600;
            color: #666;
        }}

        .badge {{
            display: inline-block;
            padding: 4px 12px;
            border-radius: 20px;
            background-color: var(--accent-color);
            color: white;
            font-size: 0.85rem;
            font-weight: 500;
        }}

        .badge.beginner {{
            background-color: #27ae60;
        }}

        .badge.intermediate {{
            background-color: #f39c12;
        }}

        .badge.advanced {{
            background-color: #e74c3c;
        }}

        .video-container {{
            position: relative;
            width: 100%;
            padding-bottom: 56.25%; /* 16:9 aspect ratio */
            margin-bottom: 30px;
            background-color: #000;
            border-radius: 8px;
            overflow: hidden;
        }}

        .video-container iframe {{
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            border: 0;
        }}

        .description {{
            margin-bottom: 30px;
            padding: 20px;
            background-color: var(--card-bg);
            border-radius: 8px;
            border-left: 4px solid var(--accent-color);
        }}

        .description h2 {{
            font-size: 1.3rem;
            margin-bottom: 10px;
        }}

        .details {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}

        .detail-card {{
            padding: 20px;
            background-color: var(--card-bg);
            border-radius: 8px;
            border: 1px solid var(--border-color);
        }}

        .detail-card h3 {{
            font-size: 1.1rem;
            margin-bottom: 10px;
            color: var(--accent-color);
        }}

        .detail-card ul {{
            list-style: none;
            padding-left: 0;
        }}

        .detail-card li {{
            padding: 5px 0;
            border-bottom: 1px solid var(--border-color);
        }}

        .detail-card li:last-child {{
            border-bottom: none;
        }}

        .back-link {{
            display: inline-block;
            margin-top: 30px;
            padding: 12px 24px;
            background-color: var(--accent-color);
            color: white;
            text-decoration: none;
            border-radius: 6px;
            font-weight: 500;
            transition: background-color 0.3s;
        }}

        .back-link:hover {{
            background-color: #2980b9;
        }}

        @media (max-width: 768px) {{
            h1 {{
                font-size: 1.5rem;
            }}

            .details {{
                grid-template-columns: 1fr;
            }}
        }}
    </style>
</head>
<body>
    <header>
        <nav class="breadcrumb">
            <a href="/">Home</a> / <a href="/videos/">Video Library</a> / {video['title']}
        </nav>

        <h1>{video['title']}</h1>

        <div class="video-meta">
            <div class="meta-item">
                <span class="meta-label">Instructor:</span>
                <span>{video['instructor']}</span>
            </div>
            <div class="meta-item">
                <span class="meta-label">Duration:</span>
                <span>{video['duration']}</span>
            </div>
            <div class="meta-item">
                <span class="badge {video['difficulty'].lower()}">{video['difficulty']}</span>
            </div>
        </div>
    </header>

    <main>
        <div class="video-container">
            <iframe
                src="https://www.youtube.com/embed/{video['youtube_id']}"
                title="{video['title']}"
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                allowfullscreen>
            </iframe>
        </div>

        <div class="description">
            <h2>About This Video</h2>
            <p>{video['description']}</p>
        </div>

        <div class="details">
            <div class="detail-card">
                <h3>Target Segments</h3>
                <ul>
                    {''.join(f'<li>{seg}</li>' for seg in video['segments'])}
                </ul>
            </div>

            <div class="detail-card">
                <h3>Region</h3>
                <ul>
                    <li>{video['region']}</li>
                </ul>
            </div>

            <div class="detail-card">
                <h3>Addresses</h3>
                <ul>
                    {''.join(f'<li>{ailment}</li>' for ailment in video['ailment'])}
                </ul>
            </div>

            <div class="detail-card">
                <h3>Equipment</h3>
                <ul>
                    <li>{video['equipment']}</li>
                </ul>
            </div>
        </div>

        <a href="/videos/" class="back-link">← Back to Video Library</a>
    </main>
</body>
</html>"""

    # Write the HTML file
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html_content)

    return filename

def generate_all_video_pages(videos, output_dir):
    """Generate individual pages for all videos"""
    os.makedirs(output_dir, exist_ok=True)

    generated_files = []
    for video in videos:
        filename = generate_video_page(video, output_dir)
        generated_files.append(filename)

    print(f"✓ Generated {len(generated_files)} individual video pages in {output_dir}")
    return generated_files

def generate_video_sitemap(videos, output_path):
    """Generate XML sitemap for all video pages"""

    sitemap_xml = '''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
        xmlns:video="http://www.google.com/schemas/sitemap-video/1.1">
'''

    for video in videos:
        sitemap_xml += f'''    <url>
        <loc>https://eldoa.ai/videos/{video['id']}.html</loc>
        <video:video>
            <video:thumbnail_loc>{video['thumbnail']}</video:thumbnail_loc>
            <video:title>{video['title']}</video:title>
            <video:description>{video['description'][:500]}</video:description>
            <video:content_loc>{video['url']}</video:content_loc>
            <video:duration>{video['duration_seconds']}</video:duration>
            <video:publication_date>{video['date_added']}T00:00:00+00:00</video:publication_date>
        </video:video>
        <lastmod>{video['date_added']}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.8</priority>
    </url>
'''

    sitemap_xml += '</urlset>'

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(sitemap_xml)

    print(f"✓ Generated video sitemap at {output_path}")

def main():
    """Main execution"""
    script_dir = Path(__file__).parent
    project_root = script_dir.parent

    csv_path = project_root / 'videos' / 'Eldoa Video Library - Sheet1.csv'
    json_output = project_root / 'data' / 'video-library.json'
    pages_output = project_root / 'videos' / 'pages'
    sitemap_output = project_root / 'videos' / 'video-sitemap.xml'

    print("=" * 60)
    print("ELDOA Video Library Processor")
    print("=" * 60)

    # Step 1: Process CSV to JSON
    print("\n[1/3] Processing CSV and generating enhanced video library JSON...")
    videos = process_csv_to_json(csv_path, json_output)

    # Step 2: Generate individual video pages
    print("\n[2/3] Generating individual video pages with SEO metadata...")
    generated_files = generate_all_video_pages(videos, pages_output)

    # Step 3: Generate video sitemap
    print("\n[3/3] Generating video sitemap for SEO...")
    generate_video_sitemap(videos, sitemap_output)

    print("\n" + "=" * 60)
    print("✓ Processing complete!")
    print(f"  - {len(videos)} videos processed")
    print(f"  - {len(generated_files)} HTML pages generated")
    print(f"  - Video library JSON: {json_output}")
    print(f"  - Video pages directory: {pages_output}")
    print(f"  - Video sitemap: {sitemap_output}")
    print("=" * 60)

if __name__ == '__main__':
    main()
