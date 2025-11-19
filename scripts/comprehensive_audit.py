#!/usr/bin/env python3
"""
Comprehensive Website Audit for SEO, AEO, and Mobile Optimization
Audits all HTML files in the public directory
"""

import os
import json
import re
from pathlib import Path
from bs4 import BeautifulSoup
from collections import defaultdict

class WebsiteAuditor:
    def __init__(self, public_dir):
        self.public_dir = Path(public_dir)
        self.results = {
            'summary': {},
            'seo_scores': [],
            'aeo_scores': [],
            'mobile_scores': [],
            'issues': defaultdict(list),
            'recommendations': []
        }

    def audit_seo(self, soup, file_path, url):
        """Audit SEO factors"""
        score = 0
        max_score = 100
        issues = []

        # Title tag (10 points)
        title = soup.find('title')
        if title and title.string:
            title_text = title.string.strip()
            if 30 <= len(title_text) <= 60:
                score += 10
            elif len(title_text) > 0:
                score += 5
                issues.append(f"Title length ({len(title_text)}) not optimal (30-60 chars)")
        else:
            issues.append("Missing title tag")

        # Meta description (10 points)
        meta_desc = soup.find('meta', {'name': 'description'})
        if meta_desc and meta_desc.get('content'):
            desc_text = meta_desc['content']
            if 120 <= len(desc_text) <= 160:
                score += 10
            elif len(desc_text) > 0:
                score += 5
                issues.append(f"Meta description length ({len(desc_text)}) not optimal (120-160 chars)")
        else:
            issues.append("Missing meta description")

        # Canonical URL (5 points)
        canonical = soup.find('link', {'rel': 'canonical'})
        if canonical and canonical.get('href'):
            score += 5
        else:
            issues.append("Missing canonical URL")

        # H1 tag (10 points)
        h1_tags = soup.find_all('h1')
        if len(h1_tags) == 1:
            score += 10
        elif len(h1_tags) > 1:
            score += 5
            issues.append(f"Multiple H1 tags found ({len(h1_tags)}), should have exactly 1")
        else:
            issues.append("Missing H1 tag")

        # Heading hierarchy (5 points)
        headings = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
        if headings:
            score += 5

        # Open Graph tags (10 points)
        og_tags = soup.find_all('meta', property=re.compile('^og:'))
        required_og = ['og:title', 'og:description', 'og:url', 'og:type']
        og_present = [tag.get('property') for tag in og_tags]
        og_score = sum(5 if req in og_present else 0 for req in required_og[:2])
        og_score += sum(2.5 if req in og_present else 0 for req in required_og[2:])
        score += og_score
        if og_score < 10:
            missing_og = [tag for tag in required_og if tag not in og_present]
            issues.append(f"Missing Open Graph tags: {', '.join(missing_og)}")

        # Twitter Card tags (5 points)
        twitter_tags = soup.find_all('meta', {'name': re.compile('^twitter:')})
        if len(twitter_tags) >= 3:
            score += 5
        elif twitter_tags:
            score += 2.5

        # Schema.org structured data (15 points)
        schema_scripts = soup.find_all('script', {'type': 'application/ld+json'})
        if schema_scripts:
            schema_score = min(15, len(schema_scripts) * 7.5)
            score += schema_score
            if schema_score < 15:
                issues.append(f"Limited structured data ({len(schema_scripts)} schemas)")
        else:
            issues.append("Missing Schema.org structured data")

        # Meta keywords (5 points)
        meta_keywords = soup.find('meta', {'name': 'keywords'})
        if meta_keywords and meta_keywords.get('content'):
            score += 5

        # Robots meta (5 points)
        meta_robots = soup.find('meta', {'name': 'robots'})
        if meta_robots and meta_robots.get('content'):
            score += 5

        # Images with alt text (5 points)
        images = soup.find_all('img')
        if images:
            images_with_alt = [img for img in images if img.get('alt')]
            alt_percentage = len(images_with_alt) / len(images) * 100
            score += (alt_percentage / 100) * 5
            if alt_percentage < 100:
                issues.append(f"Only {alt_percentage:.0f}% of images have alt text")

        # Internal links (5 points)
        internal_links = soup.find_all('a', href=re.compile('^/'))
        if internal_links:
            score += 5

        # Favicon (5 points)
        favicon = soup.find('link', rel='icon') or soup.find('link', rel='shortcut icon')
        if favicon:
            score += 5

        # Theme color (5 points)
        theme_color = soup.find('meta', {'name': 'theme-color'})
        if theme_color:
            score += 5

        return {
            'score': min(score, max_score),
            'max_score': max_score,
            'percentage': min(score / max_score * 100, 100),
            'issues': issues,
            'url': url,
            'file': str(file_path)
        }

    def audit_aeo(self, soup, file_path, url):
        """Audit Answer Engine Optimization (AEO) factors"""
        score = 0
        max_score = 100
        issues = []

        # Structured data presence (30 points)
        schema_scripts = soup.find_all('script', {'type': 'application/ld+json'})
        if schema_scripts:
            # Parse and check schema types
            schema_types = []
            for script in schema_scripts:
                try:
                    schema_data = json.loads(script.string)
                    schema_type = schema_data.get('@type', '')
                    schema_types.append(schema_type)
                except:
                    pass

            # Award points for different schema types
            if 'DefinedTerm' in schema_types:
                score += 10
            if 'BreadcrumbList' in schema_types:
                score += 5
            if any(t in schema_types for t in ['Article', 'BlogPosting', 'NewsArticle']):
                score += 5
            if any(t in schema_types for t in ['VideoObject', 'VideoGallery']):
                score += 5
            if any(t in schema_types for t in ['FAQPage', 'QAPage', 'HowTo']):
                score += 5

            # Base points for having any structured data
            if not score:
                score += 10
        else:
            issues.append("No structured data for answer engines")

        # Clear, concise content (15 points)
        paragraphs = soup.find_all('p')
        if paragraphs:
            score += 10
            # Check for short, scannable paragraphs
            avg_para_length = sum(len(p.get_text()) for p in paragraphs) / len(paragraphs)
            if 50 <= avg_para_length <= 200:
                score += 5

        # Headings for topic structure (15 points)
        h2_tags = soup.find_all('h2')
        if h2_tags:
            score += 10
            if len(h2_tags) >= 3:
                score += 5
        else:
            issues.append("No H2 headings for content structure")

        # Lists (ordered or unordered) (10 points)
        lists = soup.find_all(['ul', 'ol'])
        if lists:
            score += 10
        else:
            issues.append("No lists - answer engines favor listed content")

        # Links to related content (10 points)
        internal_links = soup.find_all('a', href=re.compile('^/'))
        if len(internal_links) >= 5:
            score += 10
        elif internal_links:
            score += 5
        else:
            issues.append("Limited internal linking")

        # Breadcrumbs (10 points)
        breadcrumb_schema = False
        for script in schema_scripts:
            try:
                schema_data = json.loads(script.string)
                if schema_data.get('@type') == 'BreadcrumbList':
                    breadcrumb_schema = True
                    break
            except:
                pass

        if breadcrumb_schema:
            score += 10
        else:
            issues.append("No breadcrumb schema for navigation context")

        # Descriptive link text (5 points)
        links = soup.find_all('a')
        if links:
            descriptive_links = [l for l in links if l.get_text().strip() and
                               l.get_text().strip().lower() not in ['click here', 'read more', 'here']]
            if len(descriptive_links) / len(links) > 0.9:
                score += 5

        # Table of contents or navigation (5 points)
        nav = soup.find('nav') or soup.find(class_=re.compile('nav|menu|toc'))
        if nav:
            score += 5

        return {
            'score': min(score, max_score),
            'max_score': max_score,
            'percentage': min(score / max_score * 100, 100),
            'issues': issues,
            'url': url,
            'file': str(file_path)
        }

    def audit_mobile(self, soup, file_path, url):
        """Audit mobile optimization factors"""
        score = 0
        max_score = 100
        issues = []

        # Viewport meta tag (20 points)
        viewport = soup.find('meta', {'name': 'viewport'})
        if viewport and viewport.get('content'):
            content = viewport['content']
            if 'width=device-width' in content:
                score += 15
            if 'initial-scale=1' in content:
                score += 5
        else:
            issues.append("Missing viewport meta tag - critical for mobile")

        # Responsive CSS (20 points)
        style_tags = soup.find_all('style')
        has_media_queries = False
        for style in style_tags:
            if style.string and '@media' in style.string:
                has_media_queries = True
                # Check for common breakpoints
                if 'max-width: 768px' in style.string or 'max-width: 767px' in style.string:
                    score += 20
                    break
                else:
                    score += 10
                    break

        if not has_media_queries:
            issues.append("No CSS media queries found for responsive design")

        # Font size readability (10 points)
        body = soup.find('body')
        if body:
            # Check for reasonable font sizes in CSS
            for style in style_tags:
                if style.string and 'font-size' in style.string:
                    score += 10
                    break

        # Touch-friendly elements (15 points)
        # Check for reasonable button/link sizing
        buttons = soup.find_all(['button', 'a'])
        if buttons:
            score += 10
            # Check for padding in styles
            for style in style_tags:
                if style.string and 'padding' in style.string:
                    score += 5
                    break

        # No horizontal scrolling (10 points)
        # Check for max-width or overflow handling
        for style in style_tags:
            if style.string and ('max-width' in style.string or 'overflow-x' in style.string):
                score += 10
                break

        # Optimized images (10 points)
        images = soup.find_all('img')
        if images:
            # Check if images have width/height or are in responsive containers
            responsive_images = [img for img in images if
                               img.get('width') or img.get('height') or
                               img.parent.get('class') and 'responsive' in str(img.parent.get('class'))]
            if len(responsive_images) / len(images) > 0.5:
                score += 10
            elif responsive_images:
                score += 5
        else:
            score += 5  # No images to optimize

        # Fast loading (5 points)
        # Check for minimal inline styles and scripts
        inline_scripts = soup.find_all('script', src=False)
        if len(inline_scripts) < 5:
            score += 5

        # Mobile-friendly navigation (10 points)
        nav = soup.find('nav')
        if nav:
            score += 5
            # Check for mobile menu indicators in classes
            if nav.find(class_=re.compile('mobile|hamburger|menu-toggle')):
                score += 5

        return {
            'score': min(score, max_score),
            'max_score': max_score,
            'percentage': min(score / max_score * 100, 100),
            'issues': issues,
            'url': url,
            'file': str(file_path)
        }

    def audit_file(self, file_path):
        """Audit a single HTML file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            soup = BeautifulSoup(content, 'html.parser')

            # Generate URL from file path
            rel_path = file_path.relative_to(self.public_dir)
            if rel_path.name == 'index.html':
                url = f"https://eldoa.ai/{rel_path.parent}/"
            else:
                url = f"https://eldoa.ai/{rel_path.with_suffix('')}"

            # Run all audits
            seo_result = self.audit_seo(soup, file_path, url)
            aeo_result = self.audit_aeo(soup, file_path, url)
            mobile_result = self.audit_mobile(soup, file_path, url)

            return {
                'file': str(file_path),
                'url': url,
                'seo': seo_result,
                'aeo': aeo_result,
                'mobile': mobile_result,
                'overall': {
                    'score': (seo_result['percentage'] + aeo_result['percentage'] + mobile_result['percentage']) / 3,
                    'seo_score': seo_result['percentage'],
                    'aeo_score': aeo_result['percentage'],
                    'mobile_score': mobile_result['percentage']
                }
            }

        except Exception as e:
            return {
                'file': str(file_path),
                'error': str(e)
            }

    def run_audit(self):
        """Run audit on all HTML files"""
        html_files = list(self.public_dir.rglob('*.html'))

        print(f"Found {len(html_files)} HTML files to audit")
        print("Running comprehensive audit...\n")

        all_results = []
        seo_scores = []
        aeo_scores = []
        mobile_scores = []
        overall_scores = []

        for i, file_path in enumerate(html_files, 1):
            if i % 50 == 0:
                print(f"Progress: {i}/{len(html_files)} files audited")

            result = self.audit_file(file_path)
            if 'error' not in result:
                all_results.append(result)
                seo_scores.append(result['seo']['percentage'])
                aeo_scores.append(result['aeo']['percentage'])
                mobile_scores.append(result['mobile']['percentage'])
                overall_scores.append(result['overall']['score'])

        # Calculate statistics
        self.results['summary'] = {
            'total_files': len(html_files),
            'audited_files': len(all_results),
            'average_seo_score': sum(seo_scores) / len(seo_scores) if seo_scores else 0,
            'average_aeo_score': sum(aeo_scores) / len(aeo_scores) if aeo_scores else 0,
            'average_mobile_score': sum(mobile_scores) / len(mobile_scores) if mobile_scores else 0,
            'average_overall_score': sum(overall_scores) / len(overall_scores) if overall_scores else 0,
            'min_seo_score': min(seo_scores) if seo_scores else 0,
            'max_seo_score': max(seo_scores) if seo_scores else 0,
            'min_aeo_score': min(aeo_scores) if aeo_scores else 0,
            'max_aeo_score': max(aeo_scores) if aeo_scores else 0,
            'min_mobile_score': min(mobile_scores) if mobile_scores else 0,
            'max_mobile_score': max(mobile_scores) if mobile_scores else 0,
        }

        # Find pages with issues
        pages_with_seo_issues = [r for r in all_results if r['seo']['percentage'] < 80]
        pages_with_aeo_issues = [r for r in all_results if r['aeo']['percentage'] < 70]
        pages_with_mobile_issues = [r for r in all_results if r['mobile']['percentage'] < 80]

        self.results['pages_needing_attention'] = {
            'seo': len(pages_with_seo_issues),
            'aeo': len(pages_with_aeo_issues),
            'mobile': len(pages_with_mobile_issues)
        }

        # Collect all issues
        all_seo_issues = []
        all_aeo_issues = []
        all_mobile_issues = []

        for result in all_results:
            all_seo_issues.extend(result['seo']['issues'])
            all_aeo_issues.extend(result['aeo']['issues'])
            all_mobile_issues.extend(result['mobile']['issues'])

        # Count issue frequency
        from collections import Counter
        seo_issue_counts = Counter(all_seo_issues)
        aeo_issue_counts = Counter(all_aeo_issues)
        mobile_issue_counts = Counter(all_mobile_issues)

        self.results['common_issues'] = {
            'seo': dict(seo_issue_counts.most_common(10)),
            'aeo': dict(aeo_issue_counts.most_common(10)),
            'mobile': dict(mobile_issue_counts.most_common(10))
        }

        # Find top and bottom performers
        sorted_by_overall = sorted(all_results, key=lambda x: x['overall']['score'], reverse=True)

        self.results['top_performers'] = sorted_by_overall[:10]
        self.results['needs_improvement'] = sorted_by_overall[-10:]

        return self.results

    def print_report(self):
        """Print audit report"""
        print("\n" + "="*80)
        print("COMPREHENSIVE WEBSITE AUDIT REPORT")
        print("="*80)

        summary = self.results['summary']

        print(f"\n📊 OVERALL SUMMARY")
        print(f"Total files audited: {summary['audited_files']}")
        print(f"\nAverage Scores:")
        print(f"  SEO Score:    {summary['average_seo_score']:.1f}/100")
        print(f"  AEO Score:    {summary['average_aeo_score']:.1f}/100")
        print(f"  Mobile Score: {summary['average_mobile_score']:.1f}/100")
        print(f"  Overall Score: {summary['average_overall_score']:.1f}/100")

        print(f"\n📈 SCORE RANGES")
        print(f"  SEO:    {summary['min_seo_score']:.1f} - {summary['max_seo_score']:.1f}")
        print(f"  AEO:    {summary['min_aeo_score']:.1f} - {summary['max_aeo_score']:.1f}")
        print(f"  Mobile: {summary['min_mobile_score']:.1f} - {summary['max_mobile_score']:.1f}")

        needs_attn = self.results['pages_needing_attention']
        print(f"\n⚠️  PAGES NEEDING ATTENTION")
        print(f"  SEO issues (<80):    {needs_attn['seo']} pages")
        print(f"  AEO issues (<70):    {needs_attn['aeo']} pages")
        print(f"  Mobile issues (<80): {needs_attn['mobile']} pages")

        print(f"\n🔍 MOST COMMON ISSUES")

        print(f"\n  SEO Issues:")
        for issue, count in list(self.results['common_issues']['seo'].items())[:5]:
            print(f"    • {issue} ({count} pages)")

        print(f"\n  AEO Issues:")
        for issue, count in list(self.results['common_issues']['aeo'].items())[:5]:
            print(f"    • {issue} ({count} pages)")

        print(f"\n  Mobile Issues:")
        for issue, count in list(self.results['common_issues']['mobile'].items())[:5]:
            print(f"    • {issue} ({count} pages)")

        print(f"\n⭐ TOP 5 PERFORMING PAGES")
        for i, page in enumerate(self.results['top_performers'][:5], 1):
            print(f"  {i}. {page['url']}")
            print(f"     Overall: {page['overall']['score']:.1f} | SEO: {page['seo']['percentage']:.1f} | AEO: {page['aeo']['percentage']:.1f} | Mobile: {page['mobile']['percentage']:.1f}")

        print(f"\n🔧 BOTTOM 5 PAGES (Need Improvement)")
        for i, page in enumerate(self.results['needs_improvement'][:5], 1):
            print(f"  {i}. {page['url']}")
            print(f"     Overall: {page['overall']['score']:.1f} | SEO: {page['seo']['percentage']:.1f} | AEO: {page['aeo']['percentage']:.1f} | Mobile: {page['mobile']['percentage']:.1f}")

        print("\n" + "="*80)

        # Grade the overall website
        overall_score = summary['average_overall_score']
        if overall_score >= 90:
            grade = "A+ (Excellent)"
        elif overall_score >= 80:
            grade = "A (Very Good)"
        elif overall_score >= 70:
            grade = "B (Good)"
        elif overall_score >= 60:
            grade = "C (Fair)"
        else:
            grade = "D (Needs Improvement)"

        print(f"\n🎯 OVERALL WEBSITE GRADE: {grade}")
        print("="*80 + "\n")

def main():
    public_dir = Path('/home/user/eldoaai/public')

    auditor = WebsiteAuditor(public_dir)
    results = auditor.run_audit()
    auditor.print_report()

    # Save detailed results to JSON
    output_file = Path('/home/user/eldoaai/audit-report.json')
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2)

    print(f"✅ Detailed audit results saved to: {output_file}")

if __name__ == "__main__":
    main()
