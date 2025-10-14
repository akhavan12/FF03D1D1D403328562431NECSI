# NECSI Content Foundry — Developer Instructions

_AKA: “GPT-in-a-program” pipeline to migrate and maintain NECSI’s research & education corpus as structured content._

## 0) Goals
- Convert legacy Squarespace/HTML/WebArchive pages into **versioned structured content** (JSON/MD + assets) without manual page-building.
- Keep the pipeline **separate** from renderers (NECSI site, overlays, search). Treat output as a **data product**.
- Be **idempotent**, **auditable**, and **extensible** (can re-run, diff, roll back; easy to add new collections like Evolution Ed.).

---
## 1) Top-level layout (in this `r/Factory/` component)
```
r/Factory/
  orchestrator/            # CLI/API; state machine; job runner
  ingest/                  # unarchivers, HTML fetchers/parsers, link mapping
  normalize/               # HTML→schema; GPT-assisted transformers; validators
  prompts/                 # LLM prompt templates + tests
  schemas/                 # JSON Schema / Zod definitions for content
  taxonomy/                # controlled vocabularies (categories, tags)
  content/                 # GENERATED structured content (JSON/MD)
  public_assets/           # GENERATED assets (images, PDFs) (or mirror to S3)
  jobs/                    # search indexer, link checker, redirects builder
  scripts/                 # one-off utilities (e.g., webarchive extractor)
  config/                  # .env, provider keys, rate limits, source mappings
  tests/                   # unit/integration tests
  docs/                    # design notes, runbook, ADRs
```
> **Note:** Renderers live elsewhere (e.g., `necsi-site/`). They consume `content/`, `public_assets/`, and artifacts from `jobs/`.

---
## 2) Content model (schemas)
All content items carry a shared envelope and a type-specific body.

### 2.1 Shared envelope
```json
{
  "schema_version": 1,
  "type": "research" | "course" | "lesson",
  "slug": "ending-pandemics",
  "title": "Ending Pandemics",
  "summary": "In the era of global connectivity…",
  "categories": ["Health", "Policy"],
  "tags": ["pandemics", "Ebola", "community-screening"],
  "hero_image": "ending-pandemics/hero.jpg",
  "provenance": {
    "source_url": "https://necsi.edu/research/ending-pandemics",
    "capture_method": "webarchive|html|xml",
    "captured_at": "2025-09-04T00:00:00Z",
    "checksum": "sha256:…"
  }
}
```

### 2.2 Research body
```json
{
  "type": "research",
  "narrative_md": "# Overview\n…main body in Markdown…",
  "sections": {
    "introductions": [
      {"title": "How community response stopped Ebola", "authors": ["Y. Bar-Yam"], "pub": "NECSI", "date": "2016-07-11", "url": "…"}
    ],
    "research": [
      {"title": "Long-range interaction and evolutionary stability in a predator–prey system", "authors": ["E.M. Rauch", "Y. Bar-Yam"], "pub": "Phys. Rev. E 73:020903", "year": 2006, "url": "…"}
    ],
    "policy_statements": [
      {"title": "Stopping hospital acquired infections…", "authors": ["Y. Bar-Yam"], "pub": "NECSI", "date": "2016-07-24", "url": "…"}
    ],
    "media_coverage": [
      {"title": "Did Authorities Use the Wrong Approach to Stop Ebola?", "outlet": "TIME", "author": "A. Sifferlin", "date": "2014-…", "url": "…"}
    ]
  },
  "figure_assets": ["ending-pandemics/map-liberia.png"]
}
```

