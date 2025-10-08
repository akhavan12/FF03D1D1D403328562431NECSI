import fs from 'node:fs/promises';
import path from 'node:path';

const FACTORY = process.env.FACTORY_DIR || path.resolve(process.cwd(), '../../Factory');
const CONTENT = path.join(FACTORY, 'content');

export type ContentDoc = {
  type: string;
  slug: string;
  title: string;
  subtitle?: string;
  summary?: string;
  narrative_md?: string;
  sections?: Record<string, any>;
};

export async function getAllContent(): Promise<ContentDoc[]> {
  const dirs = await fs.readdir(CONTENT, { withFileTypes: true });
  const items: ContentDoc[] = [];
  for (const d of dirs) {
    if (!d.isDirectory()) continue;
    const p = path.join(CONTENT, d.name, 'content.json');
    try {
      const raw = await fs.readFile(p, 'utf8');
      const j = JSON.parse(raw);
      items.push(j);
    } catch {}
  }
  return items;
}

export async function getResearchList() {
  const all = await getAllContent();
  return all.filter(x => x.type === 'research');
}

export async function getResearchBySlug(slug: string) {
  const p = path.join(CONTENT, slug, 'content.json');
  const raw = await fs.readFile(p, 'utf8');
  return JSON.parse(raw);
}

export async function getDocBySlug(slug: string) {
  const p = path.join(CONTENT, slug, 'content.json');
  const raw = await fs.readFile(p, 'utf8');
  return JSON.parse(raw);
}
