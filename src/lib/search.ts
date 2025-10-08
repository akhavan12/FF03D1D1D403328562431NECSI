import fs from 'node:fs/promises';
import path from 'node:path';

const FACTORY = process.env.FACTORY_DIR || path.resolve(process.cwd(), '../../Factory');
const JOBS = path.join(FACTORY, 'jobs');

export async function getSearchIndex() {
  return JSON.parse(await fs.readFile(path.join(JOBS, 'search-index.json'), 'utf8'));
}
