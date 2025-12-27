/**
 * ELDOA AI Cross-Linking Module
 * Adds dynamic internal links between encyclopedia, videos, practitioners, and research
 */

(function() {
  'use strict';

  const CrossLinks = {
    // Cache for loaded data
    cache: {
      videos: null,
      encyclopedia: null,
      practitioners: null
    },

    // Research mapping (static since there are only a few)
    research: [
      { id: 'athletic-performance', title: 'Athletic Performance & ELDOA', keywords: ['athletic', 'performance', 'sport', 'training', 'muscle'] },
      { id: 'breathing-foundation', title: 'Breathing Foundation', keywords: ['breathing', 'diaphragm', 'respiration', 'breath'] },
      { id: 'digital-posture-crisis', title: 'Digital Posture Crisis', keywords: ['posture', 'digital', 'desk', 'computer', 'neck', 'cervical'] },
      { id: 'neurological-mechanisms-eldoa', title: 'Neurological Mechanisms of ELDOA', keywords: ['neural', 'neurological', 'nerve', 'proprioception', 'nervous'] },
      { id: 'visceral-autonomic-effects', title: 'Visceral & Autonomic Effects', keywords: ['visceral', 'autonomic', 'organ', 'internal'] },
      { id: 'visual-performance-posture', title: 'Visual Performance & Posture', keywords: ['visual', 'eye', 'vision', 'vestibular'] }
    ],

    /**
     * Load data files
     */
    async loadData(type) {
      if (this.cache[type]) return this.cache[type];

      const paths = {
        videos: '/data/video-library.json',
        encyclopedia: '/data/encyclopedia-entries.json',
        practitioners: '/data/practitioners.json'
      };

      try {
        const response = await fetch(paths[type]);
        const data = await response.json();
        this.cache[type] = type === 'practitioners' ? data.practitioners : data;
        return this.cache[type];
      } catch (error) {
        console.warn(`Failed to load ${type} data:`, error);
        return [];
      }
    },

    /**
     * Find related videos for an encyclopedia entry
     */
    async findRelatedVideos(entry) {
      const videos = await this.loadData('videos');
      if (!videos || !videos.length) return [];

      const matches = [];
      const entrySegments = (entry.related_segments || []).map(s => s.toLowerCase());
      const entryTags = (entry.tags || []).map(t => t.toLowerCase());
      const entryRegion = (entry.region || '').toLowerCase();
      const entryTitle = (entry.title || '').toLowerCase();

      videos.forEach(video => {
        let score = 0;
        const videoSegments = (video.segments || []).map(s => s.toLowerCase());
        const videoTags = (video.tags || []).map(t => t.toLowerCase());
        const videoRegion = (video.region || '').toLowerCase();
        const videoAilments = (video.ailment || []).map(a => a.toLowerCase());

        // Check segment matches (highest priority)
        entrySegments.forEach(seg => {
          if (videoSegments.some(vs => vs.includes(seg) || seg.includes(vs))) {
            score += 10;
          }
        });

        // Check tag matches
        entryTags.forEach(tag => {
          if (videoTags.includes(tag)) score += 5;
        });

        // Check region overlap
        if (entryRegion && videoRegion && (
          entryRegion.includes(videoRegion) ||
          videoRegion.includes(entryRegion) ||
          this.regionsRelated(entryRegion, videoRegion)
        )) {
          score += 3;
        }

        // Check title/content matches
        videoAilments.forEach(ailment => {
          if (entryTitle.includes(ailment.split(' ')[0].toLowerCase())) score += 4;
        });

        if (score > 0) {
          matches.push({ ...video, score });
        }
      });

      // Sort by score and return top matches
      return matches
        .sort((a, b) => b.score - a.score)
        .slice(0, 4);
    },

    /**
     * Find related encyclopedia entries for a video
     */
    async findRelatedEncyclopedia(video) {
      const entries = await this.loadData('encyclopedia');
      if (!entries || !entries.length) return [];

      const matches = [];
      const videoSegments = (video.segments || []).map(s => s.toLowerCase());
      const videoTags = (video.tags || []).map(t => t.toLowerCase());
      const videoAilments = (video.ailment || []).map(a => a.toLowerCase());
      const videoRegion = (video.region || '').toLowerCase();

      entries.forEach(entry => {
        let score = 0;
        const entrySegments = (entry.related_segments || []).map(s => s.toLowerCase());
        const entryTags = (entry.tags || []).map(t => t.toLowerCase());
        const entryRegion = (entry.region || '').toLowerCase();
        const entryTitle = (entry.title || '').toLowerCase();

        // Check segment matches
        videoSegments.forEach(seg => {
          if (entrySegments.some(es => es.includes(seg) || seg.includes(es))) {
            score += 10;
          }
        });

        // Check tag matches
        videoTags.forEach(tag => {
          if (entryTags.includes(tag)) score += 5;
        });

        // Check region overlap
        if (videoRegion && entryRegion && this.regionsRelated(videoRegion, entryRegion)) {
          score += 3;
        }

        // Check ailment in title
        videoAilments.forEach(ailment => {
          const ailmentWords = ailment.toLowerCase().split(' ');
          if (ailmentWords.some(word => word.length > 3 && entryTitle.includes(word))) {
            score += 4;
          }
        });

        if (score > 0) {
          matches.push({ ...entry, score });
        }
      });

      return matches
        .sort((a, b) => b.score - a.score)
        .slice(0, 5);
    },

    /**
     * Find practitioners by region/specialization
     */
    async findPractitioners(options = {}) {
      const practitioners = await this.loadData('practitioners');
      if (!practitioners || !practitioners.length) return [];

      let filtered = practitioners.filter(p => p.status !== 'deceased' && p.status !== 'closed');

      // Filter by country if specified
      if (options.countries && options.countries.length) {
        filtered = filtered.filter(p => options.countries.includes(p.country));
      }

      // Filter by level (prefer higher levels)
      filtered = filtered.sort((a, b) => (b.level || 0) - (a.level || 0));

      return filtered.slice(0, 3);
    },

    /**
     * Find related research articles
     */
    findRelatedResearch(content) {
      const contentLower = (content.title + ' ' + (content.tags || []).join(' ')).toLowerCase();

      return this.research
        .filter(r => r.keywords.some(kw => contentLower.includes(kw)))
        .slice(0, 2);
    },

    /**
     * Check if two regions are related
     */
    regionsRelated(region1, region2) {
      const lumbar = ['lumbar', 'lumbosacral', 'lower back', 'l5-s1', 'l4-l5'];
      const thoracic = ['thoracic', 'mid back', 't8-t9', 't12-l1'];
      const cervical = ['cervical', 'neck', 'c-spine'];
      const wholeBody = ['whole body', 'general', 'spine'];

      const inSameGroup = (r, group) => group.some(g => r.includes(g));

      if (inSameGroup(region1, wholeBody) || inSameGroup(region2, wholeBody)) return true;
      if (inSameGroup(region1, lumbar) && inSameGroup(region2, lumbar)) return true;
      if (inSameGroup(region1, thoracic) && inSameGroup(region2, thoracic)) return true;
      if (inSameGroup(region1, cervical) && inSameGroup(region2, cervical)) return true;

      return false;
    },

    /**
     * Render related videos section
     */
    renderRelatedVideos(videos, containerId) {
      const container = document.getElementById(containerId);
      if (!container || !videos.length) return;

      const html = `
        <h2 class="eldoa-h2" style="display:flex;align-items:center;gap:8px;">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <polygon points="5,3 19,12 5,21"/>
          </svg>
          Related Videos
        </h2>
        <div class="cross-link-grid" style="display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:16px;margin-top:16px;">
          ${videos.map(v => `
            <a href="/videos/pages/${v.id}.html" class="cross-link-card" style="display:block;padding:16px;background:var(--eldoa-surface,#f9f9f9);border:1px solid var(--eldoa-border-color,#e0e0e0);border-radius:8px;text-decoration:none;transition:transform 0.2s,box-shadow 0.2s;">
              <div style="font-weight:600;color:var(--eldoa-text-primary,#333);margin-bottom:8px;line-height:1.3;">${v.title}</div>
              <div style="font-size:0.85rem;color:var(--eldoa-text-secondary,#666);">
                ${v.instructor ? `<span>${v.instructor}</span>` : ''}
                ${v.duration ? `<span style="margin-left:8px;">${v.duration}</span>` : ''}
              </div>
              ${v.segments && v.segments.length ? `
                <div style="margin-top:8px;display:flex;flex-wrap:wrap;gap:4px;">
                  ${v.segments.slice(0, 3).map(s => `<span style="font-size:0.75rem;padding:2px 8px;background:var(--eldoa-primary-color,#3498db);color:#fff;border-radius:12px;">${s}</span>`).join('')}
                </div>
              ` : ''}
            </a>
          `).join('')}
        </div>
        <div style="margin-top:16px;text-align:center;">
          <a href="/videos/" style="display:inline-block;padding:10px 20px;background:var(--eldoa-primary-color,#3498db);color:#fff;border-radius:6px;text-decoration:none;font-weight:500;">Browse All Videos</a>
        </div>
      `;

      container.innerHTML = html;
      container.style.display = 'block';
    },

    /**
     * Render related encyclopedia section
     */
    renderRelatedEncyclopedia(entries, containerId) {
      const container = document.getElementById(containerId);
      if (!container || !entries.length) return;

      const html = `
        <h3 style="font-size:1.1rem;font-weight:700;margin-bottom:16px;display:flex;align-items:center;gap:8px;">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/>
            <path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/>
          </svg>
          Learn More in the Encyclopedia
        </h3>
        <ul style="list-style:none;padding:0;margin:0;">
          ${entries.map(e => `
            <li style="margin:8px 0;padding:8px 0;border-bottom:1px solid var(--border-color,#ddd);">
              <a href="/library/${e.id}.html" style="color:var(--accent-color,#3498db);text-decoration:none;font-weight:500;">${e.title}</a>
              ${e.category ? `<span style="margin-left:8px;font-size:0.8rem;color:#888;">(${e.category})</span>` : ''}
            </li>
          `).join('')}
        </ul>
        <div style="margin-top:16px;">
          <a href="/encyclopedia.html" style="color:var(--accent-color,#3498db);text-decoration:none;font-weight:500;">Browse Encyclopedia →</a>
        </div>
      `;

      container.innerHTML = html;
      container.style.display = 'block';
    },

    /**
     * Render practitioners section
     */
    renderPractitioners(practitioners, containerId) {
      const container = document.getElementById(containerId);
      if (!container || !practitioners.length) return;

      const html = `
        <h2 class="eldoa-h2" style="display:flex;align-items:center;gap:8px;">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/>
            <circle cx="9" cy="7" r="4"/>
            <path d="M23 21v-2a4 4 0 0 0-3-3.87"/>
            <path d="M16 3.13a4 4 0 0 1 0 7.75"/>
          </svg>
          Find a Certified Practitioner
        </h2>
        <div class="cross-link-grid" style="display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:16px;margin-top:16px;">
          ${practitioners.map(p => `
            <a href="/practitioner.html?id=${p.id}" class="cross-link-card" style="display:block;padding:16px;background:var(--eldoa-surface,#f9f9f9);border:1px solid var(--eldoa-border-color,#e0e0e0);border-radius:8px;text-decoration:none;">
              <div style="font-weight:600;color:var(--eldoa-text-primary,#333);margin-bottom:4px;">${p.name}</div>
              ${p.level ? `<div style="display:inline-block;font-size:0.75rem;padding:2px 8px;background:linear-gradient(135deg,#6366f1,#8b5cf6);color:#fff;border-radius:4px;margin-bottom:8px;">Level ${p.level}</div>` : ''}
              <div style="font-size:0.85rem;color:var(--eldoa-text-secondary,#666);">
                ${[p.city, p.state || p.region, p.country].filter(Boolean).join(', ')}
              </div>
            </a>
          `).join('')}
        </div>
        <div style="margin-top:16px;text-align:center;">
          <a href="/practitioners.html" style="display:inline-block;padding:10px 20px;background:var(--eldoa-accent-color,#4caf50);color:#fff;border-radius:6px;text-decoration:none;font-weight:500;">Find All Practitioners</a>
        </div>
      `;

      container.innerHTML = html;
      container.style.display = 'block';
    },

    /**
     * Render related research section
     */
    renderRelatedResearch(research, containerId) {
      const container = document.getElementById(containerId);
      if (!container || !research.length) return;

      const html = `
        <h2 class="eldoa-h2" style="display:flex;align-items:center;gap:8px;">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
            <polyline points="14,2 14,8 20,8"/>
            <line x1="16" y1="13" x2="8" y2="13"/>
            <line x1="16" y1="17" x2="8" y2="17"/>
          </svg>
          Related Research
        </h2>
        <ul style="list-style:none;padding:0;margin:16px 0;">
          ${research.map(r => `
            <li style="margin:12px 0;">
              <a href="/research/${r.id}/" style="color:var(--eldoa-info-color,#007acc);text-decoration:none;font-weight:500;display:flex;align-items:center;gap:8px;">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/>
                  <polyline points="15,3 21,3 21,9"/>
                  <line x1="10" y1="14" x2="21" y2="3"/>
                </svg>
                ${r.title}
              </a>
            </li>
          `).join('')}
        </ul>
        <div style="margin-top:8px;">
          <a href="/research/" style="color:var(--eldoa-info-color,#007acc);text-decoration:none;font-weight:500;">View All Research →</a>
        </div>
      `;

      container.innerHTML = html;
      container.style.display = 'block';
    },

    /**
     * Initialize for encyclopedia page
     */
    async initForEncyclopedia(entryId) {
      const entries = await this.loadData('encyclopedia');
      const entry = entries.find(e => e.id === entryId);
      if (!entry) return;

      // Find and render related videos
      const videos = await this.findRelatedVideos(entry);
      this.renderRelatedVideos(videos, 'eldoa-related-videos');

      // Find and render practitioners
      const practitioners = await this.findPractitioners({ limit: 3 });
      this.renderPractitioners(practitioners, 'eldoa-find-practitioner');

      // Find and render research
      const research = this.findRelatedResearch(entry);
      this.renderRelatedResearch(research, 'eldoa-related-research');
    },

    /**
     * Initialize for video page
     */
    async initForVideo(videoId) {
      const videos = await this.loadData('videos');
      const video = videos.find(v => v.id === videoId);
      if (!video) return;

      // Find and render related encyclopedia entries
      const entries = await this.findRelatedEncyclopedia(video);
      this.renderRelatedEncyclopedia(entries, 'eldoa-related-encyclopedia');

      // Find and render practitioners
      const practitioners = await this.findPractitioners({ limit: 3 });
      this.renderPractitioners(practitioners, 'eldoa-find-practitioner');
    },

    /**
     * Initialize for practitioner page
     */
    async initForPractitioner(practitionerName) {
      // Find videos by this instructor
      const videos = await this.loadData('videos');
      const instructorVideos = videos.filter(v =>
        v.instructor && v.instructor.toLowerCase().includes(practitionerName.toLowerCase())
      );

      if (instructorVideos.length > 0) {
        this.renderRelatedVideos(instructorVideos.slice(0, 4), 'eldoa-practitioner-videos');
      }
    },

    /**
     * Find similar videos
     */
    async findSimilarVideos(video) {
      const videos = await this.loadData('videos');
      if (!videos || !videos.length) return [];

      const matches = [];
      const videoSegments = (video.segments || []).map(s => s.toLowerCase());
      const videoTags = (video.tags || []).map(t => t.toLowerCase());
      const videoRegion = (video.region || '').toLowerCase();
      const videoDifficulty = (video.difficulty || '').toLowerCase();

      videos.forEach(v => {
        if (v.id === video.id) return; // Skip same video

        let score = 0;
        const vSegments = (v.segments || []).map(s => s.toLowerCase());
        const vTags = (v.tags || []).map(t => t.toLowerCase());
        const vRegion = (v.region || '').toLowerCase();
        const vDifficulty = (v.difficulty || '').toLowerCase();

        // Segment matches (high priority)
        videoSegments.forEach(seg => {
          if (vSegments.includes(seg)) score += 10;
        });

        // Same region
        if (videoRegion === vRegion) score += 5;

        // Same difficulty
        if (videoDifficulty === vDifficulty) score += 3;

        // Tag matches
        videoTags.forEach(tag => {
          if (vTags.includes(tag)) score += 2;
        });

        if (score > 0) {
          matches.push({ ...v, score });
        }
      });

      return matches
        .sort((a, b) => b.score - a.score)
        .slice(0, 4);
    },

    /**
     * Render similar videos section
     */
    renderSimilarVideos(videos, containerId) {
      const container = document.getElementById(containerId);
      if (!container || !videos.length) return;

      const html = `
        <h3 style="font-size:1.1rem;font-weight:700;margin-bottom:16px;display:flex;align-items:center;gap:8px;">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <rect x="2" y="2" width="20" height="20" rx="2.18" ry="2.18"/>
            <line x1="7" y1="2" x2="7" y2="22"/>
            <line x1="17" y1="2" x2="17" y2="22"/>
            <line x1="2" y1="12" x2="22" y2="12"/>
            <line x1="2" y1="7" x2="7" y2="7"/>
            <line x1="2" y1="17" x2="7" y2="17"/>
            <line x1="17" y1="17" x2="22" y2="17"/>
            <line x1="17" y1="7" x2="22" y2="7"/>
          </svg>
          Similar Videos
        </h3>
        <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:12px;">
          ${videos.map(v => `
            <a href="/videos/pages/${v.id}.html" style="display:block;padding:12px;background:var(--card-bg,#f8f9fa);border:1px solid var(--border-color,#ddd);border-radius:6px;text-decoration:none;">
              <div style="font-weight:600;color:var(--text-color,#333);font-size:0.9rem;margin-bottom:4px;line-height:1.3;">${v.title}</div>
              <div style="font-size:0.8rem;color:#888;">
                ${v.difficulty || ''} ${v.duration ? '• ' + v.duration : ''}
              </div>
            </a>
          `).join('')}
        </div>
      `;

      container.innerHTML = html;
      container.style.display = 'block';
    },

    /**
     * Find videos related to research topic
     */
    async findVideosForResearch(researchId) {
      const videos = await this.loadData('videos');
      if (!videos || !videos.length) return [];

      // Keywords for each research article
      const researchKeywords = {
        'athletic-performance': ['performance', 'sport', 'athletic', 'training', 'l5-s1', 'l4-l5'],
        'breathing-foundation': ['breathing', 'diaphragm', 't8-t9', 't7-t8'],
        'digital-posture-crisis': ['posture', 'neck', 'cervical', 'c6-c7', 'c5-c6', 'c4-c5'],
        'neurological-mechanisms-eldoa': ['neural', 'nervous', 'general', 'spinal'],
        'visceral-autonomic-effects': ['visceral', 't12-l1', 't8-t9', 'thoracic'],
        'visual-performance-posture': ['posture', 'cervical', 'neck', 'c-spine']
      };

      const keywords = researchKeywords[researchId] || [];
      const matches = [];

      videos.forEach(v => {
        let score = 0;
        const vTags = (v.tags || []).map(t => t.toLowerCase());
        const vSegments = (v.segments || []).map(s => s.toLowerCase());
        const vTitle = v.title.toLowerCase();

        keywords.forEach(kw => {
          if (vTags.some(t => t.includes(kw))) score += 5;
          if (vSegments.some(s => s.includes(kw))) score += 8;
          if (vTitle.includes(kw)) score += 3;
        });

        if (score > 0) {
          matches.push({ ...v, score });
        }
      });

      return matches
        .sort((a, b) => b.score - a.score)
        .slice(0, 4);
    },

    /**
     * Initialize for research page
     */
    async initForResearch(researchId) {
      // Find and render related videos
      const videos = await this.findVideosForResearch(researchId);
      this.renderRelatedVideos(videos, 'eldoa-related-videos');

      // Find and render practitioners
      const practitioners = await this.findPractitioners({ limit: 3 });
      this.renderPractitioners(practitioners, 'eldoa-find-practitioner');
    },

    /**
     * Enhanced video page initialization with similar videos
     */
    async initForVideoEnhanced(videoId) {
      const videos = await this.loadData('videos');
      const video = videos.find(v => v.id === videoId);
      if (!video) return;

      // Find and render related encyclopedia entries
      const entries = await this.findRelatedEncyclopedia(video);
      this.renderRelatedEncyclopedia(entries, 'eldoa-related-encyclopedia');

      // Find and render similar videos
      const similar = await this.findSimilarVideos(video);
      this.renderSimilarVideos(similar, 'eldoa-similar-videos');

      // Find and render practitioners
      const practitioners = await this.findPractitioners({ limit: 3 });
      this.renderPractitioners(practitioners, 'eldoa-find-practitioner');
    }
  };

  // Expose globally
  window.ELDOACrossLinks = CrossLinks;
})();
