# Kaelindor Campaign Knowledge Base

A single-source-of-truth knowledge base + generated wiki for the *Kaelindor* D&D campaign
(setting: Valenya / the Lands of the Valenwyr).

This repository does three jobs:

1. **Agent-queryable KB** — the `kb/` markdown files are structured so an AI agent (Claude)
   can answer natural-language questions: *"what's the progress on finding the source of the
   Uthrel?"*, *"what's the significance of this NPC?"*, *"we're in Greymere — what should we do?"*
   See `CLAUDE.md` for the query contract.
2. **Human wiki** — `py generator/build.py` renders `kb/` into a searchable static HTML site
   in `site/`, with Characters / Locations / Quests / Factions / Items / Lore / Sessions
   sections and client-side keyword search. Deploys to any static host (GitHub Pages).
3. **Session ingestion** — the `/session-ingest` skill (`.claude/skills/session-ingest/`)
   consumes a Whisper transcript, separates in-game canon from table chatter, updates the KB,
   regenerates the wiki, and writes prose session notes matching `style/session-notes-style.md`.

## Layout

| Path | What it holds |
|------|---------------|
| `kb/characters/` | One file per PC / NPC |
| `kb/locations/`  | Towns, regions, dungeons, landmarks |
| `kb/quests/`     | Missions / plot threads, with progress logs |
| `kb/factions/`   | Churches, orders, nations, groups |
| `kb/items/`      | Notable objects |
| `kb/lore/`       | World concepts (gods, the Uthrel, Horizon Doors, history) |
| `kb/sessions/`   | One canon recap per session |
| `kb/index.md`    | Campaign overview / table of contents |
| `notes/`         | Human-readable prose session notes |
| `style/`         | The session-notes style ruleset |
| `generator/`     | The Python static-site generator |
| `transcripts/`   | Drop raw Whisper transcripts here for ingestion |

## Building the wiki

```sh
py generator/build.py        # reads kb/, writes site/
```

Then open `site/index.html`, or deploy `site/` to a static host.

## Deploying to GitHub Pages

A GitHub Action (`.github/workflows/deploy.yml`) builds the wiki and publishes it on every push
to `main` — you only ever commit the `kb/` markdown; the built `site/` is regenerated in CI (and
is gitignored locally). To enable it on a new repo: push to `main`, then in **Settings → Pages**
set **Source = GitHub Actions**. The site URL appears in the Action's deploy step.

> ⚠️ This wiki is single-view and includes DM-only secrets. A **public** Pages site is readable
> by anyone (and search-indexed). Keep the repo private, or strip secrets, if that's a concern.

## Conventions

- **IDs**: every entity file's `id` frontmatter is the kebab-case of its canonical name
  (e.g. `caspian-talon`, `the-uthrel`, `greymere`). The filename matches the id.
- **Cross-links**: reference other entities in prose with `[[id]]` or `[[id|display text]]`.
  The generator resolves these to links; the agent follows them to answer relationship queries.
- See `SCHEMA.md` for the full frontmatter spec per entity type.
