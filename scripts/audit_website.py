#!/usr/bin/env python3
"""
Comprehensive Website Audit for Mobile, SEO, and AEO Optimization
Analyzes all HTML files in the ELDOA AI website
"""

import os
import re
import json
from pathlib import Path
from html.parser import HTMLParser
from collections import defaultdict
from urllib.parse import urlparse

class HTMLAuditor(HTMLParser):
    """Parse and audit HTML for SEO/AEO/Mobile optimization"""

    def __init__(self):
        super().__init__()
        self.meta_tags = {}
        self.og_tags = {}
        self.twitter_tags = {}
        self.schema_data = []
        self.headings = defaultdict(list)
        self.images = []
        self.links = []
        self.has_viewport = False
        self.has_canonical = False
        self.has_title = False
        self.title_content = ""
        self.in_title = False

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)

        # Check meta tags
        if tag == 'meta':
            name = attrs_dict.get('name', attrs_dict.get('property', ''))
            content = attrs_dict.get('content', '')

            if name == 'viewport':
                self.has_viewport = True
                self.meta_tags['viewport'] = content
            elif name == 'description':
                self.meta_tags['description'] = content
            elif name == 'keywords':
                self.meta_tags['keywords'] = content
            elif name == 'robots':
                self.meta_tags['robots'] = content
            elif name.startswith('og:'):
                self.og_tags[name] = content
            elif name.startswith('twitter:'):
                self.twitter_tags[name] = content
            elif name:
                self.meta_tags[name] = content

        # Check canonical
        if tag == 'link' and attrs_dict.get('rel') == 'canonical':
            self.has_canonical = True
            self.meta_tags['canonical'] = attrs_dict.get('href', '')

        # Check title
        if tag == 'title':
            self.has_title = True
            self.in_title = True

        # Check headings
        if tag in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
            self.headings[tag].append(attrs_dict)

        # Check images
        if tag == 'img':
            self.images.append({
                'src': attrs_dict.get('src', ''),
                'alt': attrs_dict.get('alt', ''),
                'width': attrs_dict.get('width', ''),
                'height': attrs_dict.get('height', '')
            })

        # Check links
        if tag == 'a':
            self.links.append({
                'href': attrs_dict.get('href', ''),
                'rel': attrs_dict.get('rel', ''),
                'target': attrs_dict.get('target', '')
            })

    def handle_data(self, data):
        if self.in_title:
            self.title_content += data

    def handle_endtag(self, tag):
        if tag == 'title':
            self.in_title = False

def extract_schema_data(html_content):
    """Extract JSON-LD schema data from HTML"""
    schema_pattern = r'<script[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>'
    schemas = re.findall(schema_pattern, html_content, re.DOTALL | re.IGNORECASE)

    parsed_schemas = []
    for schema in schemas:
        try:
            parsed = json.loads(schema.strip())
            parsed_schemas.append(parsed)
        except json.JSONDecodeError:
            pass

    return parsed_schemas

def audit_mobile_optimization(parser, file_path):
    """Audit mobile optimization"""
    issues = []
    score = 100

    # Check viewport meta tag
    if not parser.has_viewport:
        issues.append("❌ Missing viewport meta tag")
        score -= 30
    elif 'width=device-width' not in parser.meta_tags.get('viewport', ''):
        issues.append("⚠️ Viewport doesn't include width=device-width")
        score -= 15

    # Check for responsive images
    images_without_alt = [img for img in parser.images if not img['alt']]
    if images_without_alt:
        issues.append(f"⚠️ {len(images_without_alt)} images missing alt text")
        score -= min(len(images_without_alt) * 2, 20)

    # Check touch target sizes (basic check for mobile-friendly links)
    # This is a heuristic - we can't fully check without rendering

    return {
        'score': max(score, 0),
        'issues': issues,
        'has_viewport': parser.has_viewport,
        'viewport_content': parser.meta_tags.get('viewport', 'N/A')
    }