### 2.3 Course body (Education)
```json
{
  "type": "course",
  "delivery": {"format": ["prerecorded", "live-qna"], "duration_days": 12},
  "sessions": [
    {"title": "Part 1: Introduction to Complex Systems", "length": "55:19"},
    {"title": "Part 2: Self-Organization of Patterns of Behavior", "length": "1:20:16"}
  ],
  "schedule": {"start": "2025-06-09", "end": "2025-06-20"},
  "tuition_tiers": [
    {"audience": "Corporate", "price": 978},
    {"audience": "Government/NGO", "price": 808},
    {"audience": "Individual", "price": 765},
    {"audience": "Student/Academic", "price": 638, "note": "*.edu email"}
  ],
  "scholarship": {"text_md": "To apply for a scholarship, click here.", "url": "…"},
  "contact": {"email": "programs@necsi.edu", "phone": "+1-617-547-4100"}
}
```

### 2.4 Lesson body (Evolution education)
```json
{
  "type": "lesson",
  "audience": "High School",
  "objectives_md": "…",
  "materials": ["pdfs/worksheet-1.pdf", "slides/intro.pptx"],
  "activities_md": "…",
  "assessments_md": "…",
  "teacher_notes_md": "…",
  "downloads": [{"label": "Student Packet", "path": "evolution/lesson-01/packet.pdf"}]
}
```

---
## 3) Controlled vocabulary (taxonomy)
`taxonomy/categories.json`, `taxonomy/tags.json`
- **Categories**: small, curated set (`Health`, `Economy`, `Biology`, `Methods`, `Policy`, `Education`).
- **Tags**: larger controlled list (`pandemics`, `Ebola`, `Zika`, `financial-crisis`, `ethnic-violence`, `multiscale`, `scaling`, `universality`, `agent-based`, `cellular-automata`, `precautionary-principle`, …).
- The normalizer must **map synonyms→controlled tag**. Unknown tags are rejected unless added via PR.

---
## 4) Orchestrator — state machine
States (per page):
```
INGESTED → PARSED → NORMALIZED → SCHEMA_VALID → BUILT → INDEXED
             ↘─────────────┬────────────↗
                  QUARANTINED (with reason)
```
Transitions:
- **INGESTED**: raw file(s) present (html, webarchive, xml).
- **PARSED**: DOM extracted, sections detected, links enumerated.
- **NORMALIZED**: narrative to Markdown, references to objects, tags inferred.
- **SCHEMA_VALID**: JSON Schema passes; required fields present.
- **BUILT**: content written to `content/…`, assets copied to `public_assets/…`.
- **INDEXED**: search index updated; redirects generated.
- **QUARANTINED**: rule violation (e.g., missing title, huge content delta, empty sections).

Artifacts per state:
- `orchestrator/state/<slug>.json` (status, timestamps, checksums, diffs)

---
## 5) CLI commands (examples)
```
# ingest
factory ingest add incoming/ending-pandemics.webarchive --slug ending-pandemics

# parse + normalize + validate (single item)
factory run ending-pandemics --to SCHEMA_VALID --open-diff

# batch run (all new items)
factory batch run --from INGESTED --to BUILT --limit 100

# build search index + redirects
factory index build
factory redirects build --legacy-map data/legacy_urls.csv

# verify external links
factory links check --concurrency 8 --timeout 8000

# report
factory report --since 7d --by-state
```

---
## 6) Normalization (Rules first, then GPT)
1. **Rules:**
   - Extract `<title>`, `h1…h3`, paragraphs, lists, tables.
   - Identify known block labels: `Introduction`, `Research`, `Policy`, `Media` (case-insensitive).
   - Pull link text + href + inferred metadata (outlet, year).
2. **GPT passes:**
   - `html_to_markdown`: clean Markdown without layout cruft.
   - `extract_citations`: return arrays for each section with fields normalized.
   - `summarize_page`: 1–3 sentence summary.
   - `infer_tags`: from body + links → controlled tags (reject OOV).
3. **Validation:** JSON Schema; word-count delta vs source (±40%); link count delta (±20%).

Prompt inputs must include: the controlled taxonomy, schema shape, and examples. Keep temperature low (≤0.2).

---
## 7) Validation rules (hard failures)
- Missing `title`, `slug`, `narrative_md` (<200 chars), or **all** reference sections empty.
- Tags outside controlled vocabulary.
- Dead internal links (to other migrated slugs) unresolved.
- Asset missing for declared `hero_image`.

