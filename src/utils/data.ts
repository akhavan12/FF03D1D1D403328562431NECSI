import type { PageData } from '../types';

// Get all page data files
export async function getAllPages(): Promise<PageData[]> {
  const dataDir = new URL('../data/', import.meta.url);
  const pages: PageData[] = [];
  
  // Get the main index.json
  try {
    const mainPage = await import('../data/index.json');
    pages.push(mainPage.default);
  } catch (error) {
    console.error('Error loading main page:', error);
  }
  
  // Get all subdirectory index.json files
  // Note: In a real implementation, you'd need to dynamically discover these
  // For now, we'll create a list of known paths
  const knownPaths = [
    'about',
    'research',
    'engage',
    'compassionate-science',
    'support',
    'privacy-policy',
    'certificate-programs-1',
    'certificateprograms',
    'concepts-and-applications-of-complexity-science',
    'principles-of-public-health',
    'google-search',
    'affiliates',
    'faculty',
    'researchers-and-staff',
    'books',
    'journals',
    'online-resources',
    'video-archive',
    'visualizations',
    'recent-papers',
    'research-archive',
    'research-overview',
    'student-opportunities',
    'faculty-position',
    'join-our-team',
    'newsletter-optin',
    'store-2',
    'monthlymemberships',
    'special-membership-levels',
    'apply-for-academic-scholarship',
    'register-for-eqai',
    'eq-ai-2401-empowering-resilient-leadership',
    'conversations-about-complexity',
    'making-things-work',
    'why-complexity-is-different',
    'an-introduction-to-complex-systems-science-and-its-applications',
    'an-introduction-to-complex-systems-science-and-its-applications-chinese',
    'concepts-and-applications-of-complexity-science',
    'dynamics-of-complex-systems',
    'complexity-logic-and-cognition',
    'multiscale-methods',
    'evolution-and-systems-biology',
    'social-complexity',
    'economic-dynamics',
    'healthcare',
    'education',
    'military',
    'engineering',
    'business',
    'sports',
    'biodiversity',
    'evolution',
    'networks',
    'social-systems',
    'social-media',
    'social-psychological-systems',
    'complex-social-psychological-systems',
    'chaos-complexity-and-entropy',
    'multiscale-information-and-universality',
    'concept-map',
    'visualizing-complex-systems-science',
    'visual-figures',
    'visual-airplane-design',
    'visual-capture-the-flag',
    'visualizing-the-heartbeat-of-a-city-with-tweets',
    'wikimania-2014',
    'significant-points',
    'necsi-on-the-radio',
    'necsi-work-on-catastrophes',
    'history-necsi-and-the-2004-red-sox-parade',
    'corona-virus-pandemic',
    'ebola-in-the-democratic-republic-of-the-congo-in-2018',
    'ending-pandemics',
    'beyond-contact-tracing',
    'stopping-zika-and-microcephaly',
    'the-case-for-pyriproxyfen-as-a-potential-cause-of-microcephaly-from-biology-to-epidemiology',
    'financial-crisis',
    'stopping-the-market-crash',
    'the-stock-market-has-grown-unstable-since-february-2018',
    'preliminary-steps-toward-a-universal-economic-dynamics-for-monetary-and-fiscal-policy',
    'the-dynamics-of-financial-flows-and-their-significance-for-development',
    'how-can-we-balance-the-economy-to-create-sustainable-growth-for-everyone',
    'food-crisis',
    'ethnic-violence',
    'science-of-ethnic-violence',
    'solving-ethnic-violence',
    'good-fences-the-importance-of-setting-boundaries-for-peaceful-coexistence',
    'segregation-and-polarization-in-urban-areas',
    'us-social-fragmentation-at-multiple-scales',
    'the-transition-from-search-to-social-media',
    'global-patterns-of-synchronization-in-human-communications',
    'how-do-people-differ-a-social-media-approach',
    'the-future-of-new-orleans',
    'risk-and-opportunity-in-the-space-of-possibilities',
    'fixing-science-using-a-new-science-of-science',
    'rethinking-psychology-research-with-jerome-kagan',
    'teams-a-manifesto',
    'power-and-leadership',
    'precautionary-principle',
    'negative-representation-and-instability-in-democratic-elections-nature',
    'negative-representation-video',
    'the-inherent-instability-of-disordered-systems',
    'renormalization-of-sparse-disorder-in-the-ising-model',
    'beyond-big-data-identifying-important-information-for-real-world-challenges',
    'accurate-market-price-formation-model',
    'does-replacing-coal-with-wood-lower-co2-emissions-dynamic-lifecycle-analysis-of-wood-bioenergy',
    'how-much-sodium-should-we-eat',
    'healthcare-costs-the-road-map',
    'complex-systems-science-where-does-it-come-from-and-where-is-it-going-to',
    'evolution-of-cooperation',
    'evolution-of-lifespans',
    'group-selection',
    'a-mathematical-theory-of-interpersonal-interactions-and-group-behavior',
    'a-lesson-in-the-errors-of-statistical-thinking-nate-silver-on-trump',
    'aaron-rothschild',
    'albert-laszlo-barabasi',
    'ataro-paul-stephen-ayella',
    'blake-lebaron',
    'c-peter-timmer',
    'charles-cantor',
    'dan-braha',
    'daniel-zoughbie',
    'dean-lebaron',
    'deb-roy',
    'eric-feigl-ding',
    'eric-klopfer',
    'ernest-hartmann',
    'frannie-leautier',
    'fumiaki-katagiri',
    'greg-lindsay',
    'gunter-wagner',
    'irving-epstein',
    'james-h-stock',
    'jeffrey-fuhrer',
    'jeffrey-r-cares',
    'jerome-kagan',
    'joa-jakeno-obitachiki-okech-ojony',
    'john-sterman',
    'justin-werfel',
    'kaitlinsundling',
    'larry-rudolph',
    'les-kaufman',
    'luci-leykum',
    'mark-esposito',
    'mehran-kardar',
    'michel-baranger',
    'nassim-nicholas-taleb',
    'peter-senge',
    'roozbeh-daneshvar',
    'sandy-pentland',
    'stephane-bilodeau',
    'stuart-pimm',
    'sunil-raina',
    'temple-smith',
    'terrence-deacon',
    'thomas-c-schelling',
    'thomas-petzinger',
    'walter-vester',
    'william-gelbart',
    'engage-1',
    'research-1',
    '-star-movies-mobile-app-released'
  ];

  for (const path of knownPaths) {
    try {
      const pageData = await import(`../data/${path}/index.json`);
      pages.push(pageData.default);
    } catch (error) {
      // Skip if file doesn't exist
      console.warn(`Could not load page data for ${path}:`, error);
    }
  }

  return pages;
}

