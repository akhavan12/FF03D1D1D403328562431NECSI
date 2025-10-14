# NECSI Content Foundry — Developer Instructions (v2)
## Stage-2 Processing: Strip Unnecessary Stuff + One-Command Pipeline

This document defines the **Stage‑2 cleanup & build** pass that runs after Stage‑1 ingest/parse. It:

1) **Removes site chrome and cruft** from per‑page content (scripts, styles, nav, footers, cookie banners, tracking, inline CSS, layout‑only HTML).
2) **Preserves layout metadata** separately (`sources/<slug>/dom_map.json`, `sources/<slug>/asset_manifest.json`).
3) **Normalizes narrative** to `narrative_md` and reference lists to structured arrays.
4) **Writes/overwrites** `content/**` and `public_assets/**` in a controlled way.
5) Supports a **single command** to run the full pipeline end‑to‑end with safety options.

> Stage‑1 artifacts (from the first dev instructions) remain the source of truth for provenance.

---
## 0) Inputs → Outputs (recap)
**Input:** `incoming/` exports → `sources/<slug>/raw.html`, `styles/`, `assets/`, `asset_manifest.json`, `dom_map.json`.

**Output:**
- `content/research/<slug>.json` (or other type) with: envelope, `summary`, `narrative_md`, `sections`, `provenance`, `figure_assets`.
- `public_assets/<slug>/*` (images/PDFs), paths referenced as `/assets/<slug>/…`.
- `jobs/search-index.json`, `jobs/redirects.csv` (via jobs step).

---
## 1) What to REMOVE from source pages
Removal is **non‑destructive** to provenance: raw HTML is kept in `sources/<slug>/raw.html`.

**Always remove:**
- `<script>` tags and inline JS (analytics, Squarespace packs, UI widgets).
- `<style>` tags, inline `style="…"` attributes, font imports.
- Global navs/footers, cookie banners, newsletter/CTA popups, login bars.
- Page chrome: headers, sidebars, breadcrumbs, share buttons, comments widgets.
- Tracking pixels, iframes used for analytics, A/B test beacons.
- Empty/whitespace wrappers, divs that only control grid/columns.

**Keep (but normalize):**
- **Main narrative** text, headings (`h1–h3`), paragraphs, lists, quotes, simple tables.
- **Figures** (img + caption). Store image assets in `public_assets/<slug>/…` and keep captions in content or `asset_manifest.json`.
- **Reference sections**: Introductions, Research, Policy, Media Coverage (convert to arrays of objects).

**Spatial structure:** do **not** bake coordinates into `content/*.json`. Keep them in `sources/<slug>/dom_map.json`.

---
## 2) Stage‑2 Cleanup Algorithm

1. **DOM isolate** — Identify content root (heuristics + rules):
   - Prefer a container with highest text density near first `h1`.
   - Exclude elements matching denylist selectors (configurable):
     - `header, footer, nav, .site-nav, .global-nav, .footer, .cookie, .banner, .newsletter, .signup, .modal, .share, .breadcrumbs`
     - `.sqs-block-button, .sqs-block-social, .sqs-video-wrapper, .sqs-gallery-controls`
   - Keep a copy of rejected selectors in `orchestrator/state/<slug>.json` under `rejected_nodes` (counts only).

2. **Strip style/script** — Remove `<script>`, `<style>`, `link[rel=stylesheet]`, and inline `style` attributes.

3. **Flatten layout** — Collapse single‑child wrappers; convert remaining semantic blocks to Markdown:
   - `h1–h3`, `p`, `ul/ol/li`, `blockquote`, `table` (basic), `figure/figcaption`.

4. **Image handling** — For each `<img>` in content root:
   - Resolve to local path via `asset_manifest.json`.
   - Write `/assets/<slug>/…` path into Markdown image links.
   - If caption exists (or `alt`), append as italic caption line beneath the image in Markdown.

5. **Section extraction** — Detect headings for **Introductions**, **Research**, **Policy Statements**, **Media Coverage** (case/space tolerant). Convert listed links into structured arrays with `{title, authors|outlet, pub, date|year, url}`.

6. **Summarize** — If no `summary` exists, generate 1–2 sentences via GPT (temperature 0), store in envelope.