Warnings (non-blocking):
- >40% word-count delta vs source; >20% link delta; date parsing fallbacks.

---
## 8) Jobs (post-build)
- **Search indexer** → `jobs/search-index.json` (title, summary, tags, first 2k chars, slug).
- **Redirects builder** → `jobs/redirects.csv` (legacy_url, new_slug).
- **Link checker** → reports to `jobs/reports/links-YYYYMMDD.json`.

---
## 9) CI/CD
- Any commit to `content/` triggers renderer preview (separate repo).
- Batches produce immutable artifact: `dist/content-<hash>.tar.gz` + `search-index.json` + `redirects.csv`.
- Renderer pins content by hash for deterministic builds and easy rollbacks.

---
## 10) Runbook (migration)
1) **Decide scope for Batch 1** (e.g., 50 research pages + the core course page).
2) **Export** legacy pages (WebArchive/HTML/XML) into `incoming/`.
3) Run `factory batch run …` to `BUILT`.
4) Preview in renderer; fix quarantined items (adjust rules or add taxonomy entries via PR).
5) Publish preview; collect feedback; iterate.
6) Repeat batches until coverage target.

Freeze legacy edits during cutover week; then switch DNS and enable redirects.

---
## 11) Security & provenance
- Content commits via PR only; require reviews for schema/taxonomy changes.
- Store source checksums and capture timestamps.
- Optionally mirror `public_assets/` to S3/GCS with content-addressed paths.

---
## 12) Notes & extensions
- Add a `collections/` field if we later need curated bundles (e.g., “Pandemics Toolkit”).
- Add `related_slugs` for manual curation beyond tag-based related items.
- Optional embeddings build for semantic search (separate job).

---
## 13) Minimal renderer contract
Renderers should assume:
- `content/**.json|md` with envelope + body (as above).
- `jobs/search-index.json` for site search.
- `jobs/redirects.csv` to configure path redirects.
- Assets live under `/assets/<slug>/…` with the same relative paths referenced in content.


## Addendum:

Let’s preserve the original layout metadata and make it available to the builder. Here’s how to bake that into the factory, without changing your authored content:

What we’ll capture from each source page
	•	Raw source bundle:
