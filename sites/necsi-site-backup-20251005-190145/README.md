# NECSI Site Renderer (necsi-site)

This is a thin static site renderer that consumes artifacts from the Factory (`r/Factory`). It never mutates content; it only reads JSON and serves public assets.

- Content: `${FACTORY_DIR}/content/**` (per-slug `content.json`)
- Assets: `${FACTORY_DIR}/public_assets/**` (served under `/assets`)
- Jobs: `${FACTORY_DIR}/jobs/**` (e.g., `search-index.json`)

See `../dev_instructions.md` for the full plan. This repo scaffolds the basics with Astro.

## Quick start

1. Install deps

```
pnpm install
# or npm/yarn
```

2. Point to Factory and link content

```
export FACTORY_DIR=../../Factory
node scripts/link-content.mjs
```

3. Dev server

```
pnpm dev
```

4. Build

```
node scripts/link-content.mjs
pnpm build
```

## Notes
- We scan `${FACTORY_DIR}/content/*/content.json` and filter by `type`.
- We serve assets by symlinking/copying `${FACTORY_DIR}/public_assets` into `public/assets`.
