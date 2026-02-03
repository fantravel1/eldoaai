#!/usr/bin/env python3
"""
Script to add homepage header and footer to all encyclopedia pages.
"""
import os
import re

# Header HTML to insert after <body> tag
HEADER_HTML = '''<a class="sr-only" href="#main">Skip to content</a>
<header role="banner" class="site-header">
  <div class="nav" aria-label="Primary">
    <a class="logo" href="/" aria-label="ELDOA AI Home">
      <span class="logo-mark" aria-hidden="true"></span>
      <span>ELDOA <span style="color:var(--brand)">AI</span></span>
    </a>
    <div class="nav-right">
      <nav class="nav-links" aria-label="Primary links">
        <a href="/diagnostic.html" class="btn">🎯 Diagnostic</a>
        <a href="/posture-check.html" class="btn">📐 Posture Check</a>
        <a href="/videos/" class="btn">📹 Videos</a>
        <a href="/practitioners.html" class="btn">🧑‍⚕️ Practitioners</a>
        <a href="/encyclopedia.html" class="btn">📖 Encyclopedia</a>
      </nav>
      <button id="menuToggle" class="hamburger" aria-label="Open menu" aria-expanded="false" aria-controls="mobileMenu">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="18" x2="21" y2="18"/></svg>
      </button>
      <button id="themeToggle" class="switch" aria-label="Toggle dark/light theme"><span></span></button>
    </div>
  </div>
  <div id="mobileMenu" class="mobile-menu" hidden>
    <div class="menu-inner">
      <a href="/diagnostic.html">🎯 Interactive Diagnostic</a>
      <a href="/posture-check.html">📐 Posture Check Tool</a>
      <a href="/videos/">📹 Complete Video Library</a>
      <a href="/practitioners.html">🧑‍⚕️ Find Practitioners</a>
      <a href="/encyclopedia.html">📖 Complete Encyclopedia</a>
      <a href="/kids/encyclopedia.html">🧒 Kids Encyclopedia</a>
    </div>
  </div>
</header>
<main id="main" role="main">
'''

# Footer HTML to insert before </body>
FOOTER_HTML = '''</main>
<footer class="site-footer" role="contentinfo">
  <div class="footer-inner">
    <div><strong>ELDOA AI</strong> — Knowledge • Videos • Practitioners</div>
    <div class="footer-links">
      <a href="/">Home</a>
      <a href="/what-is-eldoa.html">What is ELDOA?</a>
      <a href="/encyclopedia.html">Encyclopedia</a>
      <a href="/videos/">Videos</a>
      <a href="/about.html">About</a>
      <a href="/about.html#contact">Contact</a>
      <a href="/privacy.html">Privacy</a>
    </div>
    <small>Educational content only — not medical advice. Based on the work of Dr. Guy Voyer.</small>
  </div>
</footer>
<script>
// Theme toggle
(function(){
  const root = document.documentElement;
  const btn = document.getElementById('themeToggle');
  const key = 'theme';
  if (!btn) return;
  const setTheme = (mode) => {
    root.setAttribute('data-theme', mode);
    localStorage.setItem(key, mode);
  };
  const saved = localStorage.getItem(key);
  if (saved) setTheme(saved);
  else if (window.matchMedia('(prefers-color-scheme: dark)').matches) setTheme('dark');
  btn.addEventListener('click', () => setTheme((root.getAttribute('data-theme')||'light') === 'light' ? 'dark' : 'light'));
})();
// Mobile menu
(function(){
  const toggle = document.getElementById('menuToggle');
  const panel = document.getElementById('mobileMenu');
  if (!toggle || !panel) return;
  const open = () => { panel.hidden = false; panel.classList.add('open'); toggle.setAttribute('aria-expanded','true'); };
  const close = () => { panel.classList.remove('open'); toggle.setAttribute('aria-expanded','false'); setTimeout(()=>{ panel.hidden = true; }, 180); };
  toggle.addEventListener('click', ()=>{ panel.hidden || !panel.classList.contains('open') ? open() : close(); });
  panel.querySelectorAll('a').forEach(a=> a.addEventListener('click', close));
  window.addEventListener('keydown', (e)=>{ if (e.key === 'Escape') close(); });
  window.addEventListener('resize', ()=>{ if (window.innerWidth > 720 && !panel.hidden) close(); });
})();
</script>
'''

