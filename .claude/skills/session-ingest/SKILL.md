---
name: session-ingest
description: >-
  Ingest a D&D session transcript (e.g. a Whisper transcription) into the Kaelindor knowledge
  base. Separates in-game canon from out-of-game table chatter, then produces two artifacts:
  (1) KB + wiki updates (new/updated entity files, quest progress, a session recap, regenerated
  HTML), and (2) prose session notes matching style/session-notes-style.md. Use whenever a new
  session recording/transcript needs to be turned into canon + notes.
---

# Session Ingest

Turn a raw session transcript into canon. Run this from the repo root
(`C:\Users\jake.savage\Documents\dnd-kb`). Read these first if not already in context:
`SCHEMA.md` (entity frontmatter), `CLAUDE.md` (query contract + conventions),
`style/session-notes-style.md` (the prose voice), and skim `kb/` to know the canonical ids.

## Inputs
- A transcript file (usually in `transcripts/`), or pasted transcript text.
- The session's real-world date (ask if not given) and, if known, the in-world date.

## Procedure

### 1. Orient
- Read the transcript fully.
- Determine the new session id: the next number after the latest `kb/sessions/ch02-sNN.md`
  (the campaign is currently in Chapter 2). If the user says a new chapter has started, begin
  `ch03-s01`. Confirm the number if ambiguous.

### 2. Classify in-game vs out-of-game
Split the transcript into **canon** and **chatter**. Treat as **out-of-game** (exclude from canon):
rules/mechanics debate, dice talk, scheduling, snacks/breaks, real-world tangents, meta-discussion
about the game, and player names used out-of-character. Treat as **in-game canon**: what the
characters say/do/discover in the fiction, NPC dialogue and actions, locations entered, items
gained/lost, and information learned. When a passage is ambiguous (e.g. a player reasoning aloud
"in character"), prefer canon if it reflects a character's intent, chatter if it's purely tactical.
Keep a short list of judgment calls to report.

### 3. Extract canon into KB updates
Working only from the canon material, and conforming to `SCHEMA.md` and the **existing canonical
ids** (reuse ids — never duplicate an entity under a new spelling; normalise per
`style/session-notes-style.md`):
- **New entities**: create `kb/<type>/<id>.md` for any new character, location, faction, item, or
  lore concept introduced. Filename = id (kebab-case of canonical name).
- **Updated entities**: amend existing files — add to a character's `## Appearances`, update
  `status`/`last_session`, add newly-revealed detail or DM secrets.
- **Quests**: for every quest touched, append a dated bullet to its `## Progress log`
  (`- S2.NN: …`), update `status`, bump `last_updated_session`, and refresh `## Open threads` /
  `## Leads / next steps`. Open a new `kb/quests/` file for any new thread.
- Use `[[id]]` cross-links throughout. Do **not invent canon** — if the transcript doesn't
  establish something, leave it unknown.

### 4. Write the session recap (canon)
Create `kb/sessions/ch0X-sNN.md` per the `session` schema: frontmatter
(`id, type, chapter, number, title, date_real, date_inworld, characters, locations, quests,
summary`) and body `## Recap` (third-person present-tense canon narrative), `## Key facts learned`,
`## Threads opened / advanced`. This is canon-only — no table chatter.

### 5. Write the prose session notes (style artifact)
Create `notes/session-NN.md` written to **every rule in `style/session-notes-style.md`**:
third-person present tense, `Session NN - DD/MM/YYYY` heading + in-world date line, location/
character sub-headers, the colon-then-bullets "facts learned" device, reported speech, compressed
combat, the established character humour. This is the human-readable telling — richer in voice than
the KB recap, and it may keep a little dry flavour, but still no out-of-game logistics.

### 6. Regenerate the wiki
Run `py generator/build.py`. Confirm the build reports **"All wikilinks resolved."** If there are
unresolved `[[links]]`, fix them (usually a typo'd id or an entity you should create) and rebuild.

### 7. Report for review — do not finalise silently
Summarise for the user before considering the ingest done:
- The session id/title and one-line summary.
- New entities created and existing entities changed (a short diff).
- Quest progress applied.
- The in-game / out-of-game judgment calls you made (so they can correct mis-classifications).
- Confirmation the wiki rebuilt cleanly, and the path to `notes/session-NN.md`.

Offer to adjust classification or detail. Only commit/publish if the user asks.

## Cautions
- Reuse canonical ids; normalise spelling variants. When unsure an entity already exists,
  search `kb/` before creating a new file.
- Keep every `summary` to one sentence.
- Preserve in-world uncertainty — record what the party *believes* vs what is *confirmed*.
- If the transcript is long, work in passes (orient → classify → extract → write) rather than
  one giant pass, and keep the canonical-id list handy to avoid duplicates.
