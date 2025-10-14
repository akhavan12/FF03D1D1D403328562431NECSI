# NECSI Site Rebuilder

This repository contains two cooperating parts:

- `Factory/` — the content pipeline (ingest → normalize → build) that turns
  source captures into structured JSON and site-ready assets.
- `sites/necsi-site/` — an Astro/Tailwind front-end that renders the built
  content from `Factory/content/`.

## Quick Start

### Prerequisites
- macOS or Linux
- Node 18+ and npm
- Python 3.10+

### 1) Set up Factory (Python)
```
cd Factory
python3 -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install -r requirements.txt
```

#### Ingest sources
- Put webarchives into `Factory/incoming/` (research pages) or
  `Factory/incoming/panels/` (panel-style pages like About).
- Use the bulk ingestor to process many files at once:
```
python scripts/bulk_ingest.py --dry-run         # show plan
python scripts/bulk_ingest.py --build           # ingest + build all
# or a subset
python scripts/bulk_ingest.py --only about,ending-pandemics --build
```

Notes:
- Slugs are auto-detected from `og:url`/canonical inside the page (fallback: page URL).
- Build outputs go to `Factory/content/<slug>/content.json`.
- Debug artifacts are written to `Factory/jobs/debug/<slug>/` (e.g., `hero.json`, `panels.json`).

### 2) Run the site (Astro + Tailwind)
```
cd sites/necsi-site
npm install
# Sync assets exported by Factory into the site's public folder
npm run sync:assets
# Start dev server
npm run dev
# open http://localhost:4321/
```

The site reads JSON from `Factory/content/` at runtime; you do not need to rebuild
the site when content changes, but you should re-run `npm run sync:assets` when new
images are added by Factory.

## Repository Structure
```
Factory/
  ingest/           # Input readers (e.g., webarchive)
  normalize/        # Cleanup, section extraction, panel extraction, assets
  necsifactory/     # CLI orchestrator (typer-based)
  content/          # Built JSON (git-tracked for now; heavy assets ignored)
  public_assets/    # Downloaded images from sources (git-ignored)
  jobs/debug/       # Debug outputs per slug (git-ignored)
  scripts/          # Utilities (bulk_ingest.py)
  incoming/         # Source captures (webarchives)
  incoming/panels/  # Panel-style pages (e.g., About)

sites/necsi-site/
  src/pages/        # Astro pages (about, research detail/index)
  src/lib/          # Content loader helpers and markdown utils
  src/layouts/      # Base layout shared across pages
  public/assets/    # Synced images (git-ignored)
```

## Common Tasks

- Build a single slug to latest state:
```
cd Factory && source .venv/bin/activate
python -m necsifactory.cli run <slug> --to BUILT --force --replace --snapshot
```

- Sync assets into the site:
```
cd sites/necsi-site
npm run sync:assets
```

- Add a new panel-style page (e.g., another landing page):
1. Place its `.webarchive` into `Factory/incoming/panels/`.
2. Build with the CLI or `scripts/bulk_ingest.py --build`.
3. Sync assets and refresh the site.

## Panel Pages (About)
- The panel extractor groups Squarespace sections into ordered `panels` with:
  `type`, `title`, `body_md`, optional `media.image`, `buttons`, and layout hints.
- For hero-like headings, the pipeline promotes the first H1/H2 to page-level
  `title`/`subtitle` and cleans them from the first panel.
- For the About page, an additional rule inserts the H3 under “About Complex Systems”
  as the subheading for that panel.

## Troubleshooting
- If images don’t appear on the site, re-run `npm run sync:assets` and refresh.
- Some `.webarchive` files are binary plists. To inspect:
  - `plutil -convert xml1 path/to/file.webarchive -o page.xml`, or
  - Use Python `plistlib` to read `WebMainResource` and `WebResourceData`.

## Contributing
- Create a new branch from `main`.
- Commit focused changes with clear messages.
- Open a PR against `main`.

---
For any questions on the pipeline or extractor behavior, see
`Factory/docs/README.md` and `Factory/normalize/` modules (`panels.py`, `sections.py`).
