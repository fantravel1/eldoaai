/**
 * ELDOA City Page — Shared Rendering Logic
 * Each eldoa-{city}.html sets window.CITY_SLUG before loading this script.
 */

(function() {
  var citySlug = window.CITY_SLUG;
  if (!citySlug) {
    showError('No city specified', 'Please select a city to view.');
    return;
  }

  loadCityPage();

  async function loadCityPage() {
    try {
      var [cityResponse, practitionerResponse] = await Promise.all([
        fetch('/data/city-pages.json'),
        fetch('/data/practitioners.json')
      ]);

      var cityData = await cityResponse.json();
      var practitionerData = await practitionerResponse.json();
      var city = cityData.cities.find(function(c) { return c.slug === citySlug; });

      if (!city) {
        showError('City page not found', 'This city page does not exist yet. Browse our full practitioner directory instead.');
        return;
      }

      // Find practitioners for this city
      var cityPractitioners = practitionerData.practitioners.filter(function(p) {
        return city.practitionerCities && city.practitionerCities.some(function(c) {
          return p.city && p.city.toLowerCase() === c.toLowerCase();
        });
      });

      displayCityPage(city, cityPractitioners, cityData.cities);
    } catch (error) {
      console.error('Error loading city page:', error);
      showError('Error loading page', 'Please try refreshing the page.');
    }
  }

  function displayCityPage(city, practitioners, allCities) {
    var canonicalUrl = 'https://eldoa.ai/eldoa-' + city.slug + '.html';

    // Update structured data - ItemList
    var citySchema = {
      "@context": "https://schema.org",
      "@type": "ItemList",
      "name": "ELDOA Practitioners in " + city.name,
      "description": city.metaDescription,
      "url": canonicalUrl,
      "numberOfItems": practitioners.length,
      "itemListElement": practitioners.map(function(p, i) {
        return {
          "@type": "ListItem",
          "position": i + 1,
          "item": {
            "@type": "LocalBusiness",
            "name": p.practice || (p.name + " — ELDOA Practitioner"),
            "url": "https://eldoa.ai/practitioner.html?id=" + p.id,
            "address": {
              "@type": "PostalAddress",
              "addressLocality": p.city || city.name,
              "addressRegion": p.state || p.region || city.state,
              "addressCountry": p.country || city.country
            }
          }
        };
      })
    };
    var el = document.getElementById('city-schema');
    if (el) el.textContent = JSON.stringify(citySchema);

    // Update FAQ schema
    if (city.faqs && city.faqs.length) {
      var faqSchema = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": city.faqs.map(function(faq) {
          return {
            "@type": "Question",
            "name": faq.question,
            "acceptedAnswer": { "@type": "Answer", "text": faq.answer }
          };
        })
      };
      var faqEl = document.getElementById('faq-schema');
      if (faqEl) faqEl.textContent = JSON.stringify(faqSchema);
    }

    // Update breadcrumb schema
    var breadcrumbSchema = {
      "@context": "https://schema.org",
      "@type": "BreadcrumbList",
      "itemListElement": [
        { "@type": "ListItem", "position": 1, "name": "Home", "item": "https://eldoa.ai/" },
        { "@type": "ListItem", "position": 2, "name": "Find a Specialist", "item": "https://eldoa.ai/practitioners.html" },
        { "@type": "ListItem", "position": 3, "name": "ELDOA " + city.name, "item": canonicalUrl }
      ]
    };
    var bcEl = document.getElementById('breadcrumb-schema');
    if (bcEl) bcEl.textContent = JSON.stringify(breadcrumbSchema);

    // Sort practitioners: active first, then by level descending
    var sortedPractitioners = practitioners.slice().sort(function(a, b) {
      if (a.status === 'active' && b.status !== 'active') return -1;
      if (a.status !== 'active' && b.status === 'active') return 1;
      return (b.level || 0) - (a.level || 0);
    });

    var activePractitioners = sortedPractitioners.filter(function(p) { return p.status === 'active'; });
    var locationStr = [city.name, city.state, city.country].filter(Boolean).join(', ');

    var html = '';

    // Back link
    html += '<a href="/practitioners.html" class="back-link"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M19 12H5M12 19l-7-7 7-7"/></svg> Back to All Specialists</a>';

    // Hero Section
    html += '</div><section class="hero"><div class="container">';
    html += '<div class="hero-flag">' + city.flag + '</div>';
    html += '<h1>' + city.heroTitle + '</h1>';
    html += '<p>' + city.heroSubtitle + '</p>';

    html += '<div class="stats">';
    html += '<div class="stat"><div class="stat-num">' + activePractitioners.length + '</div><div class="stat-label">Active Practitioners</div></div>';
    html += '<div class="stat"><div class="stat-num">' + sortedPractitioners.length + '</div><div class="stat-label">Total Listed</div></div>';
    if (city.trainingHub) {
      html += '<div class="stat"><div class="stat-num">1</div><div class="stat-label">Training Hub</div></div>';
    }
    html += '<div class="stat"><div class="stat-num">' + (city.sportsConnections ? city.sportsConnections.length : 0) + '</div><div class="stat-label">Pro Sports Teams</div></div>';
    html += '</div>';

    html += '<div class="quick-links">';
    html += '<a href="#practitioners" class="quick-link primary"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.35-4.35"/></svg> View Practitioners</a>';
    html += '<a href="#about" class="quick-link secondary"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M12 16v-4M12 8h.01"/></svg> About ELDOA in ' + city.name + '</a>';
    html += '<a href="#faq" class="quick-link secondary"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3M12 17h.01"/></svg> FAQ</a>';
    html += '</div></div></section><div class="container">';

    // Training Hub
    if (city.trainingHub) {
      html += '<section class="section" id="training"><div class="hub-card">';
      html += '<h3>' + city.trainingHub.name + '</h3>';
      html += '<p>' + city.trainingHub.description + '</p>';
      if (city.trainingHub.website) html += '<p><a href="https://' + city.trainingHub.website + '" target="_blank" rel="noopener">' + city.trainingHub.website + '</a></p>';
      if (city.trainingHub.phone) html += '<p>' + city.trainingHub.phone + '</p>';
      html += '<span class="hub-badge">Official Training Hub</span></div></section>';
    }

    // About ELDOA in City
    html += '<section class="section" id="about"><div class="content-block">';
    html += '<h2><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg> ELDOA in ' + city.name + '</h2>';
    html += city.aboutCity + '</div></section>';

    // Why Popular
    if (city.whyPopular) {
      html += '<section class="section"><div class="content-block">';
      html += '<h2><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z"/></svg> Why ELDOA is Growing in ' + city.name + '</h2>';
      html += city.whyPopular + '</div></section>';
    }

    // Sports Connections
    if (city.sportsConnections && city.sportsConnections.length) {
      html += '<section class="section" id="sports"><div class="section-header">';
      html += '<h2 class="section-title">Pro Sports & Myofascial Training in ' + city.name + '</h2>';
      html += '<p class="section-desc">Professional sports teams and athletes in ' + city.name + ' are increasingly using myofascial stretching and fascial chain training — the same principles that underlie ELDOA.</p>';
      html += '</div><div class="sports-grid">';
      city.sportsConnections.forEach(function(s) {
        html += '<div class="sport-card"><span class="sport-badge">' + s.sport + '</span><h4>' + s.team + '</h4><p>' + s.note + '</p></div>';
      });
      html += '</div></section>';
    }

    // Practitioners Section
    html += '<section class="section" id="practitioners">';
    if (sortedPractitioners.length > 0) {
      html += '<div class="section-header"><h2 class="section-title">ELDOA Practitioners in ' + city.name + '</h2>';
      html += '<p class="section-desc">' + activePractitioners.length + ' active practitioner' + (activePractitioners.length !== 1 ? 's' : '') + ' trained to help with back pain, spinal decompression, and posture correction in ' + locationStr + '.</p></div>';
      html += '<div class="practitioners-grid">';
      sortedPractitioners.forEach(function(p) { html += renderPractitionerCard(p); });
      html += '</div>';
    } else {
      html += '<div class="no-practitioners-banner"><h3>No Practitioners Listed in ' + city.name + ' Yet</h3>';
      html += '<p>We don\'t currently have ELDOA practitioners listed in ' + city.name + ', but you can still get help! Explore our online options below, or use our free tools to start your ELDOA journey today.</p></div>';
    }

    // Online options
    if (city.onlineFallbacks && city.onlineFallbacks.length) {
      html += '<div style="margin-top:2rem"><h3 style="font-size:1.1rem;font-weight:700;margin-bottom:1rem">';
      html += (sortedPractitioners.length > 0 ? 'Online Alternatives' : 'Popular Online ELDOA Practitioners') + '</h3>';
      html += '<div class="online-grid">';
      city.onlineFallbacks.forEach(function(o) {
        html += '<a href="https://' + o.website + '" target="_blank" rel="noopener" class="online-card">';
        html += '<div class="online-card-name">' + o.name + '</div>';
        html += '<div class="online-card-url">' + o.website + '</div>';
        html += '<div class="online-card-desc">' + o.description + '</div></a>';
      });
      html += '</div></div>';
    }
    html += '</section>';

    // ELDOA Tools
    html += '<section class="section"><div class="tools-section">';
    html += '<h2>Free ELDOA Tools & Resources</h2>';
    html += '<p style="color:var(--muted);font-size:.95rem;margin-bottom:1.25rem">Start exploring ELDOA on your own with these free tools from ELDOA AI. No account required.</p>';
    html += '<div class="tools-grid">';
    html += '<a href="/diagnostic.html" class="tool-link"><div class="tool-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 12h-4l-3 9L9 3l-3 9H2"/></svg></div><div><div class="tool-name">Diagnostic Tool</div><div class="tool-desc">Find exercises for your specific pain</div></div></a>';
    html += '<a href="/videos/" class="tool-link"><div class="tool-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="5 3 19 12 5 21 5 3"/></svg></div><div><div class="tool-name">Video Library</div><div class="tool-desc">100+ guided exercise videos</div></div></a>';
    html += '<a href="/encyclopedia.html" class="tool-link"><div class="tool-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/></svg></div><div><div class="tool-name">Encyclopedia</div><div class="tool-desc">252+ anatomy & exercise entries</div></div></a>';
    html += '<a href="/posture-check.html" class="tool-link"><div class="tool-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg></div><div><div class="tool-name">Posture Check</div><div class="tool-desc">Assess your posture patterns</div></div></a>';
    html += '</div></div></section>';

    // FAQs
    if (city.faqs && city.faqs.length) {
      html += '<section class="section" id="faq"><div class="section-header">';
      html += '<h2 class="section-title">Frequently Asked Questions — ELDOA in ' + city.name + '</h2>';
      html += '<p class="section-desc">Common questions about finding ELDOA practitioners and classes in ' + city.name + '.</p></div>';
      html += '<div class="faq-list">';
      city.faqs.forEach(function(faq, i) {
        html += '<div class="faq-item' + (i === 0 ? ' open' : '') + '">';
        html += '<div class="faq-question" onclick="this.parentElement.classList.toggle(\'open\')"><span>' + faq.question + '</span>';
        html += '<svg class="faq-chevron" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 12 15 18 9"/></svg></div>';
        html += '<div class="faq-answer">' + faq.answer + '</div></div>';
      });
      html += '</div></section>';
    }

    // Nearby Cities
    if (city.nearbyPractitionerCities && city.nearbyPractitionerCities.length) {
      var nearbyCityLinks = city.nearbyPractitionerCities.map(function(nearbyName) {
        var nearbyCity = allCities.find(function(c) { return c.name === nearbyName; });
        var href = nearbyCity ? '/eldoa-' + nearbyCity.slug + '.html' : '/practitioners.html?search=' + encodeURIComponent(nearbyName);
        return '<a href="' + href + '" class="nearby-city-link"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg> ELDOA ' + nearbyName + '</a>';
      }).join('');

      html += '<section class="section"><div class="section-header">';
      html += '<h2 class="section-title">ELDOA in Nearby Cities</h2>';
      html += '<p class="section-desc">Explore ELDOA practitioners and classes in cities near ' + city.name + '.</p></div>';
      html += '<div class="nearby-cities">' + nearbyCityLinks + '</div></section>';
    }

    // All Practitioners CTA
    html += '<div class="all-practitioners-cta">';
    html += '<h2>Search All 213+ Practitioners Worldwide</h2>';
    html += '<p>Can\'t find what you need in ' + city.name + '? Browse our complete directory with practitioners in 15 countries.</p>';
    html += '<a href="/practitioners.html"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.35-4.35"/></svg> Browse Full Directory</a></div>';

    document.getElementById('main-content').innerHTML = '<div class="container">' + html + '</div>';
  }

  function renderPractitionerCard(p) {
    var location = [p.city, p.state || p.region, p.country].filter(Boolean).join(', ');
    var levelClass = p.level ? 'l' + p.level : '';
    var levelText = p.level ? 'Level ' + p.level : '';

    var creds = (p.credentials || []).slice(0, 4).map(function(c) {
      return '<span class="prac-cred">' + c + '</span>';
    }).join('');

    var specs = (p.specializations || []).slice(0, 3).join(' · ');

    var statusClass = (p.status || 'active').replace('-patients', '');
    var statusMap = { 'active': 'Active', 'not-accepting-patients': 'Not accepting new patients', 'deceased': 'Deceased', 'closed': 'Practice closed' };
    var statusText = statusMap[p.status || 'active'];

    var practiceHtml = p.practice ? '<div class="prac-practice">' + p.practice + '</div>' : '';

    return '<a href="/practitioner.html?id=' + p.id + '" class="prac-card">' +
      '<div class="prac-card-header"><div class="prac-name">' + p.name + '</div>' +
      (levelText ? '<span class="prac-level ' + levelClass + '">' + levelText + '</span>' : '') +
      '</div>' +
      '<div class="prac-location"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg> ' + location + '</div>' +
      (creds ? '<div class="prac-creds">' + creds + '</div>' : '') +
      (specs ? '<div class="prac-specs">' + specs + '</div>' : '') +
      practiceHtml +
      '<div class="prac-status"><span class="status-dot ' + statusClass + '"></span><span>' + statusText + '</span></div></a>';
  }

  function showError(title, message) {
    document.getElementById('main-content').innerHTML =
      '<div class="container">' +
      '<a href="/practitioners.html" class="back-link"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M19 12H5M12 19l-7-7 7-7"/></svg> Back to All Specialists</a>' +
      '<div class="error-state"><svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" style="margin-bottom:1rem;opacity:.4"><circle cx="12" cy="12" r="10"/><path d="M15 9l-6 6M9 9l6 6"/></svg>' +
      '<h2>' + title + '</h2><p>' + message + '</p>' +
      '<p style="margin-top:1rem"><a href="/practitioners.html">Browse All Practitioners</a></p></div></div>';
  }

  // Theme detection
  if (window.matchMedia('(prefers-color-scheme: dark)').matches) {
    document.documentElement.setAttribute('data-theme', 'dark');
  }
})();
