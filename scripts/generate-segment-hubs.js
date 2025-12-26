#!/usr/bin/env node
/**
 * Generate segment hub pages that link all content related to each spinal segment
 */

const fs = require('fs');
const path = require('path');

// Define segments and their metadata
const segments = [
  { id: 'c4-c5', name: 'C4-C5', region: 'Cervical', description: 'Upper neck segment affecting shoulder and arm function' },
  { id: 'c5-c6', name: 'C5-C6', region: 'Cervical', description: 'Mid-cervical segment involved in bicep strength and wrist extension' },
  { id: 'c6-c7', name: 'C6-C7', region: 'Cervical', description: 'Lower cervical segment affecting tricep and grip strength' },
  { id: 'c7-t1', name: 'C7-T1', region: 'Cervicothoracic Junction', description: 'Cervicothoracic junction, critical transition zone' },
  { id: 't4-t5', name: 'T4-T5', region: 'Upper Thoracic', description: 'Upper thoracic segment affecting upper back and chest' },
  { id: 't7-t8', name: 'T7-T8', region: 'Mid Thoracic', description: 'Mid-thoracic segment associated with core stability' },
  { id: 't8-t9', name: 'T8-T9', region: 'Mid Thoracic', description: 'Mid-thoracic segment important for posture and breathing' },
  { id: 't12-l1', name: 'T12-L1', region: 'Thoracolumbar Junction', description: 'Thoracolumbar junction, high stress transition zone' },
  { id: 'l1-l2', name: 'L1-L2', region: 'Upper Lumbar', description: 'Upper lumbar segment affecting hip flexion' },
  { id: 'l2-l3', name: 'L2-L3', region: 'Lumbar', description: 'Lumbar segment involved in hip and thigh function' },
  { id: 'l3-l4', name: 'L3-L4', region: 'Lumbar', description: 'Lumbar segment affecting quadriceps and knee extension' },
  { id: 'l4-l5', name: 'L4-L5', region: 'Lower Lumbar', description: 'Lower lumbar segment, common site of disc issues' },
  { id: 'l5-s1', name: 'L5-S1', region: 'Lumbosacral Junction', description: 'Lumbosacral junction, bearing most spinal load' },
  { id: 's1-s2', name: 'S1-S2', region: 'Sacral', description: 'Upper sacral segment affecting calf and foot function' }
];

// Load data files
const videosPath = path.join(__dirname, '..', 'data', 'video-library.json');
const encyclopediaPath = path.join(__dirname, '..', 'data', 'encyclopedia-entries.json');

let videos = [];
let encyclopedia = [];

try {
  videos = JSON.parse(fs.readFileSync(videosPath, 'utf8'));
} catch (e) {
  console.warn('Could not load videos:', e.message);
}

try {
  encyclopedia = JSON.parse(fs.readFileSync(encyclopediaPath, 'utf8'));
} catch (e) {
  console.warn('Could not load encyclopedia:', e.message);
}

function findRelatedVideos(segmentId) {
  const segmentLower = segmentId.toLowerCase();
  return videos.filter(v => {
    const vSegments = (v.segments || []).map(s => s.toLowerCase());
    const vTags = (v.tags || []).map(t => t.toLowerCase());
    return vSegments.some(s => s.includes(segmentLower) || segmentLower.includes(s)) ||
           vTags.some(t => t.includes(segmentLower));
  });
}

function findRelatedEncyclopedia(segmentId) {
  const segmentLower = segmentId.toLowerCase();
  return encyclopedia.filter(e => {
    const eSegments = (e.related_segments || []).map(s => s.toLowerCase());
    const eTags = (e.tags || []).map(t => t.toLowerCase());
    const eTitle = e.title.toLowerCase();
    return eSegments.some(s => s.includes(segmentLower) || segmentLower.includes(s)) ||
           eTags.some(t => t.includes(segmentLower)) ||
           eTitle.includes(segmentLower);
  });
}