# CSS to add to <head>
HEADER_FOOTER_CSS = '''
/* Site-wide header/footer styles */
[data-theme="light"] {
  --bg: #ffffff;
  --fg: #0d0f13;
  --muted: #475569;
  --brand: #2f2fe6;
  --brand-2: #0891b2;
  --card: #f8fafc;
  --border: #e2e8f0;
}
[data-theme="dark"] {
  --bg: #0b0d12;
  --fg: #eef2ff;
  --muted: #c7d2fe;
  --brand: #8b5cf6;
  --brand-2: #22d3ee;
  --card: #111827;
  --border: #262b36;
}
html { scroll-behavior: smooth; }
body { background: var(--bg, #fff); color: var(--fg, #0d0f13); }
a { color: var(--brand, #2f2fe6); }
.sr-only { position:absolute !important; width:1px; height:1px; padding:0; margin:-1px; overflow:hidden; clip:rect(0,0,0,0); white-space:nowrap; border:0; }
.site-header { position: sticky; top: 0; z-index: 1000; backdrop-filter: saturate(1.2) blur(8px); background: color-mix(in oklab, var(--bg, #fff), transparent 20%); border-bottom: 1px solid var(--border, #e2e8f0); }
.site-header .nav { display:flex; align-items:center; justify-content:space-between; padding: .75rem 1rem; max-width: 1100px; margin: 0 auto; }
.site-header .logo { display:flex; align-items:center; gap:.6rem; font-weight:800; letter-spacing:.2px; text-decoration: none; color: var(--fg, #0d0f13); }
.site-header .logo-mark { width:32px; height:32px; border-radius:8px; background: conic-gradient(from 180deg at 50% 50%, var(--brand, #2f2fe6), var(--brand-2, #0891b2)); }
.site-header .nav-right { display:flex; align-items:center; gap:.75rem; }
.site-header .nav-links { display:flex; align-items:center; gap:.5rem; }
.site-header .btn { display:inline-flex; align-items:center; gap:.5rem; padding:.5rem .75rem; border-radius:10px; border:1px solid var(--border, #e2e8f0); background: color-mix(in oklab, var(--bg, #fff), var(--card, #f8fafc) 35%); color: var(--fg, #0d0f13); font-weight:600; font-size: .85rem; text-decoration: none; transition: filter .15s; }
.site-header .btn:hover { filter: brightness(1.03); text-decoration: none; }
.site-header .switch { cursor:pointer; border:1px solid var(--border, #e2e8f0); border-radius:999px; padding:.3rem; display:flex; align-items:center; background: transparent; }
.site-header .switch span { display:inline-block; width:20px; height:20px; border-radius:999px; background: var(--brand, #2f2fe6); }
.site-header .hamburger { display:none; width:40px; height:40px; border-radius:10px; border:1px solid var(--border, #e2e8f0); background: color-mix(in oklab, var(--bg, #fff), var(--card, #f8fafc) 35%); align-items:center; justify-content:center; cursor: pointer; }
.site-header .hamburger svg { width:22px; height:22px; }
.site-header .mobile-menu { position:fixed; left:0; right:0; top:56px; background: var(--bg, #fff); border-bottom:1px solid var(--border, #e2e8f0); box-shadow: 0 10px 30px rgba(0,0,0,0.1); z-index:999; transform: translateY(-8px); opacity:0; pointer-events:none; transition: transform .18s ease, opacity .18s ease; }
.site-header .mobile-menu.open { transform: translateY(0); opacity:1; pointer-events:auto; }
.site-header .mobile-menu .menu-inner { padding: .75rem 1rem; display:grid; gap:.5rem; max-width: 500px; margin: 0 auto; }
.site-header .mobile-menu a { display:block; padding:.9rem 1rem; border:1px solid var(--border, #e2e8f0); border-radius:12px; background: color-mix(in oklab, var(--bg, #fff), var(--card, #f8fafc) 35%); font-weight:600; text-align:center; text-decoration: none; color: var(--fg, #0d0f13); }
@media(max-width: 720px){
  .site-header .nav-links { display:none; }
  .site-header .hamburger { display:inline-flex; }
  .site-header .nav { padding: .5rem 1rem; }
  .site-header .btn { padding:.45rem .65rem; font-size: .8rem; }
}
.site-footer { padding:2rem 1rem 3rem; border-top:1px solid var(--border, #e2e8f0); color: var(--muted, #475569); margin-top: 2rem; background: var(--bg, #fff); }
.site-footer .footer-inner { max-width: 1100px; margin: 0 auto; display:grid; gap:1rem; }
.site-footer .footer-links { display:flex; gap:.75rem; flex-wrap:wrap; }
.site-footer a { color: var(--brand, #2f2fe6); text-decoration: none; }
.site-footer a:hover { text-decoration: underline; }
.site-footer small { font-size: .85rem; }
'''