def audit_seo_optimization(parser, schemas, file_path, html_content):
    """Audit SEO optimization"""
    issues = []
    score = 100

    # Check title tag
    if not parser.has_title:
        issues.append("❌ Missing title tag")
        score -= 20
    elif len(parser.title_content) < 30:
        issues.append("⚠️ Title tag too short (< 30 characters)")
        score -= 10
    elif len(parser.title_content) > 60:
        issues.append("⚠️ Title tag too long (> 60 characters)")
        score -= 5

    # Check meta description
    if 'description' not in parser.meta_tags:
        issues.append("❌ Missing meta description")
        score -= 20
    elif len(parser.meta_tags.get('description', '')) < 120:
        issues.append("⚠️ Meta description too short (< 120 characters)")
        score -= 10
    elif len(parser.meta_tags.get('description', '')) > 160:
        issues.append("⚠️ Meta description too long (> 160 characters)")
        score -= 5

    # Check canonical URL
    if not parser.has_canonical:
        issues.append("⚠️ Missing canonical URL")
        score -= 10

    # Check robots meta
    if 'robots' not in parser.meta_tags:
        issues.append("ℹ️ No robots meta tag (default: index,follow)")

    # Check heading structure
    h1_count = len(parser.headings.get('h1', []))
    if h1_count == 0:
        issues.append("❌ No H1 heading found")
        score -= 15
    elif h1_count > 1:
        issues.append(f"⚠️ Multiple H1 headings ({h1_count})")
        score -= 10

    # Check Open Graph tags
    required_og = ['og:title', 'og:description', 'og:url', 'og:type']
    missing_og = [tag for tag in required_og if tag not in parser.og_tags]
    if missing_og:
        issues.append(f"⚠️ Missing Open Graph tags: {', '.join(missing_og)}")
        score -= len(missing_og) * 3

    # Check Twitter Card tags
    if 'twitter:card' not in parser.twitter_tags:
        issues.append("⚠️ Missing Twitter Card meta tags")
        score -= 5

    # Check for broken internal links (basic check)
    internal_links = [link['href'] for link in parser.links if link['href'].startswith('/') or not link['href'].startswith('http')]

    return {
        'score': max(score, 0),
        'issues': issues,
        'title': parser.title_content,
        'title_length': len(parser.title_content),
        'description_length': len(parser.meta_tags.get('description', '')),
        'h1_count': h1_count,
        'has_canonical': parser.has_canonical,
        'has_og_tags': len(parser.og_tags) > 0,
        'has_twitter_tags': len(parser.twitter_tags) > 0
    }

def audit_aeo_optimization(parser, schemas, file_path):
    """Audit AEO (Answer Engine Optimization)"""
    issues = []
    score = 100
    schema_types = []

    # Check for structured data
    if not schemas:
        issues.append("❌ No Schema.org structured data found")
        score -= 30
    else:
        # Extract schema types
        for schema in schemas:
            if isinstance(schema, dict):
                schema_type = schema.get('@type', 'Unknown')
                schema_types.append(schema_type)

        # Check for appropriate schema types
        if schema_types:
            issues.append(f"✅ Found schema types: {', '.join(schema_types)}")

        # Check for FAQPage schema (great for AEO)
        if 'FAQPage' in schema_types:
            issues.append("✅ Excellent: FAQPage schema found (highly AEO-friendly)")
            score += 10

        # Check for HowTo schema
        if 'HowTo' in schema_types:
            issues.append("✅ Excellent: HowTo schema found (highly AEO-friendly)")
            score += 10

        # Check for breadcrumb schema
        if 'BreadcrumbList' in schema_types:
            issues.append("✅ Good: BreadcrumbList schema found")

        # Check for VideoObject schema
        if 'VideoObject' in schema_types:
            issues.append("✅ Good: VideoObject schema found")

        # Check for MedicalWebPage or other medical schemas
        medical_schemas = ['MedicalWebPage', 'MedicalTherapy', 'MedicalCondition']
        found_medical = [s for s in schema_types if s in medical_schemas]
        if found_medical:
            issues.append(f"✅ Excellent: Medical schema found ({', '.join(found_medical)})")

    # Check for Q&A content patterns (good for AEO)
    # This is a heuristic check

    # Check for list content (good for featured snippets)
    if parser.headings.get('h2') or parser.headings.get('h3'):
        issues.append("✅ Good heading structure for featured snippets")

    return {
        'score': min(max(score, 0), 100),
        'issues': issues,
        'schema_types': schema_types,
        'has_structured_data': len(schemas) > 0,
        'schema_count': len(schemas)
    }

def audit_performance(html_content, file_path):
    """Basic performance audit"""
    issues = []
    score = 100

    file_size = len(html_content.encode('utf-8'))

    # Check file size
    if file_size > 500000:  # 500KB
        issues.append(f"⚠️ Large HTML file size: {file_size / 1024:.1f} KB")
        score -= 15
    elif file_size > 200000:  # 200KB
        issues.append(f"ℹ️ Moderate HTML file size: {file_size / 1024:.1f} KB")
        score -= 5

    # Check for inline styles (better to use external CSS)
    inline_style_count = html_content.count('style=')
    if inline_style_count > 20:
        issues.append(f"⚠️ Many inline styles found ({inline_style_count})")
        score -= 10

    # Check for external resources
    external_scripts = len(re.findall(r'<script[^>]*src=["\']https?://', html_content))
    if external_scripts > 5:
        issues.append(f"ℹ️ {external_scripts} external scripts (may impact load time)")
        score -= 5

    return {
        'score': max(score, 0),
        'issues': issues,
        'file_size_kb': file_size / 1024,
        'inline_styles': inline_style_count,
        'external_scripts': external_scripts
    }

