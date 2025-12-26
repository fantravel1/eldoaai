#!/usr/bin/env node
/**
 * Script to add cross-linking sections to all encyclopedia and video pages
 */

const fs = require('fs');
const path = require('path');

const libraryDir = path.join(__dirname, '..', 'library');
const encyclopediaDir = path.join(__dirname, '..', 'encyclopedia');
const videoPagesDir = path.join(__dirname, '..', 'videos', 'pages');

// Cross-link sections to add to library pages (more styled)
const librarySections = `
      <!-- Related Videos (Dynamic) -->
      <section id="eldoa-related-videos" class="eldoa-related eldoa-section" data-section="videos" style="display:none;"></section>

      <!-- Related Research (Dynamic) -->
      <section id="eldoa-related-research" class="eldoa-related eldoa-section" data-section="research" style="display:none;"></section>

      <!-- Find a Practitioner (Dynamic) -->
      <section id="eldoa-find-practitioner" class="eldoa-related eldoa-section" data-section="practitioners" style="display:none;"></section>`;

// Cross-link sections for /encyclopedia/ pages (simpler style)
const encyclopediaSections = `
<div class="content-section" id="eldoa-related-videos" style="display:none;"></div>
<div class="content-section" id="eldoa-related-research" style="display:none;"></div>
<div class="content-section" id="eldoa-find-practitioner" style="display:none;"></div>`;

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
        <!-- Similar Videos (Dynamic) -->
        <div id="eldoa-similar-videos" class="description" style="display:none;"></div>

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
                window.ELDOACrossLinks.initForVideoEnhanced(videoId);
            }
        });
    </script>`;

// Cross-link sections for research pages
const researchSections = `
      <div class="related-articles" id="eldoa-related-videos" style="display:none; margin-top: 3rem;"></div>
      <div class="related-articles" id="eldoa-find-practitioner" style="display:none; margin-top: 3rem;"></div>`;

const researchScript = `
  <!-- Cross-Linking Module -->
  <script src="/assets/js/cross-links.js"></script>
  <script>
    document.addEventListener('DOMContentLoaded', function() {
      const researchId = document.body.dataset.researchId;
      if (researchId && window.ELDOACrossLinks) {
        window.ELDOACrossLinks.initForResearch(researchId);
      }
    });
  </script>`;

function updateLibraryPage(filePath) {
    let content = fs.readFileSync(filePath, 'utf8');

    // Skip if already has cross-links
    if (content.includes('eldoa-related-videos')) {
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
            librarySections + '\n\n      <!-- FAQ Section -->'
        );
    } else if (content.includes('eldoa-faq')) {
        content = content.replace(
            /<section[^>]*class="eldoa-faq/,
            librarySections + '\n\n      <section class="eldoa-faq'
        );
    } else {
        content = content.replace(
            '      <!-- Bottom Ad Zone -->',
            librarySections + '\n\n      <!-- Bottom Ad Zone -->'
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

function updateEncyclopediaPage(filePath) {
    let content = fs.readFileSync(filePath, 'utf8');

    // Skip if already has cross-links
    if (content.includes('eldoa-related-videos')) {
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

    // Add cross-link sections before back-link
    if (content.includes('class="back-link"')) {
        content = content.replace(
            /<a class="back-link"/,
            encyclopediaSections + '\n<a class="back-link"'
        );
    } else {
        // Add before closing container div
        content = content.replace(
            '</div>\n</body>',
            encyclopediaSections + '\n</div>\n</body>'
        );
    }

    // Add script before closing body tag if not present
    if (!content.includes('cross-links.js')) {
        content = content.replace('</body>', encyclopediaScript + '\n</body>');
    }

    fs.writeFileSync(filePath, content);
    return true;
}

function updateVideoPage(filePath) {
    let content = fs.readFileSync(filePath, 'utf8');
    let updated = false;

    // Check if needs similar videos added
    const needsSimilarVideos = !content.includes('eldoa-similar-videos');
    const needsEnhancedInit = content.includes('initForVideo(') && !content.includes('initForVideoEnhanced(');

    // Skip if already fully updated
    if (!needsSimilarVideos && !needsEnhancedInit && content.includes('eldoa-related-encyclopedia')) {
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
        updated = true;
    }

    // Add similar videos section if missing
    if (needsSimilarVideos && content.includes('eldoa-related-encyclopedia')) {
        content = content.replace(
            '<div id="eldoa-related-encyclopedia"',
            `<!-- Similar Videos (Dynamic) -->
        <div id="eldoa-similar-videos" class="description" style="display:none;"></div>

        <div id="eldoa-related-encyclopedia"`
        );
        updated = true;
    } else if (!content.includes('eldoa-related-encyclopedia') && content.includes('class="back-link"')) {
        // Add all cross-link sections before back-link
        content = content.replace(
            /<a href="\/videos\/"[^>]*class="back-link"/,
            videoSections + '\n\n        <a href="/videos/" class="back-link"'
        );
        updated = true;
    }

    // Upgrade to enhanced init
    if (needsEnhancedInit) {
        content = content.replace('initForVideo(videoId)', 'initForVideoEnhanced(videoId)');
        updated = true;
    }

    // Add script before closing body tag if not present
    if (!content.includes('cross-links.js')) {
        content = content.replace('</body>', videoScript + '\n</body>');
        updated = true;
    }

    if (updated) {
        fs.writeFileSync(filePath, content);
    }
    return updated;
}

function updateResearchPage(filePath, researchId) {
    let content = fs.readFileSync(filePath, 'utf8');

    // Skip if already has cross-links
    if (content.includes('eldoa-related-videos')) {
        return false;
    }

    // Add data-research-id to body tag if not present
    if (!content.includes('data-research-id=')) {
        content = content.replace(
            /<body([^>]*)>/,
            `<body$1 data-research-id="${researchId}">`
        );
    }

    // Add cross-link sections before closing article tag
    if (content.includes('</article>')) {
        content = content.replace(
            '</article>',
            researchSections + '\n    </article>'
        );
    }

    // Add script before closing body tag if not present
    if (!content.includes('cross-links.js')) {
        content = content.replace('</body>', researchScript + '\n</body>');
    }

    fs.writeFileSync(filePath, content);
    return true;
}

function main() {
    console.log('Adding cross-links to encyclopedia, video, and research pages...\n');

    let libraryCount = 0;
    let encyclopediaCount = 0;
    let videoCount = 0;
    let researchCount = 0;

    // Process library pages
    console.log('Processing library pages:');
    if (fs.existsSync(libraryDir)) {
        const files = fs.readdirSync(libraryDir)
            .filter(f => f.endsWith('.html') && !f.includes('index'));

        for (const file of files) {
            const filePath = path.join(libraryDir, file);
            if (updateLibraryPage(filePath)) {
                libraryCount++;
            }
        }
        console.log(`  Processed ${files.length} files, updated ${libraryCount}`);
    }

    // Process encyclopedia pages
    console.log('\nProcessing encyclopedia pages:');
    if (fs.existsSync(encyclopediaDir)) {
        const files = fs.readdirSync(encyclopediaDir)
            .filter(f => f.endsWith('.html') && !f.includes('index'));

        let processed = 0;
        for (const file of files) {
            const filePath = path.join(encyclopediaDir, file);
            if (updateEncyclopediaPage(filePath)) {
                encyclopediaCount++;
            }
            processed++;
            if (processed % 100 === 0) {
                console.log(`  Processed ${processed} files...`);
            }
        }
        console.log(`  Processed ${files.length} files, updated ${encyclopediaCount}`);
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
        console.log(`  Processed ${files.length} files, updated ${videoCount}`);
    }

    // Process research pages
    console.log('\nProcessing research pages:');
    const researchDir = path.join(__dirname, '..', 'research');
    const researchArticles = [
        'athletic-performance',
        'breathing-foundation',
        'digital-posture-crisis',
        'neurological-mechanisms-eldoa',
        'visceral-autonomic-effects',
        'visual-performance-posture'
    ];

    for (const article of researchArticles) {
        const filePath = path.join(researchDir, article, 'index.html');
        if (fs.existsSync(filePath)) {
            if (updateResearchPage(filePath, article)) {
                researchCount++;
                console.log(`  Updated: ${article}`);
            }
        }
    }
    console.log(`  Updated ${researchCount} research pages`);

    console.log(`\nDone! Updated ${libraryCount} library, ${encyclopediaCount} encyclopedia, ${videoCount} video, and ${researchCount} research pages.`);
}

main();