function generateHubPage(segment) {
  const relatedVideos = findRelatedVideos(segment.id);
  const relatedEncyclopedia = findRelatedEncyclopedia(segment.id);

  const html = `<!DOCTYPE html>
<html lang="en" data-theme="light">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>${segment.name} Segment Hub - ELDOA AI</title>
  <meta name="description" content="All ELDOA content for the ${segment.name} segment: videos, exercises, and encyclopedia entries for ${segment.description.toLowerCase()}.">
  <meta name="keywords" content="ELDOA ${segment.name}, ${segment.region}, spinal segment, ${segment.id} exercises">
  <link rel="canonical" href="https://eldoa.ai/segments/${segment.id}.html">

  <meta property="og:type" content="website">
  <meta property="og:title" content="${segment.name} Segment Hub - ELDOA AI">
  <meta property="og:description" content="Complete guide to ELDOA exercises and resources for the ${segment.name} spinal segment.">
  <meta property="og:url" content="https://eldoa.ai/segments/${segment.id}.html">

  <link rel="icon" type="image/png" href="/favicon.png">
  <meta name="theme-color" content="#2f2fe6">

  <style>
    :root {
      --bg: #ffffff;
      --fg: #0d0f13;
      --muted: #64748b;
      --brand: #2f2fe6;
      --brand-light: #eef2ff;
      --card: #f8fafc;
      --border: #e2e8f0;
    }
    [data-theme="dark"] {
      --bg: #0b0d12;
      --fg: #eef2ff;
      --muted: #94a3b8;
      --brand: #818cf8;
      --brand-light: #1e1b4b;
      --card: #111827;
      --border: #1f2937;
    }
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      background: var(--bg);
      color: var(--fg);
      line-height: 1.6;
    }
    .container { max-width: 1000px; margin: 0 auto; padding: 2rem; }
    header { text-align: center; margin-bottom: 3rem; }
    .breadcrumb {
      font-size: 0.9rem;
      color: var(--muted);
      margin-bottom: 1.5rem;
    }
    .breadcrumb a { color: var(--brand); text-decoration: none; }
    .breadcrumb a:hover { text-decoration: underline; }
    h1 {
      font-size: 2.5rem;
      font-weight: 800;
      margin-bottom: 0.5rem;
      background: linear-gradient(135deg, var(--brand), #6366f1);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      background-clip: text;
    }
    .region-badge {
      display: inline-block;
      padding: 0.25rem 0.75rem;
      background: var(--brand-light);
      color: var(--brand);
      border-radius: 20px;
      font-size: 0.85rem;
      font-weight: 600;
      margin-bottom: 1rem;
    }
    .description {
      color: var(--muted);
      font-size: 1.1rem;
      max-width: 600px;
      margin: 0 auto;
    }
    .stats {
      display: flex;
      justify-content: center;
      gap: 2rem;
      margin: 2rem 0;
      padding: 1rem;
      background: var(--card);
      border-radius: 12px;
      border: 1px solid var(--border);
    }
    .stat { text-align: center; }
    .stat-number { font-size: 2rem; font-weight: 700; color: var(--brand); }
    .stat-label { font-size: 0.85rem; color: var(--muted); }

    section { margin-bottom: 3rem; }
    h2 {
      font-size: 1.5rem;
      font-weight: 700;
      margin-bottom: 1.5rem;
      padding-bottom: 0.5rem;
      border-bottom: 2px solid var(--border);
    }
    .grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
      gap: 1rem;
    }
    .card {
      display: block;
      padding: 1.25rem;
      background: var(--card);
      border: 1px solid var(--border);
      border-radius: 12px;
      text-decoration: none;
      transition: transform 0.2s, box-shadow 0.2s;
    }
    .card:hover {
      transform: translateY(-2px);
      box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    .card-title {
      font-weight: 600;
      color: var(--fg);
      margin-bottom: 0.5rem;
      line-height: 1.3;
    }
    .card-meta {
      font-size: 0.85rem;
      color: var(--muted);
    }
    .card-tags {
      display: flex;
      flex-wrap: wrap;
      gap: 0.5rem;
      margin-top: 0.75rem;
    }
    .tag {
      font-size: 0.75rem;
      padding: 0.2rem 0.5rem;
      background: var(--brand);
      color: #fff;
      border-radius: 12px;
    }
    .empty-state {
      text-align: center;
      padding: 2rem;
      color: var(--muted);
      background: var(--card);
      border-radius: 12px;
      border: 1px dashed var(--border);
    }
    .cta-section {
      text-align: center;
      padding: 2rem;
      background: linear-gradient(135deg, var(--brand-light), var(--card));
      border-radius: 12px;
      margin-top: 2rem;
    }
    .cta-title { font-size: 1.25rem; font-weight: 600; margin-bottom: 0.5rem; }
    .cta-text { color: var(--muted); margin-bottom: 1rem; }
    .cta-button {
      display: inline-block;
      padding: 0.75rem 1.5rem;
      background: var(--brand);
      color: #fff;
      text-decoration: none;
      border-radius: 8px;
      font-weight: 600;
    }
    .cta-button:hover { opacity: 0.9; }
    footer {
      margin-top: 3rem;
      padding-top: 2rem;
      border-top: 1px solid var(--border);
      text-align: center;
      color: var(--muted);
      font-size: 0.9rem;
    }
    footer a { color: var(--brand); text-decoration: none; }
    footer a:hover { text-decoration: underline; }
    .nav-segments {
      display: flex;
      flex-wrap: wrap;
      gap: 0.5rem;
      justify-content: center;
      margin-top: 1rem;
    }
    .nav-segment {
      padding: 0.25rem 0.75rem;
      background: var(--card);
      border: 1px solid var(--border);
      border-radius: 6px;
      color: var(--fg);
      text-decoration: none;
      font-size: 0.85rem;
    }
    .nav-segment:hover { background: var(--brand-light); border-color: var(--brand); }
    .nav-segment.active { background: var(--brand); color: #fff; border-color: var(--brand); }
  </style>
</head>
<body>
  <div class="container">
    <header>
      <nav class="breadcrumb">
        <a href="/">Home</a> → <a href="/segments/">Segments</a> → ${segment.name}
      </nav>
      <h1>${segment.name}</h1>
      <span class="region-badge">${segment.region}</span>
      <p class="description">${segment.description}</p>

      <div class="stats">
        <div class="stat">
          <div class="stat-number">${relatedVideos.length}</div>
          <div class="stat-label">Videos</div>
        </div>
        <div class="stat">
          <div class="stat-number">${relatedEncyclopedia.length}</div>
          <div class="stat-label">Encyclopedia Entries</div>
        </div>
      </div>
    </header>

    <section>
      <h2>Videos for ${segment.name}</h2>
      ${relatedVideos.length > 0 ? `
      <div class="grid">
        ${relatedVideos.slice(0, 8).map(v => `
        <a href="/videos/pages/${v.id}.html" class="card">
          <div class="card-title">${v.title}</div>
          <div class="card-meta">
            ${v.instructor || ''} ${v.duration ? '• ' + v.duration : ''} ${v.difficulty ? '• ' + v.difficulty : ''}
          </div>
          ${v.segments && v.segments.length ? `
          <div class="card-tags">
            ${v.segments.slice(0, 3).map(s => `<span class="tag">${s}</span>`).join('')}
          </div>
          ` : ''}
        </a>
        `).join('')}
      </div>
      ${relatedVideos.length > 8 ? `
      <div style="text-align:center;margin-top:1rem;">
        <a href="/videos/?segment=${segment.id}" class="cta-button" style="background:transparent;color:var(--brand);border:1px solid var(--brand);">View All ${relatedVideos.length} Videos</a>
      </div>
      ` : ''}
      ` : `
      <div class="empty-state">
        <p>No specific videos yet for ${segment.name}. Check out our <a href="/videos/">full video library</a>.</p>
      </div>
      `}
    </section>

    <section>
      <h2>Encyclopedia Entries</h2>
      ${relatedEncyclopedia.length > 0 ? `
      <div class="grid">
        ${relatedEncyclopedia.slice(0, 6).map(e => `
        <a href="/encyclopedia/${e.id}.html" class="card">
          <div class="card-title">${e.title}</div>
          <div class="card-meta">${e.category || 'Encyclopedia'}</div>
        </a>
        `).join('')}
      </div>
      ${relatedEncyclopedia.length > 6 ? `
      <div style="text-align:center;margin-top:1rem;">
        <a href="/encyclopedia.html?segment=${segment.id}" class="cta-button" style="background:transparent;color:var(--brand);border:1px solid var(--brand);">View All ${relatedEncyclopedia.length} Entries</a>
      </div>
      ` : ''}
      ` : `
      <div class="empty-state">
        <p>No specific encyclopedia entries yet for ${segment.name}. Explore our <a href="/encyclopedia.html">full encyclopedia</a>.</p>
      </div>
      `}
    </section>

    <div class="cta-section">
      <div class="cta-title">Need Help with ${segment.name}?</div>
      <p class="cta-text">Find a certified ELDOA practitioner who specializes in ${segment.region.toLowerCase()} issues.</p>
      <a href="/practitioners.html" class="cta-button">Find a Practitioner</a>
    </div>

    <footer>
      <p>Browse Other Segments:</p>
      <div class="nav-segments">
        ${segments.map(s => `
        <a href="/segments/${s.id}.html" class="nav-segment${s.id === segment.id ? ' active' : ''}">${s.name}</a>
        `).join('')}
      </div>
      <p style="margin-top:2rem;">
        <a href="/">Home</a> • <a href="/videos/">Videos</a> • <a href="/encyclopedia.html">Encyclopedia</a> • <a href="/practitioners.html">Practitioners</a>
      </p>
    </footer>
  </div>

  <script>
    if (window.matchMedia('(prefers-color-scheme: dark)').matches) {
      document.documentElement.setAttribute('data-theme', 'dark');
    }
  </script>
</body>
</html>`;

  return html;
}