def process_encyclopedia_file(filepath):
    """Process a single encyclopedia HTML file to add header and footer."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Skip if already processed
        if 'site-header' in content:
            return False

        # Remove the old dynamic loader if present
        content = content.replace('<script src="/assets/js/encyclopedia-layout.js"></script>\n', '')
        content = content.replace('<script src="/assets/js/encyclopedia-layout.js"></script>', '')

        # Add data-theme attribute to html tag if not present
        if 'data-theme' not in content:
            content = re.sub(r'<html([^>]*)>', r'<html\1 data-theme="light">', content)

        # Add header/footer CSS before </style>
        if HEADER_FOOTER_CSS.strip() not in content:
            content = content.replace('</style></head>', HEADER_FOOTER_CSS + '</style></head>')

        # Add header after <body...>
        body_match = re.search(r'<body[^>]*>', content)
        if body_match:
            body_tag = body_match.group(0)
            content = content.replace(body_tag, body_tag + '\n' + HEADER_HTML)

        # Add footer before </body>
        # First, remove any existing back-link that will be in the footer
        # Then add footer
        content = content.replace('</body>', FOOTER_HTML + '</body>')

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

        return True
    except Exception as e:
        print(f"Error processing {filepath}: {e}")
        return False

def main():
    # Process encyclopedia pages
    encyclopedia_dir = '/home/user/eldoaai/encyclopedia'
    kids_encyclopedia_dir = '/home/user/eldoaai/kids/encyclopedia'

    processed = 0
    skipped = 0

    # Process main encyclopedia
    if os.path.exists(encyclopedia_dir):
        for filename in os.listdir(encyclopedia_dir):
            if filename.endswith('.html'):
                filepath = os.path.join(encyclopedia_dir, filename)
                if process_encyclopedia_file(filepath):
                    processed += 1
                else:
                    skipped += 1

    print(f"Main encyclopedia: Processed {processed}, Skipped {skipped}")

    # Process kids encyclopedia
    processed_kids = 0
    skipped_kids = 0

    if os.path.exists(kids_encyclopedia_dir):
        for filename in os.listdir(kids_encyclopedia_dir):
            if filename.endswith('.html'):
                filepath = os.path.join(kids_encyclopedia_dir, filename)
                if process_encyclopedia_file(filepath):
                    processed_kids += 1
                else:
                    skipped_kids += 1

    print(f"Kids encyclopedia: Processed {processed_kids}, Skipped {skipped_kids}")
    print(f"Total: Processed {processed + processed_kids}, Skipped {skipped + skipped_kids}")

if __name__ == '__main__':
    main()
