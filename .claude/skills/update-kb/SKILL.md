---
name: update-kb
description: >-
  Update the Kaelindor knowledge base from arbitrary text — a lore snippet, a new fact, an
  external document, or a correction/retcon/rename — then rebuild and publish the wiki. Send it
  the text (or a file path) and it ingests it into the markdown KB, rebuilds the site, and commits
  + pushes. Use for non-session updates and fixes (misspelled names, wrong facts, new lore). NOT
  for session transcripts or session notes — use `session-ingest` for those.
---

# Update KB

The write-counterpart to `/codex`, and a lighter sibling of `/session-ingest`: take text (pasted,
or a path to a document) and apply it to the markdown KB in `kb/`, then rebuild and publish the
wiki. **No session recap, no `notes/`, no in-game/out-of-game transcript classification** — this is
for lore, facts, and corrections.

Run from the repo root (`C:\Users\jake.savage\Documents\dnd-kb`).

## Inputs
- **The update text** — pasted, or a path to a document (e.g. a new lore file). It can be new
  information, an expansion, or a correction/retcon/rename.
- **Optional hints** — e.g. "this is DM-only," "rename X to Y," or the source of a lore doc.
  Everything else is derived in pre-flight.

## Procedure

### 1. Pre-flight / orient (do this for the user — don't make them re-explain the project)
Read `SCHEMA.md` (entity frontmatter spec) and `CLAUDE.md` (conventions + query contract), and
survey the canonical ids (glob/grep `kb/`) so the update **reuses existing ids and spellings**
rather than inventing or duplicating. Note the build command (`py generator/build.py`) and its two
gates: **"All wikilinks resolved"** and **"All frontmatter parsed."**

### 2. Determine the update's intent (often a mix)
- **New / expanded info** — lore, an NPC, a place, a faction, an item.
- **Correction / retcon** — a fact change that may ripple across several entries.
- **Rename** — an id or canonical-name change.

### 3. Apply — conforming to `SCHEMA.md` and existing canonical ids
- **New info:** create or extend `kb/<type>/<id>.md` (filename = kebab-case `id`), with `[[links]]`,
  a one-sentence `summary`, and **provenance noted in prose** (e.g. "per the Churches of Kaelindor
  doc," "per the DM, <date>"). Route genuinely DM-only facts into a `## DM notes` section. Reuse an
  existing entity rather than creating a near-duplicate; if unsure it exists, grep `kb/` first.
- **Correction:** locate **every** reference and fix them consistently — grep across `kb/` for the
  term and check frontmatter (`id`, and lists like `connected_to`, `involves_*`, `notable_members`,
  `related`, `affiliations`), `[[links]]`/`[[id|text]]`, and prose. Propagate downstream
  consistency: a retcon may require softening or rewording dependent claims elsewhere (as with the
  Torston / Lucien / Furnace-Brood fixes), not just the one line.
- **Rename (id/name change):** the full sweep — update the frontmatter `id` and `title`, every
  `[[id]]`/`[[id|text]]`, all list references, and prose mentions (mind both casings, e.g.
  `Bridgemarsh`/`bridgemarsh`); then **rename the file** so `filename == id` (use `git mv`). This is
  the `Bridgemarsh→Bridgemarch` procedure.

### 4. Fidelity (the same guards as `session-ingest`, G1–G5)
A **user correction** and an **external lore document** are *authoritative* — apply them as
confirmed fact. But still:
- **G1 — confirmed vs claimed:** don't over-state. If the source itself hedges or only a character
  believes something, keep it attributed/hedged; preserve in-world uncertainty the source leaves open.
- **G2 — direction of action:** get actor vs. target right.
- **G3 — no invented links:** add only the connections the text states; don't infer a cause/identity.
- **G4 — keep unknowns separate:** don't fuse two distinct things into one tidy explanation.
- **G5 — don't manufacture secrets:** record what the source establishes, not a hidden truth you inferred.
- **YAML trap:** never a bare `colon-space` inside a frontmatter scalar (`summary: …: …`) — it
  silently empties the entry's metadata (the Rell-summary bug). Quote the value or use an em-dash.

### 5. Rebuild & verify
Run `py generator/build.py`. Require **both** gates clean — **"All wikilinks resolved"** and **"All
frontmatter parsed."** If either fails, fix it (a typo'd id, a missing entity, or a bad frontmatter
colon) and rebuild before going on. (Read the full build output, not a filtered view.)

### 6. Publish (auto)
Commit and push. Stage **only the files this update touched** (the changed/created/renamed `kb/`
files) with a targeted `git add` — **never `git add -A`**, since another session (e.g. a running
`session-ingest`) may have unrelated in-progress edits in the working tree. Write a descriptive
commit message. If the push is rejected as non-fast-forward, `git fetch` + `git rebase origin/main`
and push again (as when the session-28 transcript landed). End commit messages with the standard
Co-Authored-By line.

### 7. Report a change ledger
Summarise: files created / changed / renamed; new entities and their ids; any `[[links]]` that
broke and were fixed; and **anything ambiguous** — uncertain spellings (especially names you had to
guess), or a correction whose downstream ripple you want confirmed. Offer to adjust or to revert
(git) if anything looks wrong.

## Out of scope (use `session-ingest` instead)
Session recaps (`kb/sessions/`), prose session notes (`notes/`), and in-game/out-of-game transcript
classification. If the input is a session transcript, say so and point to `session-ingest`.

## Cautions
- Reuse canonical ids; normalise spelling variants; grep before creating a new entity.
- Keep every `summary` to one sentence.
- Prefer an honest "unknown / the source doesn't say" over inventing detail to fill a gap.
- Don't touch `notes/` or `kb/sessions/`; this skill is KB + wiki only.
