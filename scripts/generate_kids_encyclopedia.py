#!/usr/bin/env python3
"""
Generate kid-friendly encyclopedia pages for all entries
"""

import json
import os
import re
from pathlib import Path

# Paths
DATA_FILE = "/home/user/eldoaai/public/encyclopedia-data.json"
OUTPUT_DIR = "/home/user/eldoaai/kids/encyclopedia"
KIDS_INDEX_FILE = "/home/user/eldoaai/kids/encyclopedia.html"

# Emoji mapping for different topics
EMOJI_MAP = {
    # Body parts
    'achilles': '🦶', 'ankle': '🦶', 'foot': '🦶', 'feet': '🦶',
    'neck': '🦒', 'cervical': '🦒', 'head': '🧠',
    'back': '🦴', 'spine': '🦴', 'spinal': '🦴', 'vertebral': '🦴',
    'shoulder': '💪', 'arm': '💪', 'elbow': '💪',
    'hip': '🦵', 'knee': '🦵', 'leg': '🦵',
    'muscle': '💪', 'muscular': '💪',
    # Actions
    'breathing': '💨', 'breath': '💨',
    'stretch': '🤸', 'flexibility': '🤸',
    'balance': '⚖️', 'stability': '⚖️',
    'posture': '🧘', 'alignment': '🧘',
    'exercise': '🏃', 'training': '🏃', 'practice': '🏃',
    # Sports
    'baseball': '⚾', 'hockey': '🏒', 'golf': '⛳', 'tennis': '🎾',
    'skiing': '⛷️', 'alpine': '⛷️', 'cycling': '🚴',
    # Concepts
    'pain': '🤕', 'injury': '🤕', 'hurt': '🤕',
    'health': '💚', 'wellness': '💚',
    'learning': '📚', 'education': '📚', 'study': '📚',
    'fascial': '🕸️', 'tissue': '🕸️',
    'assessment': '🔍', 'diagnosis': '🔍',
    # Default
    'default': '⭐'
}

def get_emoji(title):
    """Get emoji based on title keywords"""
    title_lower = title.lower()
    for keyword, emoji in EMOJI_MAP.items():
        if keyword in title_lower:
            return emoji
    return EMOJI_MAP['default']

def get_color_class(index):
    """Get rotating color class for cards"""
    colors = ['color-1', 'color-2', 'color-3', 'color-4']
    return colors[index % len(colors)]

def create_slug(title):
    """Create URL-friendly slug"""
    slug = title.lower()
    slug = re.sub(r'[^\w\s-]', '', slug)
    slug = re.sub(r'[-\s]+', '-', slug)
    return slug