def audit_file(file_path):
    """Audit a single HTML file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            html_content = f.read()

        # Parse HTML
        parser = HTMLAuditor()
        parser.feed(html_content)

        # Extract schema data
        schemas = extract_schema_data(html_content)

        # Run audits
        mobile_audit = audit_mobile_optimization(parser, file_path)
        seo_audit = audit_seo_optimization(parser, schemas, file_path, html_content)
        aeo_audit = audit_aeo_optimization(parser, schemas, file_path)
        performance_audit = audit_performance(html_content, file_path)

        # Calculate overall score
        overall_score = (
            mobile_audit['score'] * 0.25 +
            seo_audit['score'] * 0.35 +
            aeo_audit['score'] * 0.25 +
            performance_audit['score'] * 0.15
        )

        return {
            'file': str(file_path),
            'overall_score': round(overall_score, 1),
            'mobile': mobile_audit,
            'seo': seo_audit,
            'aeo': aeo_audit,
            'performance': performance_audit
        }

    except Exception as e:
        return {
            'file': str(file_path),
            'error': str(e),
            'overall_score': 0
        }

def generate_report(results, output_path):
    """Generate a comprehensive audit report"""

    # Calculate statistics
    total_files = len(results)
    avg_score = sum(r['overall_score'] for r in results) / total_files if total_files > 0 else 0

    # Count files by score range
    excellent = sum(1 for r in results if r['overall_score'] >= 90)
    good = sum(1 for r in results if 75 <= r['overall_score'] < 90)
    needs_improvement = sum(1 for r in results if 60 <= r['overall_score'] < 75)
    poor = sum(1 for r in results if r['overall_score'] < 60)

    # Generate markdown report
    report = f"""# ELDOA AI Website Audit Report
Generated: {Path(__file__).parent.parent}

## Executive Summary

- **Total Pages Audited**: {total_files}
- **Average Score**: {avg_score:.1f}/100
- **Score Distribution**:
  - 🌟 Excellent (90-100): {excellent} pages
  - ✅ Good (75-89): {good} pages
  - ⚠️ Needs Improvement (60-74): {needs_improvement} pages
  - ❌ Poor (<60): {poor} pages

## Score Breakdown by Category

| Category | Weight | Avg Score |
|----------|--------|-----------|
| SEO Optimization | 35% | {sum(r.get('seo', {}).get('score', 0) for r in results) / total_files:.1f}/100 |
| Mobile Optimization | 25% | {sum(r.get('mobile', {}).get('score', 0) for r in results) / total_files:.1f}/100 |
| AEO Optimization | 25% | {sum(r.get('aeo', {}).get('score', 0) for r in results) / total_files:.1f}/100 |
| Performance | 15% | {sum(r.get('performance', {}).get('score', 0) for r in results) / total_files:.1f}/100 |

---

## Key Findings

### Strengths ✅
"""

    # Identify strengths
    pages_with_schema = sum(1 for r in results if r.get('aeo', {}).get('has_structured_data', False))
    pages_with_viewport = sum(1 for r in results if r.get('mobile', {}).get('has_viewport', False))
    pages_with_og = sum(1 for r in results if r.get('seo', {}).get('has_og_tags', False))

    report += f"""
