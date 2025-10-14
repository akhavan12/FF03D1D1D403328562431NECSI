import fs from 'node:fs/promises';
import path from 'node:path';

const FACTORY = process.env.FACTORY_DIR || path.resolve(process.cwd(), '../../Factory');
const DEST = path.resolve(process.cwd(), 'public/assets');
const SRC = path.join(FACTORY, 'public_assets');

async function ensureDir(p) { await fs.mkdir(p, { recursive: true }); }

async function copyDir(src, dest) {
  await ensureDir(dest);
  const entries = await fs.readdir(src, { withFileTypes: true });
  for (const e of entries) {
    const s = path.join(src, e.name);
    const d = path.join(dest, e.name);
    if (e.isDirectory()) {
      await copyDir(s, d);
    } else if (e.isFile()) {
      await ensureDir(path.dirname(d));
      await fs.copyFile(s, d);
    }
  }
}

async function main() {
  console.log('FACTORY=', FACTORY);
  await ensureDir(DEST);
  await copyDir(SRC, DEST);
  console.log('Assets copied to public/assets');
}

main().catch((e)=>{ console.error(e); process.exit(1); });
