#!/usr/bin/env python3
"""
Generate individual ELDOA city HTML pages from city-pages.json.

Usage: python3 scripts/generate-city-pages.py

Each city in data/city-pages.json gets its own static HTML file:
  eldoa-montreal.html
  eldoa-new-york-city.html
  eldoa-toronto.html
  ...

The HTML files have pre-baked SEO meta tags for crawlers, and load
shared CSS/JS for dynamic practitioner rendering at runtime.
"""

import json
import os
import html

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
DATA_FILE = os.path.join(PROJECT_ROOT, 'data', 'city-pages.json')


def generate_faq_schema(city):
    """Generate FAQPage schema JSON-LD."""
    if not city.get('faqs'):
        return ''
    schema = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": faq["question"],
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": faq["answer"]
                }
            }
            for faq in city["faqs"]
        ]
    }
    return json.dumps(schema, ensure_ascii=False)


def generate_breadcrumb_schema(city):
    """Generate BreadcrumbList schema JSON-LD."""
    schema = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://eldoa.ai/"},
            {"@type": "ListItem", "position": 2, "name": "Find a Specialist", "item": "https://eldoa.ai/practitioners.html"},
            {"@type": "ListItem", "position": 3, "name": f"ELDOA {city['name']}", "item": f"https://eldoa.ai/eldoa-{city['slug']}.html"}
        ]
    }
    return json.dumps(schema, ensure_ascii=False)


def generate_city_schema(city):
    """Generate initial ItemList schema JSON-LD (will be updated by JS with actual practitioners)."""
    schema = {
        "@context": "https://schema.org",
        "@type": "ItemList",
        "name": f"ELDOA Practitioners in {city['name']}",
        "description": city['metaDescription'],
        "url": f"https://eldoa.ai/eldoa-{city['slug']}.html"
    }
    return json.dumps(schema, ensure_ascii=False)


def generate_footer_city_links(all_cities):
    """Generate footer city link HTML for all cities."""
    links = []
    for c in all_cities:
        links.append(f'          <a href="/eldoa-{c["slug"]}.html">ELDOA {c["name"]}</a>')
    return '\n'.join(links)


def generate_html(city, all_cities):
    """Generate the full HTML page for a city."""
    slug = city['slug']
    name = city['name']
    meta_title = html.escape(city['metaTitle'])
    meta_desc = html.escape(city['metaDescription'])
    meta_keywords = html.escape(city['metaKeywords'])
    canonical = f'https://eldoa.ai/eldoa-{slug}.html'

    city_schema = generate_city_schema(city)
    faq_schema = generate_faq_schema(city)
    breadcrumb_schema = generate_breadcrumb_schema(city)

    # Build footer city links (show max 8 in footer, prioritize current city's nearby)
    footer_cities = []
    seen = set()
    # Add nearby cities first
    for nearby_name in (city.get('nearbyPractitionerCities') or []):
        for c in all_cities:
            if c['name'] == nearby_name and c['slug'] not in seen:
                footer_cities.append(c)
                seen.add(c['slug'])
                break
    # Fill with remaining cities
    for c in all_cities:
        if c['slug'] not in seen and len(footer_cities) < 8:
            footer_cities.append(c)
            seen.add(c['slug'])

    footer_links = '\n'.join(
        f'          <a href="/eldoa-{c["slug"]}.html">ELDOA {c["name"]}</a>'
        for c in footer_cities
    )

    return f'''<!doctype html>
<html lang="en" data-theme="light">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1"/>
  <title>{meta_title}</title>
  <meta name="description" content="{meta_desc}">
  <meta name="keywords" content="{meta_keywords}">
  <meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1">
  <link rel="canonical" href="{canonical}">

  <!-- Open Graph / Twitter -->
  <meta property="og:type" content="website">
  <meta property="og:url" content="{canonical}">
  <meta property="og:title" content="{meta_title}">
  <meta property="og:description" content="{meta_desc}">
  <meta property="og:image" content="https://eldoa.ai/images/og-practitioners.jpg">
  <meta name="twitter:card" content="summary_large_image">

  <!-- Favicons -->
  <link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">
  <link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png">
  <link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16.png">
  <link rel="manifest" href="/site.webmanifest">

  <!-- Structured Data -->
  <script type="application/ld+json" id="city-schema">
  {city_schema}
  </script>

  <script type="application/ld+json" id="faq-schema">
  {faq_schema if faq_schema else '{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[]}'}
  </script>

  <script type="application/ld+json" id="breadcrumb-schema">
  {breadcrumb_schema}
  </script>

  <link rel="stylesheet" href="/assets/css/city-page.css">
</head>
<body>
  <header>
    <div class="nav">
      <a class="logo" href="/">
        <span class="logo-mark"></span>
        <span>ELDOA <span style="color:var(--brand)">AI</span></span>
      </a>
      <nav class="nav-links">
        <a href="/diagnostic.html">Diagnostic</a>
        <a href="/videos/">Videos</a>
        <a href="/encyclopedia.html">Encyclopedia</a>
        <a href="/practitioners.html" class="active">Practitioners</a>
      </nav>
    </div>
  </header>

  <main id="main-content">
    <div class="container">
      <div class="loading">
        <div class="loading-spinner"></div>
        <p>Loading {html.escape(name)} practitioners...</p>
      </div>
    </div>
  </main>

  <footer>
    <div class="container">
      <div class="footer-grid">
        <div class="footer-col">
          <h4>Get Help</h4>
          <a href="/practitioners.html">Find a Specialist Near Me</a>
          <a href="/eldoa-classes-near-me.html">Classes Near Me</a>
          <a href="/eldoa-online-classes.html">Online Classes</a>
          <a href="/eldoa-certification.html">Get Certified</a>
        </div>
        <div class="footer-col">
          <h4>Learn ELDOA</h4>
          <a href="/diagnostic.html">Diagnostic Tool</a>
          <a href="/videos/">Video Library</a>
          <a href="/encyclopedia.html">Encyclopedia</a>
          <a href="/posture-check.html">Posture Check</a>
        </div>
        <div class="footer-col">
          <h4>ELDOA by City</h4>
{footer_links}
        </div>
        <div class="footer-col">
          <h4>Official Resources</h4>
          <a href="https://eldoavoyer.com" target="_blank" rel="noopener">ELDOAVoyer.com</a>
          <a href="https://somavoyer.com" target="_blank" rel="noopener">SomaVoyer.com</a>
          <a href="https://eldoausa.com" target="_blank" rel="noopener">ELDOAUSA</a>
          <a href="https://somaeducation.ca" target="_blank" rel="noopener">Soma Education Canada</a>
        </div>
      </div>
      <small>Educational content only - not medical advice. Consult a healthcare provider for diagnosis and treatment.</small>
    </div>
  </footer>

  <script>window.CITY_SLUG = "{slug}";</script>
  <script src="/assets/js/city-page.js"></script>
</body>
</html>'''


def main():
    with open(DATA_FILE, 'r') as f:
        data = json.load(f)

    cities = data['cities']
    print(f"Generating {len(cities)} city pages...")

    for city in cities:
        filename = f"eldoa-{city['slug']}.html"
        filepath = os.path.join(PROJECT_ROOT, filename)
        page_html = generate_html(city, cities)

        with open(filepath, 'w') as f:
            f.write(page_html)

        print(f"  ✓ {filename}")

    print(f"\nDone! {len(cities)} city pages generated.")


if __name__ == '__main__':
    main()