sources/<slug>/raw.html, sources/<slug>/styles/*.css, sources/<slug>/assets/*
	•	Asset manifest (sources/<slug>/asset_manifest.json):
Maps original URLs → new hashed asset paths, plus {mime,size,sha256,original_url,alt,caption}.
	•	DOM map (sources/<slug>/dom_map.json):
A structured list of blocks in reading order with their selectors and (if rendered) coordinates:

{
  "viewport": {"width": 1366, "height": 900, "user_agent": "…"},
  "blocks": [
    {
      "role": "heading|paragraph|figure|list|quote|table|code",
      "selector": "#main > h1",
      "order": 10,
      "text_hash": "sha256:…",
      "chars": {"start": 0, "end": 57},
      "bbox": [x,y,w,h],
      "classes": ["hero","title"],
      "asset_ref": null
    },
    {
      "role": "figure",
      "selector": "figure#liberia-map",
      "order": 120,
      "bbox": [x,y,w,h],
      "asset_ref": "public/assets/ending-pandemics/liberia-map.png",
      "caption": "Liberia caseload by county…"
    }
  ]
}

The bbox is captured by rendering with a headless browser so we preserve on-page positioning.

Where this shows up in the content JSON (non-destructive)

Add optional fields (templates can ignore or use them):

{
  "source_paths": {
    "html": "sources/ending-pandemics/raw.html",
    "dom_map": "sources/ending-pandemics/dom_map.json",
    "asset_manifest": "sources/ending-pandemics/asset_manifest.json"
  },
  "source_layout": {
    "reading_order": ["#main > h1", "p.lede", "figure#liberia-map", "h2#intro", "p:nth-of-type(1)"],
    "blocks": "inline ref to dom_map.json (or duplicated for convenience)"
  }
}

Ingest/normalize changes (concrete)
	•	Ingest
	•	Save raw HTML/CSS/assets exactly as downloaded.
	•	Compute asset_manifest.json.
	•	Parse
	•	Build a DOM and reading-order list (content flow, not just DOM tree).
	•	Render
	•	Use headless Chromium (fixed viewport) to compute bbox for each block and figure.
	•	Normalize
	•	Generate narrative_md and structured sections without losing the dom_map.
	•	Link images in Markdown to the new asset paths from asset_manifest.
	•	Validate
	•	Check that every referenced image in Markdown has a corresponding asset_ref entry.

Developer ergonomics
	•	Debug page generator: /jobs/debug/<slug>.html that overlays the dom_map on a screenshot so you can visually verify block order/positions.
	•	Reproducibility: include viewport, UA string, and CSS hash in dom_map.json.
	•	Privacy: never store absolute local file paths; only repo-relative paths and original URLs.

Directory snippet (r/Factory/)

incoming/
sources/
  ending-pandemics/
    raw.html
    styles/
    assets/
    asset_manifest.json
    dom_map.json
content/
  research/ending-pandemics.json
public_assets/
  ending-pandemics/…
jobs/
  debug/ending-pandemics.html

If you want, I can add these fields and the new folders to dev_instructions.md so it’s canonical, plus a tiny spec for the headless renderer (viewport, throttling, retries).

#  Questions about NECSI Content Foundry (Factory)

Orchestrator implementation
Language/runtime preference for orchestrator/ and CLI? Node/TypeScript, Python, or something else?
State storage format for orchestrator/state/<slug>.json: single file per slug (as specified) vs. an index? Any concurrency requirements?
Schemas and validation
Preferred schema system: JSON Schema only, or Zod (TypeScript) as the source of truth with JSON Schema generated?
Schema evolution: how do you want to manage schema_version bumps and migration scripts?
Taxonomy governance
Location and process: should taxonomy/categories.json and taxonomy/tags.json be enforced via PRs in this repo?
Synonym mapping: do you want a taxonomy/synonyms.json and a rule that rejects unmapped synonyms?
Normalization and GPT passes
Model and provider: OpenAI GPT-4o/4.1/mini, or Anthropic/other? Any existing API keys or provider preferences?
Rate limits and cost controls: desired concurrency, backoff policy, and caching of LLM results?
Determinism: should we pin prompts and set temperature ≤ 0.2 everywhere, as stated, and store prompt+response artifacts for audit?
Content and assets
Output formats: Do you want both JSON and MD for narrative (narrative_md) or JSON-only with embedded MD strings?
Asset paths: confirm canonical path scheme under public_assets/ and whether to mirror to /assets/<slug>/… at render time or pre-bake that path in output.
Checksums: preferred checksum algorithm (looks like sha256), and do you want to store both source and built artifact checksums?
Validation and quarantine
The word-count ±40% and link ±20% thresholds: should these be configurable per collection?
Quarantine triage: do you want an issue to be filed automatically (e.g., in jobs/reports/) with diffs and reasons?
Jobs and CI/CD
CI provider preference (GitHub Actions, GitLab CI, etc.)?
Artifact storage: where to publish dist/content-<hash>.tar.gz, search-index.json, and redirects.csv? Git LFS, S3, or release assets?
Renderer integration: confirm that Factory/ and necsi-site/ are separate repos, with the renderer consuming versioned artifacts by hash.
Redirects and link checking
jobs/redirects.csv: any required columns beyond (legacy_url, new_slug)? e.g., HTTP status code?
Link checker behavior: retries, per-domain rate limits, and whether to allow-list domains with flaky uptime.

---
## Decisions & Defaults (Initial Answers)

These defaults unblock implementation now; we can revise via ADRs/PRs.

### Orchestrator
- **Language/runtime:** Python 3.11+
- **CLI:** `typer` + `rich`
- **State storage:** Per-slug file at `orchestrator/state/<slug>.json` (authoritative) **and** generated index `orchestrator/state/_index.json` for fast scans.
- **Concurrency:** Per-slug lockfiles (`orchestrator/state/<slug>.lock`). Batch workers run N in parallel (configurable), never the same slug simultaneously.

### Schemas & Validation
- **Source of truth:** JSON Schema.
- **Typed bindings:** Generate Pydantic (factory) and TypeScript types (renderer) from the JSON Schemas.
- **Schema evolution:** Embed `schema_version` in each item. Use SemVer for schemas (MAJOR=breaking, MINOR=additive). Keep migration scripts in `scripts/migrate/`; orchestrator auto-runs migrations for older versions.

### Taxonomy Governance
- Files: `taxonomy/categories.json`, `taxonomy/tags.json`, `taxonomy/synonyms.json`.
- Policy: PRs required for changes. CI enforces that all content tags map to controlled tags or synonyms. Unmapped tags are rejected.

### Normalization & GPT Passes
- **Provider/models:** OpenAI GPT‑4.1 (extraction/structuring) and GPT‑4.1‑mini (summaries/tagging). Optional Claude 3.5 Sonnet behind a feature flag.
- **Determinism & audit:** `temperature=0`, `top_p=0.1`. Persist prompt template, input hash, model name, and raw response under `artifacts/<slug>/<stage>/…`. Cache keyed on `(model, prompt_version, input_sha256)`.
- **Rate limits & cost controls:** Concurrency=4 LLM calls; exponential backoff with jitter (max 3 retries). Per‑batch budget cap (default `$25`)—on exceed, QUARANTINED with reason.

### Content & Assets
- **Outputs:** Canonical JSON with `narrative_md` (string). Optionally emit sibling `.md` for human edits; JSON remains authority.
- **Asset paths:** Prebake to `public_assets/<slug>/…` and reference as `/assets/<slug>/…` in content.
- **Manifests/layout:** Always write `sources/<slug>/asset_manifest.json` and `sources/<slug>/dom_map.json`.
- **Checksums:** sha256 for both source inputs and built assets; store in provenance + manifest.

### Validation & Quarantine
- Thresholds: word count ±40%, link count ±20% vs. source. Configurable per collection in `config/validation.yml`.
- Quarantine: move to `quarantine/<slug>/…` and write machine‑readable report to `jobs/reports/<date>/<slug>.json` (reasons, diffs). Optional GitHub issue creation toggle.

### Jobs & CI/CD
- **CI provider:** GitHub Actions (lint, test, batch, build artifacts).
- **Artifacts:** `dist/content-<hash>.tar.gz`, `jobs/search-index.json`, `jobs/redirects.csv`.
- **Storage:** Prefer S3/GCS with versioning; GitHub Releases acceptable for small scale.
- **Renderer integration:** `Factory/` and `necsi-site/` are separate repos; renderer consumes artifacts by **content hash**.

### Redirects & Link Checking
- `jobs/redirects.csv` columns: `legacy_url`, `new_slug`, `http_status` (default 301), `notes` (optional).
- Link checker: 3 retries with exp backoff; per‑domain QPS=2; timeout=8s; treat 429 as retryable; allow‑list flaky domains (warn on intermittent 5xx/timeouts).

### Inputs & Sources (clarification)
- **Incoming folder:** Raw exports go in `r/Factory/incoming/` (human drop zone).
- **Source preservation:** On ingest, copy to `sources/<slug>/` and generate `asset_manifest.json` + `dom_map.json`.

### Directory recap (with inputs)
```
r/Factory/
  incoming/                      # raw webarchive/html/xml
  sources/
    <slug>/
      raw.html
      styles/
      assets/
      asset_manifest.json
      dom_map.json
  orchestrator/
    state/
      <slug>.json
      _index.json
  content/
    research/<slug>.json
    education/courses/<slug>.json
  public_assets/
    <slug>/…
  jobs/
    search-index.json
    redirects.csv
    reports/<date>/<slug>.json
  artifacts/<slug>/<stage>/…
```