- **{pages_with_schema}/{total_files}** pages have Schema.org structured data
- **{pages_with_viewport}/{total_files}** pages have proper viewport meta tag
- **{pages_with_og}/{total_files}** pages have Open Graph tags
"""

    # Identify common issues
    report += "\n### Areas for Improvement ⚠️\n\n"

    # Collect all issues
    all_issues = defaultdict(int)
    for result in results:
        for category in ['mobile', 'seo', 'aeo', 'performance']:
            if category in result:
                for issue in result[category].get('issues', []):
                    if issue.startswith('❌') or issue.startswith('⚠️'):
                        all_issues[issue] += 1

    # Sort by frequency
    sorted_issues = sorted(all_issues.items(), key=lambda x: x[1], reverse=True)
    for issue, count in sorted_issues[:10]:  # Top 10 issues
        report += f"- {issue} ({count} pages)\n"

    # Detailed page results
    report += "\n---\n\n## Detailed Page Results\n\n"

    # Sort by score
    sorted_results = sorted(results, key=lambda x: x['overall_score'], reverse=True)

    for result in sorted_results:
        file_name = Path(result['file']).relative_to(Path(__file__).parent.parent)
        score = result['overall_score']

        # Score emoji
        if score >= 90:
            emoji = "🌟"
        elif score >= 75:
            emoji = "✅"
        elif score >= 60:
            emoji = "⚠️"
        else:
            emoji = "❌"

        report += f"\n### {emoji} {file_name} - Score: {score}/100\n\n"

        if 'error' in result:
            report += f"**Error**: {result['error']}\n\n"
            continue

        # SEO details
        if 'seo' in result:
            seo = result['seo']
            report += f"**SEO ({seo['score']}/100)**\n"
            report += f"- Title: `{seo.get('title', 'N/A')[:80]}...` ({seo.get('title_length', 0)} chars)\n"
            report += f"- Description: {seo.get('description_length', 0)} chars\n"
            report += f"- H1 tags: {seo.get('h1_count', 0)}\n"
            for issue in seo.get('issues', []):
                report += f"  - {issue}\n"
            report += "\n"

        # Mobile details
        if 'mobile' in result:
            mobile = result['mobile']
            report += f"**Mobile ({mobile['score']}/100)**\n"
            for issue in mobile.get('issues', []):
                report += f"  - {issue}\n"
            report += "\n"

        # AEO details
        if 'aeo' in result:
            aeo = result['aeo']
            report += f"**AEO ({aeo['score']}/100)**\n"
            if aeo.get('schema_types'):
                report += f"  - Schema types: {', '.join(aeo['schema_types'])}\n"
            for issue in aeo.get('issues', []):
                report += f"  - {issue}\n"
            report += "\n"

        # Performance details
        if 'performance' in result:
            perf = result['performance']
            report += f"**Performance ({perf['score']}/100)**\n"
            report += f"  - File size: {perf.get('file_size_kb', 0):.1f} KB\n"
            for issue in perf.get('issues', []):
                report += f"  - {issue}\n"
            report += "\n"

    # Recommendations
    report += """
---

## Recommendations

### High Priority
1. Ensure all pages have proper meta descriptions (120-160 characters)
2. Add Schema.org structured data to pages without it
3. Fix any missing H1 tags
4. Optimize images with proper alt text

### Medium Priority
1. Add FAQ schema to relevant pages for better AEO
2. Ensure all pages have Open Graph and Twitter Card tags
3. Optimize page file sizes (< 200KB recommended)
4. Review and fix any broken internal links

### Low Priority
1. Consider adding HowTo schema for tutorial content
2. Reduce inline styles where possible
3. Optimize external script loading
4. Add more structured data for rich snippets

---

## Next Steps

1. **Review pages with scores < 75** and address critical issues
2. **Implement missing Schema.org markup** for better AEO
3. **Optimize mobile experience** on any pages missing viewport tags
4. **Submit updated sitemap** to search engines after fixes
5. **Monitor performance** using tools like Google PageSpeed Insights

**Report End**
"""

    # Write report
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(report)

    print(f"\n✓ Detailed report saved to: {output_path}")

def main():
    """Main audit execution"""
    script_dir = Path(__file__).parent
    project_root = script_dir.parent

    print("=" * 70)
    print("ELDOA AI Website Audit")
    print("Mobile, SEO, and AEO Optimization Analysis")
    print("=" * 70)

    # Find all HTML files
    html_files = []

    # Main pages
    for pattern in ['*.html', 'public/**/*.html', 'videos/**/*.html', 'library/**/*.html']:
        html_files.extend(project_root.glob(pattern))

    # Filter out any duplicates
    html_files = list(set(html_files))

    print(f"\nFound {len(html_files)} HTML files to audit\n")

    # Audit all files
    results = []
    for i, file_path in enumerate(html_files, 1):
        rel_path = file_path.relative_to(project_root)
        print(f"[{i}/{len(html_files)}] Auditing: {rel_path}...", end=' ')

        result = audit_file(file_path)
        results.append(result)

        score = result.get('overall_score', 0)
        if score >= 90:
            print(f"🌟 {score}/100")
        elif score >= 75:
            print(f"✅ {score}/100")
        elif score >= 60:
            print(f"⚠️ {score}/100")
        else:
            print(f"❌ {score}/100")

    # Generate report
    print("\n" + "=" * 70)
    print("Generating detailed report...")
    print("=" * 70)

    report_path = project_root / 'audit-report.md'
    generate_report(results, report_path)

    # Generate JSON report for programmatic access
    json_path = project_root / 'audit-results.json'
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2)

    print(f"✓ JSON results saved to: {json_path}")

    # Summary
    avg_score = sum(r['overall_score'] for r in results) / len(results) if results else 0
    print("\n" + "=" * 70)
    print(f"Audit Complete!")
    print(f"Average Score: {avg_score:.1f}/100")
    print(f"Pages Audited: {len(results)}")
    print("=" * 70)

if __name__ == '__main__':
    main()