def read_content_from_html(html_file_path):
    """Extract content from encyclopedia HTML file"""
    try:
        with open(html_file_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
            # Extract content between <div class="entry-content"> tags
            import re
            match = re.search(r'<div class="entry-content">\s*<p>(.*?)</p>\s*</div>', html_content, re.DOTALL)
            if match:
                content = match.group(1)
                # Clean up the content - remove </p><p> tags and replace with spaces
                content = re.sub(r'</p><p>', ' ', content)
                return content
    except Exception as e:
        print(f"Error reading {html_file_path}: {e}")
    return "Learn about this term in the ELDOA encyclopedia!"

def create_kids_entry_page(entry, color_class, encyclopedia_dir):
    """Create individual HTML page for a kids encyclopedia entry"""
    title = entry['title']
    slug = entry['slug']
    emoji = get_emoji(title)

    # Read content from encyclopedia HTML file
    html_file_path = os.path.join(encyclopedia_dir, f"{slug}.html")
    content = read_content_from_html(html_file_path)

    html = f'''<!doctype html>
<html lang="en" data-theme="light">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1"/>
  <title>{title} - ELDOA for Kids | ELDOA AI</title>
  <meta name="description" content="Learn about {title} in a fun, kid-friendly way!"/>
  <link rel="canonical" href="https://eldoa.ai/kids/encyclopedia/{slug}.html"/>

  <style>
    :root {{
      --bg: #fffef9;
      --fg: #1a1a1a;
      --muted: #666;
      --brand: #ff6b6b;
      --brand-2: #4ecdc4;
      --brand-3: #ffe66d;
      --brand-4: #a8dadc;
      --card: #fff;
      --border: #e0e0e0;
    }}

    [data-theme="dark"] {{
      --bg: #1a1a2e;
      --fg: #f0f0f0;
      --muted: #b0b0b0;
      --card: #252540;
      --border: #3a3a52;
    }}

    * {{ box-sizing: border-box; margin: 0; padding: 0; }}

    body {{
      font-family: 'Comic Sans MS', 'Chalkboard SE', 'Comic Neue', cursive, system-ui, sans-serif;
      background: var(--bg);
      color: var(--fg);
      line-height: 1.7;
      min-height: 100vh;
    }}

    .container {{
      width: min(800px, 94vw);
      margin: 0 auto;
      padding: 1rem;
    }}

    header {{
      background: linear-gradient(135deg, var(--brand), var(--brand-2));
      color: white;
      padding: 2rem 1rem;
      text-align: center;
      border-radius: 0 0 24px 24px;
      margin-bottom: 2rem;
    }}

    .emoji {{
      font-size: 4rem;
      display: block;
      margin-bottom: 1rem;
    }}

    h1 {{
      font-size: clamp(2rem, 5vw, 3rem);
      margin-bottom: .5rem;
      text-shadow: 2px 2px 4px rgba(0,0,0,.2);
    }}

    .subtitle {{
      font-size: 1.2rem;
      opacity: .95;
    }}

    .content-card {{
      background: var(--card);
      border: 3px solid;
      border-radius: 20px;
      padding: 2rem;
      margin: 2rem 0;
      box-shadow: 0 4px 12px rgba(0,0,0,.1);
    }}

    .content-card.color-1 {{ border-color: var(--brand); }}
    .content-card.color-2 {{ border-color: var(--brand-2); }}
    .content-card.color-3 {{ border-color: var(--brand-3); }}
    .content-card.color-4 {{ border-color: var(--brand-4); }}

    .content-card p {{
      font-size: clamp(1.1rem, 2.5vw, 1.3rem);
      line-height: 1.8;
      margin-bottom: 1rem;
    }}

    .fun-fact {{
      background: linear-gradient(135deg, #fff3cd, #ffe66d);
      border-left: 4px solid #ffc107;
      padding: 1.5rem;
      margin: 2rem 0;
      border-radius: 12px;
    }}

    .fun-fact strong {{
      color: #d68400;
      font-size: 1.2rem;
    }}

    .back-links {{
      display: flex;
      gap: 1rem;
      flex-wrap: wrap;
      margin-top: 2rem;
    }}

    .back-link {{
      display: inline-block;
      padding: .75rem 1.5rem;
      background: var(--brand-2);
      color: white;
      text-decoration: none;
      border-radius: 12px;
      font-weight: 700;
      transition: all .2s;
    }}

    .back-link:hover {{
      background: var(--brand);
      transform: translateY(-2px);
    }}

    @media (max-width: 600px) {{
      .emoji {{
        font-size: 3rem;
      }}

      h1 {{
        font-size: 1.75rem;
      }}

      .content-card {{
        padding: 1.5rem;
      }}
    }}
  </style>
</head>
<body>
  <header>
    <div class="container">
      <span class="emoji">{emoji}</span>
      <h1>{title}</h1>
      <p class="subtitle">Part of the ELDOA for Kids Encyclopedia</p>
    </div>
  </header>

  <div class="container">
    <div class="content-card {color_class}">
      <p>{content}</p>
    </div>

    <div class="fun-fact">
      <strong>💡 Did you know?</strong> Every term in the ELDOA encyclopedia helps you understand how your amazing body works! Learning about your body is like learning the instruction manual for the most incredible machine ever made - YOU!
    </div>

    <div class="back-links">
      <a href="/kids/encyclopedia.html" class="back-link">← All Kids Encyclopedia</a>
      <a href="/kids/" class="back-link">📚 Kids Home</a>
      <a href="/" class="back-link">🏠 Main Site</a>
    </div>
  </div>
</body>
</html>'''

    return html

def create_kids_index_page(entries_by_letter, total_entries):
    """Create the kids encyclopedia index page"""
    html = '''<!doctype html>
<html lang="en" data-theme="light">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1"/>
  <title>ELDOA Encyclopedia for Kids - Learn About Your Body! | ELDOA AI</title>
  <meta name="description" content="Kid-friendly encyclopedia with ''' + str(total_entries) + ''' entries about ELDOA, your spine, and staying healthy. Learn about your body in simple, fun language!"/>
  <link rel="canonical" href="https://eldoa.ai/kids/encyclopedia.html"/>

  <style>
    :root {
      --bg: #fffef9;
      --fg: #1a1a1a;
      --muted: #666;
      --brand: #ff6b6b;
      --brand-2: #4ecdc4;
      --brand-3: #ffe66d;
      --brand-4: #a8dadc;
      --card: #fff;
      --border: #e0e0e0;
    }

    [data-theme="dark"] {
      --bg: #1a1a2e;
      --fg: #f0f0f0;
      --muted: #b0b0b0;
      --card: #252540;
      --border: #3a3a52;
    }

    * { box-sizing: border-box; margin: 0; padding: 0; }

    body {
      font-family: 'Comic Sans MS', 'Chalkboard SE', 'Comic Neue', cursive, system-ui, sans-serif;
      background: var(--bg);
      color: var(--fg);
      line-height: 1.7;
    }

    .container {
      width: min(1000px, 94vw);
      margin: 0 auto;
      padding: 1rem;
    }

    header {
      background: linear-gradient(135deg, var(--brand), var(--brand-2));
      color: white;
      padding: 3rem 1rem;
      text-align: center;
      border-radius: 0 0 24px 24px;
      margin-bottom: 2rem;
    }

    h1 {
      font-size: clamp(2rem, 5vw, 3.5rem);
      margin-bottom: .5rem;
      text-shadow: 2px 2px 4px rgba(0,0,0,.2);
    }

    .subtitle {
      font-size: clamp(1.1rem, 3vw, 1.4rem);
      opacity: .95;
    }

    .search-box {
      max-width: 600px;
      margin: 2rem auto;
    }

    .search-box input {
      width: 100%;
      padding: 1rem 1.5rem;
      font-size: 1.1rem;
      border: 3px solid var(--brand-2);
      border-radius: 16px;
      font-family: inherit;
      background: white;
    }

    .search-box input:focus {
      outline: none;
      border-color: var(--brand);
      box-shadow: 0 0 0 3px rgba(255, 107, 107, 0.1);
    }

    .alphabet-nav {
      display: flex;
      flex-wrap: wrap;
      gap: .5rem;
      margin: 2rem 0;
      justify-content: center;
      position: sticky;
      top: 0;
      background: var(--bg);
      padding: 1rem 0;
      z-index: 10;
      border-bottom: 3px dashed var(--brand-3);
    }

    .letter-btn {
      width: 44px;
      height: 44px;
      border: 2px solid var(--brand);
      border-radius: 12px;
      background: white;
      color: var(--brand);
      font-weight: 800;
      font-size: 1.2rem;
      cursor: pointer;
      transition: all .2s;
      text-decoration: none;
      display: flex;
      align-items: center;
      justify-content: center;
    }

    .letter-btn:hover, .letter-btn.active {
      background: var(--brand);
      color: white;
      transform: scale(1.1);
    }

    .letter-section {
      margin: 3rem 0;
    }

    .letter-section h2 {
      font-size: 3rem;
      color: var(--brand);
      margin-bottom: 1.5rem;
      text-align: center;
      text-shadow: 2px 2px var(--brand-3);
    }

    .entries-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
      gap: 1.5rem;
      margin: 1.5rem 0;
    }

    .entry-card {
      background: var(--card);
      border: 3px solid;
      border-radius: 20px;
      padding: 1.5rem;
      text-decoration: none;
      color: var(--fg);
      transition: all .2s;
      box-shadow: 0 4px 12px rgba(0,0,0,.1);
    }

    .entry-card:hover {
      transform: translateY(-4px);
      box-shadow: 0 8px 20px rgba(0,0,0,.15);
    }

    .entry-card.color-1 { border-color: var(--brand); }
    .entry-card.color-2 { border-color: var(--brand-2); }
    .entry-card.color-3 { border-color: var(--brand-3); }
    .entry-card.color-4 { border-color: var(--brand-4); }

    .entry-card h3 {
      font-size: clamp(1.1rem, 3vw, 1.4rem);
      margin-bottom: .5rem;
      color: var(--brand);
    }

    .emoji {
      font-size: 1.8rem;
      margin-right: .5rem;
    }

    .back-link {
      display: inline-block;
      padding: .75rem 1.5rem;
      background: var(--brand-2);
      color: white;
      text-decoration: none;
      border-radius: 12px;
      font-weight: 700;
      margin: 2rem 0;
    }

    .back-link:hover {
      background: var(--brand);
    }

    .no-results {
      text-align: center;
      padding: 3rem;
      font-size: 1.3rem;
      color: var(--muted);
      display: none;
    }

    .no-results.show {
      display: block;
    }

    @media (max-width: 600px) {
      .entries-grid {
        grid-template-columns: 1fr;
      }

      .letter-btn {
        width: 38px;
        height: 38px;
        font-size: 1rem;
      }
    }
  </style>
</head>
<body>
  <header>
    <div class="container">
      <h1><span class="emoji">📚</span> ELDOA Encyclopedia for Kids</h1>
      <p class="subtitle">''' + str(total_entries) + ''' Fun Terms to Learn About Your Amazing Body!</p>
    </div>
  </header>

  <div class="container">
    <a href="/kids/" class="back-link">← Back to Kids Home</a>

    <div class="search-box">
      <input type="search" id="searchInput" placeholder="🔍 Search for a word..." autocomplete="off" />
    </div>

    <div class="alphabet-nav" id="alphabetNav">
'''

    # Add alphabet navigation
    letters = sorted(entries_by_letter.keys())
    for letter in letters:
        html += f'      <a href="#letter-{letter}" class="letter-btn">{letter}</a>\n'

    html += '''    </div>

    <div id="entriesContainer">
'''

    # Add letter sections with entries
    for letter in letters:
        html += f'''      <div class="letter-section" id="letter-{letter}">
        <h2>{letter}</h2>
        <div class="entries-grid">
'''
        for idx, entry in enumerate(entries_by_letter[letter]):
            emoji = get_emoji(entry['title'])
            color_class = get_color_class(idx)
            html += f'''          <a href="/kids/encyclopedia/{entry['slug']}.html" class="entry-card {color_class}" data-title="{entry['title'].lower()}">
            <h3><span class="emoji">{emoji}</span> {entry['title']}</h3>
          </a>
'''
        html += '''        </div>
      </div>
'''

    html += '''    </div>

    <div class="no-results" id="noResults">
      <p>🤔 No entries found. Try a different search!</p>
    </div>
  </div>

  <script>
    // Search functionality
    const searchInput = document.getElementById('searchInput');
    const entryCards = document.querySelectorAll('.entry-card');
    const letterSections = document.querySelectorAll('.letter-section');
    const noResults = document.getElementById('noResults');

    searchInput.addEventListener('input', (e) => {
      const searchTerm = e.target.value.toLowerCase().trim();
      let visibleCount = 0;

      if (searchTerm === '') {
        entryCards.forEach(card => card.style.display = 'block');
        letterSections.forEach(section => section.style.display = 'block');
        noResults.classList.remove('show');
        return;
      }

      entryCards.forEach(card => {
        const title = card.getAttribute('data-title');
        if (title.includes(searchTerm)) {
          card.style.display = 'block';
          visibleCount++;
        } else {
          card.style.display = 'none';
        }
      });

      letterSections.forEach(section => {
        const visibleCards = section.querySelectorAll('.entry-card[style*="display: block"], .entry-card:not([style*="display: none"])');
        const hasVisible = Array.from(section.querySelectorAll('.entry-card')).some(card =>
          card.style.display !== 'none'
        );
        section.style.display = hasVisible ? 'block' : 'none';
      });

      if (visibleCount === 0) {
        noResults.classList.add('show');
      } else {
        noResults.classList.remove('show');
      }
    });

    // Smooth scroll for alphabet navigation
    document.querySelectorAll('.letter-btn').forEach(link => {
      link.addEventListener('click', (e) => {
        e.preventDefault();
        const targetId = link.getAttribute('href').substring(1);
        const target = document.getElementById(targetId);
        if (target) {
          const offset = 100;
          const elementPosition = target.getBoundingClientRect().top;
          const offsetPosition = elementPosition + window.pageYOffset - offset;
          window.scrollTo({ top: offsetPosition, behavior: 'smooth' });
        }
      });
    });
  </script>
</body>
</html>'''

    return html

def main():
    """Main function"""
    print("Generating kids encyclopedia pages...")

    # Load encyclopedia data
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)

    by_letter = data['by_letter']
    total_entries = data['total_entries']

    # Collect all entries from by_letter structure
    entries = []
    for letter_entries in by_letter.values():
        entries.extend(letter_entries)

    print(f"Found {total_entries} entries")

    # Create output directory
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Encyclopedia HTML files directory
    encyclopedia_dir = "/home/user/eldoaai/public/encyclopedia"

    # Generate individual entry pages
    print(f"\nGenerating individual pages...")
    for idx, entry in enumerate(entries, 1):
        if idx % 100 == 0:
            print(f"  Processed {idx}/{total_entries}")

        color_class = get_color_class(idx)
        html = create_kids_entry_page(entry, color_class, encyclopedia_dir)

        output_file = os.path.join(OUTPUT_DIR, f"{entry['slug']}.html")
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html)

    print(f"\nCreated {total_entries} individual entry pages")

    # Generate index page
    print("\nGenerating kids encyclopedia index page...")
    index_html = create_kids_index_page(by_letter, total_entries)
    with open(KIDS_INDEX_FILE, 'w', encoding='utf-8') as f:
        f.write(index_html)

    print(f"Created kids encyclopedia index at {KIDS_INDEX_FILE}")

    print("\n✅ Done! Kids encyclopedia is complete!")
    print(f"   - {total_entries} individual entry pages")
    print(f"   - 1 encyclopedia index page")
    print(f"   - Fun, kid-friendly design with emojis and colors")

if __name__ == "__main__":
    main()
