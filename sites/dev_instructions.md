NECSI Site Renderer — Developer Instructions

These instructions define how to build the public website that consumes the Factory’s data product (content/**, public_assets/**, and jobs/**). The renderer is a separate repo (suggested name: necsi-site).

⸻

1) Tech stack
	•	Framework: Astro (SSG) or Next.js (SSG-only). Pick one; examples below use Astro for simplicity and perf.
	•	Language: TypeScript.
	•	Styling: Tailwind CSS (or your preferred CSS system).
	•	MD rendering: @astrojs/markdown-remark (or next-mdx-remote in Next).
	•	Search: client-side JSON index (Lunr / MiniSearch) reading jobs/search-index.json.
	•	Analytics & SEO: Astro SEO integration (or Next SEO), sitemap and robots from content.

The site never mutates content. It only reads Factory artifacts.

⸻

2) Directory structure (renderer repo)

necsi-site/
  src/
    content/                  # thin adapter that reads Factory artifact paths
    pages/
      index.astro             # home / front door
      research/
        index.astro           # research listing (filters)
        [slug].astro          # research detail
      education/
        courses/[slug].astro  # course detail
        evolution/[slug].astro# lesson detail (optional collection)
    components/
      ResearchCard.astro
      TagPills.astro
      ContentBody.astro       # renders MD + figures
      RefList.astro           # renders references with outlet / date
      SearchBox.astro
      Pagination.astro
    lib/
      schema.d.ts             # TS types generated from Factory JSON Schema
      content.ts              # helpers to load JSON + assets
      search.ts               # loads jobs/search-index.json
  public/
    assets/                   # symlink/copy to Factory/public_assets
  scripts/
    link-content.mjs          # copies or links artifacts from Factory
  .env.example
  astro.config.mjs
  package.json

Artifacts consumed at build-time:
	•	FACTORY_DIR=/path/to/r/Factory
	•	FACTORY_CONTENT=$FACTORY_DIR/content
	•	FACTORY_ASSETS=$FACTORY_DIR/public_assets
	•	FACTORY_JOBS=$FACTORY_DIR/jobs

A scripts/link-content.mjs script should:
	1.	Ensure public/assets is linked or copied from FACTORY_ASSETS.
	2.	Copy jobs/search-index.json into src/content/search-index.json (or read directly at build).

⸻

3) Types from schema

Generate TS types from the Factory JSON Schema (kept in r/Factory/schemas). Use json-schema-to-typescript at build:

npx json-schema-to-typescript r/Factory/schemas/content.schema.json > src/lib/schema.d.ts

Key types used by the renderer:
	•	ContentEnvelope (shared fields)
	•	ResearchItem, CourseItem, LessonItem

⸻

4) Content loader

Example src/lib/content.ts for Astro:

import fs from 'node:fs/promises';
import path from 'node:path';

const FACTORY = process.env.FACTORY_DIR || '../r/Factory';
const CONTENT = path.join(FACTORY, 'content');
const JOBS = path.join(FACTORY, 'jobs');

export async function getResearchList() {
  const dir = path.join(CONTENT, 'research');
  const files = await fs.readdir(dir);
  const items = await Promise.all(files.filter(f=>f.endsWith('.json')).map(async f => {
    const j = JSON.parse(await fs.readFile(path.join(dir, f), 'utf8'));
    return j; // assumes ResearchItem shape
  }));
  return items;
}

export async function getResearchBySlug(slug: string) {
  const file = path.join(CONTENT, 'research', `${slug}.json`);
  return JSON.parse(await fs.readFile(file, 'utf8'));
}

export async function getSearchIndex() {
  return JSON.parse(await fs.readFile(path.join(JOBS, 'search-index.json'), 'utf8'));
}


⸻

5) Routes & pages

Research list (/research)
	•	Reads all content/research/*.json.
	•	Filter UI bound to categories and tags (from each item).
	•	Sort options: relevance (if query), newest (if provenance.captured_at), or alphabetical.
	•	Cards show: title, summary, top tags, and a callout badge if sections.media_coverage.length > 0.

Research detail (/research/[slug])
	•	Render title, summary, hero image (if present).
	•	ContentBody renders narrative_md (Markdown → HTML). Figures resolve to /assets/<slug>/….
	•	RefList sections: Introductions, Research, Policy, Media (render if non-empty).
	•	Related items: tag intersection (≥2 tags) and/or manually curated related_slugs if present.

Education
	•	Courses at /education/courses/[slug] with: dates, tuition tiers, sessions list, scholarship block, contact.
	•	Evolution lessons at /education/evolution/[slug] with: objectives, materials, activities, assessments, downloads.

⸻

6) Assets & static files
	•	The renderer serves /assets/** directly from public/assets/**.
	•	Ensure your build step links or copies r/Factory/public_assets into necsi-site/public/assets.

node scripts/link-content.mjs # copies/symlinks assets & ensures search index path


⸻

7) Search
	•	Load jobs/search-index.json at runtime (client or server) and build a lightweight index with MiniSearch/Lunr.
	•	Fields: title, summary, tags, first 2k chars of narrative_md, and slug.
	•	Display top N results with highlight snippets.

⸻

8) Redirects
	•	Read jobs/redirects.csv at build and produce framework-specific redirects:
	•	Astro: astro.config.mjs redirects map.
	•	Next: generate a next.config.js async redirects() list.
	•	Default status: 301; allow per-row override.

⸻

9) SEO & a11y
	•	Auto-generate OpenGraph/Twitter tags from envelope fields.
	•	Sitemap from all content slugs.
	•	Validate color contrast, alt text (derive from manifest caption if missing).

⸻

10) Environment & build

Local dev

export FACTORY_DIR=../r/Factory
node scripts/link-content.mjs
pnpm dev   # or npm/yarn

Static build

export FACTORY_DIR=../r/Factory
node scripts/link-content.mjs
pnpm build

Preview deploys use artifact hashes in the output directory name (e.g., /v/<content-hash>/).

⸻

11) CI/CD
	•	On push to main in necsi-site:
	1.	Download Factory artifacts (or mount via submodule/checkout).
	2.	node scripts/link-content.mjs
	3.	Build site
	4.	Publish to CDN (Netlify, Vercel, S3+CloudFront).
	•	Pin builds to content hash to make rollbacks trivial.

⸻

12) Theming & components
	•	Centralize typography/colors in a small design system (tokens).
	•	Components render from schema, not from HTML; all layout is template-driven.

⸻

13) Local preview against different content snapshots

Allow a CONTENT_SNAPSHOT env var (hash or path) to swap to a different r/Factory/dist/content-<hash>.tar.gz without changing code.

⸻

14) Smoke tests
	•	Ensure at least one page of each type builds and renders.
	•	Validate that /research has filters populated and at least one card links to a detail page.
	•	Check that all referenced images exist at /assets/<slug>/….

⸻

15) Cutover checklist
	•	Upload redirects; verify top legacy URLs.
	•	Crawl for 404s.
	•	Verify search index loads and returns results.
	•	Confirm canonical tags (no duplicate tag variants).
	•	Enable caching headers for /assets/** (long TTL) and HTML (short TTL).

⸻

That’s it. This renderer is intentionally thin: it trusts the Factory’s schema and artifacts, assembles pages deterministically, and keeps the public site fast and maintainable.