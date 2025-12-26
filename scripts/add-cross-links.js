#!/usr/bin/env node
/**
 * Script to add cross-linking sections to all encyclopedia and video pages
 */

const fs = require('fs');
const path = require('path');

const libraryDir = path.join(__dirname, '..', 'library');
const videoPagesDir = path.join(__dirname, '..', 'videos', 'pages');

// Cross-link sections to add to encyclopedia pages
const encyclopediaSections = `
      <!-- Related Videos (Dynamic) -->
      <section id="eldoa-related-videos" class="eldoa-related eldoa-section" data-section="videos" style="display:none;"></section>

      <!-- Related Research (Dynamic) -->
      <section id="eldoa-related-research" class="eldoa-related eldoa-section" data-section="research" style="display:none;"></section>

      <!-- Find a Practitioner (Dynamic) -->
      <section id="eldoa-find-practitioner" class="eldoa-related eldoa-section" data-section="practitioners" style="display:none;"></section>`;

const encyclopediaScript = `
  <!-- Cross-Linking Module -->
  <script src="/assets/js/cross-links.js"></script>
  <script>
    document.addEventListener('DOMContentLoaded', function() {
      const entryId = document.body.dataset.entryId;
      if (entryId && window.ELDOACrossLinks) {
        window.ELDOACrossLinks.initForEncyclopedia(entryId);
      }
    });
  </script>`;

// Cross-link sections to add to video pages
const videoSections = `
        <!-- Related Encyclopedia (Dynamic) -->
        <div id="eldoa-related-encyclopedia" class="description" style="display:none;"></div>

        <!-- Find a Practitioner (Dynamic) -->
        <div id="eldoa-find-practitioner" class="description" style="display:none;"></div>`;

const videoScript = `
    <!-- Cross-Linking Module -->
    <script src="/assets/js/cross-links.js"></script>
    <script>
        document.addEventListener('DOMContentLoaded', function() {
            const videoId = document.body.dataset.videoId;
            if (videoId && window.ELDOACrossLinks) {
                window.ELDOACrossLinks.initForVideo(videoId);
            }
        });
    </script>`;

function updateEncyclopediaPage(filePath) {
    let content = fs.readFileSync(filePath, 'utf8');

    // Skip if already has cross-links
    if (content.includes('eldoa-related-videos')) {
        console.log(`  Skipping (already has cross-links): ${path.basename(filePath)}`);
        return false;
    }

    // Extract entry ID from filename
    const entryId = path.basename(filePath, '.html');

    // Add data-entry-id to body tag if not present
    if (!content.includes('data-entry-id=')) {
        content = content.replace(
            /<body([^>]*)>/,
            `<body$1 data-entry-id="${entryId}">`
        );
    }

    // Add cross-link sections before FAQ section
    if (content.includes('<!-- FAQ Section -->')) {
        content = content.replace(
            '      <!-- FAQ Section -->',
            encyclopediaSections + '\n\n      <!-- FAQ Section -->'
        );
    } else if (content.includes('eldoa-faq')) {
        content = content.replace(
            /<section[^>]*class="eldoa-faq/,
            encyclopediaSections + '\n\n      <section class="eldoa-faq'
        );
    } else {
        // Add before bottom ad zone
        content = content.replace(
            '      <!-- Bottom Ad Zone -->',
            encyclopediaSections + '\n\n      <!-- Bottom Ad Zone -->'
        );
    }

    // Add script before closing body tag if not present
    if (!content.includes('cross-links.js')) {
        content = content.replace('</body>', encyclopediaScript + '\n</body>');
    }

    fs.writeFileSync(filePath, content);
    console.log(`  Updated: ${path.basename(filePath)}`);
    return true;
}

function updateVideoPage(filePath) {
    let content = fs.readFileSync(filePath, 'utf8');

    // Skip if already has cross-links
    if (content.includes('eldoa-related-encyclopedia')) {
        console.log(`  Skipping (already has cross-links): ${path.basename(filePath)}`);
        return false;
    }

    // Extract video ID from filename
    const videoId = path.basename(filePath, '.html');

    // Add data-video-id to body tag if not present
    if (!content.includes('data-video-id=')) {
        content = content.replace(
            /<body([^>]*)>/,
            `<body$1 data-video-id="${videoId}">`
        );
    }

    // Add cross-link sections before back-link
    if (content.includes('class="back-link"')) {
        content = content.replace(
            /<a href="\/videos\/"[^>]*class="back-link"/,
            videoSections + '\n\n        <a href="/videos/" class="back-link"'
        );
    }

    // Add script before closing body tag if not present
    if (!content.includes('cross-links.js')) {
        content = content.replace('</body>', videoScript + '\n</body>');
    }

    fs.writeFileSync(filePath, content);
    console.log(`  Updated: ${path.basename(filePath)}`);
    return true;
}

function main() {
    console.log('Adding cross-links to encyclopedia and video pages...\n');

    let encyclopediaCount = 0;
    let videoCount = 0;

    // Process encyclopedia pages
    console.log('Processing encyclopedia pages:');
    if (fs.existsSync(libraryDir)) {
        const files = fs.readdirSync(libraryDir)
            .filter(f => f.endsWith('.html') && !f.includes('index'));

        for (const file of files) {
            const filePath = path.join(libraryDir, file);
            if (updateEncyclopediaPage(filePath)) {
                encyclopediaCount++;
            }
        }
    }

    // Process video pages
    console.log('\nProcessing video pages:');
    if (fs.existsSync(videoPagesDir)) {
        const files = fs.readdirSync(videoPagesDir)
            .filter(f => f.endsWith('.html'));

        for (const file of files) {
            const filePath = path.join(videoPagesDir, file);
            if (updateVideoPage(filePath)) {
                videoCount++;
            }
        }
    }

    console.log(`\nDone! Updated ${encyclopediaCount} encyclopedia pages and ${videoCount} video pages.`);
}

main();