7. **Assemble content JSON** — Envelope + `narrative_md` + `sections` + `provenance` + `figure_assets`.

8. **Validate** — JSON Schema; word‑count ±40%; link count ±20%; internal asset existence.

9. **Write** — Save to `content/**`. Copy assets to `public_assets/<slug>/…` (content‑addressed names allowed).

---
## 3) CLI — One Command Pipeline

Provide a single top‑level command that runs **Stage‑1 → Stage‑2 → Jobs**. Example (Python `typer`):

```bash
# Full pipeline (all new/changed sources)
factory run all \
  --from INGESTED \
  --to INDEXED \
  --concurrency 4 \
  --replace existing \
  --snapshot
```

### Flags
- `--from/--to` — state boundaries (default INGESTED→INDEXED).
- `--concurrency N` — parallel workers (default 4).
- `--replace existing` — allow overwriting existing `content/**` & `public_assets/**`.
- `--dry-run` — simulate; write reports only (no file changes).
- `--snapshot` — before overwriting, create a **content snapshot** in `dist/content-<timestamp>-pre/` with a manifest, so you can roll back.
- `--limit K` — process only first K slugs (useful for testing).

### Safety notes
- **Overwriting is dangerous** without snapshots. Keep `--snapshot` ON by default in CI.
- The orchestrator should refuse `--replace` if `--snapshot` is not set (unless `--force` is present).
- Always write a run report to `jobs/reports/<date>/run.json` with counts, changed slugs, and any quarantined items.

---
## 4) Replacement Semantics
- **Content files**: Overwrite atomically (write temp file → fsync → rename). Keep previous version in snapshot folder.
- **Assets**: Use content‑addressed filenames (sha256 in name) when possible. If not, overwrite with timestamped backup in `public_assets/.bak/<timestamp>/<slug>/…`.
- **Search index/redirects**: Regenerate in full each run.

---
## 5) Configuration
- Denylist selectors, word/link thresholds, and model choices are in `config/cleanup.yml` and `config/llm.yml`.
- Taxonomy enforcement controlled by `config/validation.yml`.

Example `config/cleanup.yml`:
```yml
content_root_hint: "#page, main, .main-content, .sqs-layout"
denylist:
  - header
  - footer
  - nav
  - .site-nav
  - .global-nav
  - .footer
  - .cookie
  - .banner
  - .newsletter
  - .signup
  - .modal
  - .share
  - .breadcrumbs
  - .sqs-block-button
  - .sqs-block-social
  - .sqs-video-wrapper
  - .sqs-gallery-controls
summarize_if_missing: true
```

---
## 6) Developer Workflow
1. Drop new pages into `incoming/`.
2. `factory ingest add …` (or `factory run all` directly; ingest will be auto‑invoked).
3. Inspect `orchestrator/state/*.json` and the **debug HTML** under `jobs/debug/` if needed.
4. When satisfied, re‑run with `--replace existing --snapshot` to write the cleaned `content/**`.
5. Open the renderer preview (Astro/Next) and verify.

---
## 7) Known Risks & Mitigations
- **Accidental content loss** → Mitigate via snapshots & atomic writes; never delete `sources/**`.
- **Selector drift** (denylist misses new Chrome) → Keep denylist in config and expand via PRs.
- **Layout‑dependent meaning** → Use `dom_map.json` to detect figures adjacent to text; if adjacency is ambiguous, add a warning.
- **LLM variability** → Temperature 0, prompt hashing, artifact logging, and caching.

---
## 8) Acceptance Criteria for Stage‑2
- Content JSON validates against schema.
- All image references resolve under `/assets/<slug>/…`.
- Narrative word count within ±40% of source content region.
- Reference lists extracted and de‑duplicated; at least one section non‑empty.
- Snapshot created when overwriting existing files.

---
## 9) Examples
**Run everything for the first 50 items, simulate only:**
```bash
factory run all --limit 50 --dry-run
```

**Run full batch with overwrite + snapshot:**
```bash
factory run all --replace existing --snapshot
```

**Rebuild a single slug to INDEXED:**
```bash
factory run ending-pandemics --to INDEXED --replace existing --snapshot
```
