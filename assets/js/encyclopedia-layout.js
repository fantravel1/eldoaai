/**
 * ELDOA Encyclopedia Layout Loader
 * Dynamically injects header and footer components into encyclopedia pages
 */
(function() {
  'use strict';

  // Configuration
  const config = {
    headerPath: '/components/header.html',
    footerPath: '/components/footer.html',
    kidsMode: window.location.pathname.includes('/kids/')
  };

  // Detect if we're on a kids page and adjust paths/styling
  const isKidsPage = config.kidsMode;

  /**
   * Fetch and inject a component
   */
  async function loadComponent(path, targetSelector, position) {
    try {
      const response = await fetch(path);
      if (!response.ok) throw new Error(`Failed to load ${path}`);

      const html = await response.text();
      const target = document.querySelector(targetSelector);

      if (target) {
        if (position === 'before') {
          target.insertAdjacentHTML('afterbegin', html);
        } else {
          target.insertAdjacentHTML('beforeend', html);
        }
        return true;
      }
      return false;
    } catch (error) {
      console.warn('ELDOA Layout: Could not load component', path, error);
      return false;
    }
  }

  /**
   * Create and inject header wrapper
   */
  function createHeaderWrapper() {
    const wrapper = document.createElement('div');
    wrapper.id = 'eldoa-header-inject';
    document.body.insertBefore(wrapper, document.body.firstChild);
    return wrapper;
  }

  /**
   * Create and inject footer wrapper
   */
  function createFooterWrapper() {
    const wrapper = document.createElement('div');
    wrapper.id = 'eldoa-footer-inject';

    // Find the container and insert footer after it
    const container = document.querySelector('.container');
    if (container) {
      container.parentNode.insertBefore(wrapper, container.nextSibling);
    } else {
      document.body.appendChild(wrapper);
    }
    return wrapper;
  }

  /**
   * Apply additional styles for encyclopedia integration
   */
  function applyIntegrationStyles() {
    const style = document.createElement('style');
    style.textContent = `
      /* Ensure proper spacing with header */
      body {
        margin: 0;
        padding: 0;
      }

      /* Adjust container for header */
      .container {
        margin-top: 0;
      }

      /* Kids encyclopedia special styling */
      ${isKidsPage ? `
      .eldoa-global-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
      }

      .eldoa-nav-mobile {
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%) !important;
      }

      .eldoa-logo a span:last-child::after {
        content: " for Kids";
        font-size: 0.7em;
        opacity: 0.8;
      }
      ` : ''}

      /* Smooth transitions */
      .eldoa-global-header,
      .eldoa-global-footer {
        opacity: 0;
        animation: fadeInLayout 0.3s ease forwards;
      }

      @keyframes fadeInLayout {
        to {
          opacity: 1;
        }
      }

      /* Fix z-index stacking */
      .eldoa-global-header {
        position: sticky;
        top: 0;
        z-index: 1000;
      }

      /* Ensure footer stays at bottom */
      .eldoa-global-footer {
        margin-top: auto;
      }

      /* Back link adjustment */
      .back-link {
        margin-bottom: 0;
      }
    `;
    document.head.appendChild(style);
  }

  /**
   * Update navigation links for current context
   */
  function updateNavLinks() {
    // Update active state based on current page
    const currentPath = window.location.pathname;

    document.querySelectorAll('.eldoa-nav-desktop a, .eldoa-nav-mobile a').forEach(link => {
      if (link.getAttribute('href') === currentPath) {
        link.style.fontWeight = 'bold';
        link.style.opacity = '1';
      }
    });

    // For kids pages, update some links
    if (isKidsPage) {
      document.querySelectorAll('.eldoa-nav-desktop a, .eldoa-nav-mobile a').forEach(link => {
        const href = link.getAttribute('href');
        // Update Encyclopedia link to point to kids version
        if (href === '/library/encyclopedia.html') {
          link.setAttribute('href', '/kids/encyclopedia.html');
          link.textContent = link.textContent.replace('Encyclopedia', 'Kids Encyclopedia');
        }
      });
    }
  }

  /**
   * Initialize the layout
   */
  async function init() {
    // Only run on encyclopedia pages
    const isEncyclopediaPage = window.location.pathname.includes('/encyclopedia/');
    if (!isEncyclopediaPage) return;

    // Check if already loaded
    if (document.getElementById('eldoa-header-inject')) return;

    // Apply integration styles first
    applyIntegrationStyles();

    // Create wrappers
    const headerWrapper = createHeaderWrapper();
    const footerWrapper = createFooterWrapper();

    // Load components
    const headerLoaded = await loadComponent(config.headerPath, '#eldoa-header-inject', 'before');
    const footerLoaded = await loadComponent(config.footerPath, '#eldoa-footer-inject', 'before');

    // Update navigation after loading
    if (headerLoaded) {
      updateNavLinks();

      // Dispatch event for other scripts
      const event = new CustomEvent('component-loaded', {
        detail: { component: 'header' }
      });
      document.getElementById('eldoa-header-inject').dispatchEvent(event);
    }

    // Log success
    if (headerLoaded && footerLoaded) {
      console.log('ELDOA Layout: Header and footer loaded successfully');
    }
  }

  // Run when DOM is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
