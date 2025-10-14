import { defineMiddleware } from 'astro:middleware';
import fs from 'node:fs/promises';
import path from 'node:path';

// Pages that should NOT be redirected
const EXCLUDED_PATHS = [
  '/',
  '/about',
  '/research',
  '/do-we-need-to-age-extending-the-arc-of-life',
  '/index-original',
  '/index-simple',
];

// Cache of available research slugs
let researchSlugs: Set<string> | null = null;

async function getResearchSlugs(): Promise<Set<string>> {
  if (researchSlugs) return researchSlugs;
  
  const contentDir = path.resolve(process.cwd(), '../../Factory/content');
  const slugs = new Set<string>();
  
  try {
    const dirs = await fs.readdir(contentDir, { withFileTypes: true });
    for (const d of dirs) {
      if (!d.isDirectory()) continue;
      const contentFile = path.join(contentDir, d.name, 'content.json');
      try {
        const raw = await fs.readFile(contentFile, 'utf8');
        const json = JSON.parse(raw);
        if (json.type === 'research' && json.slug) {
          slugs.add(json.slug);
        }
      } catch {}
    }
  } catch {}
  
  researchSlugs = slugs;
  return slugs;
}

export const onRequest = defineMiddleware(async (context, next) => {
  const { pathname } = context.url;
  
  // Skip if it's an excluded path
  if (EXCLUDED_PATHS.includes(pathname)) {
    return next();
  }
  
  // Skip if it already has /research/ prefix
  if (pathname.startsWith('/research/')) {
    return next();
  }
  
  // Skip assets, etc
  if (pathname.startsWith('/assets/') || pathname.startsWith('/_') || pathname.includes('.')) {
    return next();
  }
  
  // Extract slug from root-level path
  const slug = pathname.slice(1); // Remove leading slash
  
  if (slug) {
    const slugs = await getResearchSlugs();
    
    // If this slug exists as a research page, redirect to /research/slug
    // This maintains backward compatibility while we work on root-level serving
    if (slugs.has(slug)) {
      return context.redirect(`/research/${slug}`, 301);
    }
  }
  
  return next();
});

