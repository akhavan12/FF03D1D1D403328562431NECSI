# NECSI Content Foundry (Factory)

This is the "GPT-in-a-program" pipeline to migrate and maintain NECSI’s research & education corpus as structured content, as specified in `dev_instructions.md`.

## Quick start

1. Create a virtual environment (Python 3.11+ recommended) and install dependencies:

```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Copy environment example and edit as needed:

```
cp config/.env.example .env
```

3. Run the CLI:

```
python -m necsifactory.cli --help
```

## Layout

See `Factory/dev_instructions.md` for the detailed design. This repo includes the following top-level directories:

- `necsifactory/` Python package
- `ingest/`, `normalize/`, `prompts/`, `schemas/`, `taxonomy/` definitions
- Generated outputs go to `content/`, `public_assets/`, and `jobs/`

## Notes

- All commands are currently placeholders. They create and update state files under `orchestrator/state/` and validate basic inputs.
- Schemas live in `schemas/` and taxonomy in `taxonomy/`.