function generateIndexPage() {
  const html = `<!DOCTYPE html>
<html lang="en" data-theme="light">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Spinal Segments Hub - ELDOA AI</title>
  <meta name="description" content="Browse ELDOA content organized by spinal segment. Find videos, exercises, and encyclopedia entries for each vertebral level from cervical to sacral.">
  <link rel="canonical" href="https://eldoa.ai/segments/">
  <link rel="icon" type="image/png" href="/favicon.png">
  <meta name="theme-color" content="#2f2fe6">

  <style>
    :root {
      --bg: #ffffff;
      --fg: #0d0f13;
      --muted: #64748b;
      --brand: #2f2fe6;
      --brand-light: #eef2ff;
      --card: #f8fafc;
      --border: #e2e8f0;
    }
    [data-theme="dark"] {
      --bg: #0b0d12;
      --fg: #eef2ff;
      --muted: #94a3b8;
      --brand: #818cf8;
      --brand-light: #1e1b4b;
      --card: #111827;
      --border: #1f2937;
    }
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      background: var(--bg);
      color: var(--fg);
      line-height: 1.6;
    }
    .container { max-width: 1000px; margin: 0 auto; padding: 2rem; }
    header { text-align: center; margin-bottom: 3rem; }
    .breadcrumb { font-size: 0.9rem; color: var(--muted); margin-bottom: 1.5rem; }
    .breadcrumb a { color: var(--brand); text-decoration: none; }
    h1 {
      font-size: 2.5rem;
      font-weight: 800;
      margin-bottom: 0.5rem;
    }
    .subtitle { color: var(--muted); font-size: 1.1rem; }

    .region-section { margin-bottom: 2.5rem; }
    .region-title {
      font-size: 1.25rem;
      font-weight: 700;
      margin-bottom: 1rem;
      color: var(--brand);
    }
    .segment-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
      gap: 1rem;
    }
    .segment-card {
      display: block;
      padding: 1.25rem;
      background: var(--card);
      border: 1px solid var(--border);
      border-radius: 12px;
      text-decoration: none;
      transition: transform 0.2s, box-shadow 0.2s, border-color 0.2s;
    }
    .segment-card:hover {
      transform: translateY(-2px);
      box-shadow: 0 4px 12px rgba(0,0,0,0.1);
      border-color: var(--brand);
    }
    .segment-name {
      font-size: 1.25rem;
      font-weight: 700;
      color: var(--fg);
      margin-bottom: 0.25rem;
    }
    .segment-desc {
      font-size: 0.85rem;
      color: var(--muted);
      line-height: 1.4;
    }
    footer {
      margin-top: 3rem;
      padding-top: 2rem;
      border-top: 1px solid var(--border);
      text-align: center;
      color: var(--muted);
    }
    footer a { color: var(--brand); text-decoration: none; }
  </style>
</head>
<body>
  <div class="container">
    <header>
      <nav class="breadcrumb">
        <a href="/">Home</a> → Segments
      </nav>
      <h1>Spinal Segments Hub</h1>
      <p class="subtitle">Browse ELDOA content organized by vertebral level</p>
    </header>

    ${['Cervical', 'Thoracic', 'Lumbar', 'Sacral'].map(region => {
      const regionSegments = segments.filter(s =>
        s.region.includes(region) ||
        (region === 'Thoracic' && s.region.includes('Thoraco')) ||
        (region === 'Lumbar' && s.region.includes('Lumbo'))
      );
      if (regionSegments.length === 0) return '';
      return `
    <section class="region-section">
      <h2 class="region-title">${region} Spine</h2>
      <div class="segment-grid">
        ${regionSegments.map(s => `
        <a href="/segments/${s.id}.html" class="segment-card">
          <div class="segment-name">${s.name}</div>
          <div class="segment-desc">${s.description}</div>
        </a>
        `).join('')}
      </div>
    </section>
    `;
    }).join('')}

    <footer>
      <p>
        <a href="/">Home</a> • <a href="/videos/">Videos</a> • <a href="/encyclopedia.html">Encyclopedia</a> • <a href="/practitioners.html">Practitioners</a>
      </p>
    </footer>
  </div>

  <script>
    if (window.matchMedia('(prefers-color-scheme: dark)').matches) {
      document.documentElement.setAttribute('data-theme', 'dark');
    }
  </script>
</body>
</html>`;

  return html;
}

// Generate pages
const segmentsDir = path.join(__dirname, '..', 'segments');
if (!fs.existsSync(segmentsDir)) {
  fs.mkdirSync(segmentsDir, { recursive: true });
}

console.log('Generating segment hub pages...\n');

// Generate index
fs.writeFileSync(path.join(segmentsDir, 'index.html'), generateIndexPage());
console.log('Created: segments/index.html');

// Generate individual segment pages
for (const segment of segments) {
  const html = generateHubPage(segment);
  fs.writeFileSync(path.join(segmentsDir, `${segment.id}.html`), html);
  console.log(`Created: segments/${segment.id}.html`);
}

console.log(`\nDone! Created ${segments.length + 1} segment hub pages.`);