// Get a specific page by route path
export async function getPageByRoute(routePath: string): Promise<PageData | null> {
  try {
    if (routePath === '/' || routePath === '') {
      const mainPage = await import('../data/index.json');
      return mainPage.default;
    }
    
    // Remove leading slash and try to import
    const cleanPath = routePath.replace(/^\//, '');
    const pageData = await import(`../data/${cleanPath}/index.json`);
    return pageData.default;
  } catch (error) {
    console.error(`Error loading page data for ${routePath}:`, error);
    return null;
  }
}

// Get pages by type
export async function getPagesByType(type: PageData['type']): Promise<PageData[]> {
  const allPages = await getAllPages();
  return allPages.filter(page => page.type === type);
}

// Get all unique menu items from all pages (for navigation)
export async function getGlobalNavigation(): Promise<Array<{label: string; href: string}>> {
  const allPages = await getAllPages();
  const menuItems = new Map<string, {label: string; href: string}>();
  
  allPages.forEach(page => {
    page.navbar.menu.forEach(item => {
      // Convert href to clean route path
      let cleanHref = item.href;
      if (cleanHref.startsWith('./')) {
        cleanHref = cleanHref.replace('./', '/');
      }
      if (cleanHref.endsWith('/index.html')) {
        cleanHref = cleanHref.replace('/index.html', '');
      }
      if (cleanHref === '/index.html') {
        cleanHref = '/';
      }
      
      menuItems.set(item.label, {
        label: item.label,
        href: cleanHref
      });
    });
  });
  
  return Array.from(menuItems.values());
}
