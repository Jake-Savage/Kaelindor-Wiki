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

## Canon fidelity rules — READ FIRST, they override convenience

The single biggest risk in this job is **writing more than the transcript actually established** —
turning a guess into a fact. Past ingests inverted who-did-what, promoted a character's suspicion
into stated truth, invented causal links, and merged unrelated mysteries. Hold to these five guards
on **every** sentence you write into the KB:

- **G1 — Confirmed vs. claimed.** Only state as fact what the fiction establishes as fact (shown
  on screen, or stated plainly by the narration/world). A character's belief, accusation, theory,
  or a rumour is **attributed and hedged** — *"Bartholomew believes Torston was behind it,"*
  *"the party suspects,"* *"rumoured — and he denies it"* — never written flat. The highest-risk
  cases are **villain guilt, secret identities, hidden motives, and causes**: default these to
  attributed/suspected unless the transcript confirms them.
- **G2 — Direction of action.** For any "A did X to B," name the actor and the target explicitly
  and re-check the transcript wording before writing. (Canonical cautionary tale: *Lucien released
  Caspian*, not the reverse.)
- **G3 — No invented links.** Do not connect two people, groups, or events causally unless the
  transcript states the link. Proximity and coincidence are not causation. (e.g. the gate-tamperer
  is **not** automatically whoever else is nearby and suspicious.)
- **G4 — Keep unknowns separate.** Do not fuse two distinct open mysteries into one tidy
  explanation. Two unexplained things stay two unexplained things until the source connects them.
- **G5 — Don't manufacture DM secrets.** You record what the table *established or witnessed*; you
  do **not** decide hidden truths the players haven't earned. Anything that reads like a concealed
  truth (a true culprit, a secret allegiance, a real parentage) → record only the **evidence** and
  put the conclusion in the confirmation ledger (Step 8) for the DM to rule on.

Express confidence in **prose** (hedging words + attribution) and in the `## Open threads` /
`## DM notes` sections — do not invent new frontmatter fields. When the source is silent, the
correct output is an **open thread**, not an assertion.

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
Split the transcript into **canon** and **chatter**. Out-of-game (exclude): rules/mechanics debate,
dice talk, scheduling, breaks, real-world tangents, meta-discussion, player names used
out-of-character. In-game canon: what the characters say/do/discover, NPC dialogue and actions,
locations entered, items gained/lost, information learned. When a passage is ambiguous, prefer canon
if it reflects a character's intent, chatter if it's purely tactical. Keep a short list of the
judgment calls you made.

### 3. Extract canon into KB updates — with an evidence trail
Working only from canon material, conforming to `SCHEMA.md` and the **existing canonical ids**
(reuse ids; never duplicate an entity under a new spelling; normalise per the style ruleset):
- As you draft each non-trivial factual claim, hold its **support** in mind: which transcript
  line(s) establish it, and at what confidence (**confirmed / reported-by-X / suspected / rumoured
  / unknown**). If you can't point to support, it does not go in as fact (apply G1–G5).
- **New entities**: create `kb/<type>/<id>.md` (filename = id, kebab-case of canonical name).
- **Updated entities**: amend files — add to `## Appearances`, update `status`/`last_session`, add
  newly-revealed detail. Put genuinely-shown secrets in `## DM notes / secrets`; put
  suspected/unconfirmed secrets there too **but clearly marked as suspected**, and mirror them into
  the Step 8 ledger.
- **Quests**: for every quest touched, append a dated bullet to `## Progress log` (`- S2.NN: …`),
  update `status`, bump `last_updated_session`, and refresh `## Open threads` / `## Leads`. Unproven
  causes/culprits belong in **Open threads**, phrased as questions. Open a new quest file for a new thread.
- Use `[[id]]` cross-links. **Do not invent canon** — if the transcript doesn't establish it, it's an open thread.

### 4. Verify against the transcript (adversarial self-check) — the key guard
Before writing the recap/notes, re-read the relevant transcript spans and audit your own draft
claims as if trying to **disprove** them. For each new or changed factual statement ask:
- **Is it confirmed, or only claimed/suspected?** If claimed, attribute and hedge it (G1).
- **Did I get the direction right?** Actor vs. target, gave vs. received, detained vs. freed (G2).
- **Did I invent a link or cause** the transcript doesn't state? Cut it or move it to Open threads (G3).
- **Did I merge two separate unknowns?** Split them (G4).
- **Is this a hidden truth I decided rather than the table established?** Downgrade to evidence + flag (G5).
Downgrade or delete anything that fails. List every claim you softened/cut — it feeds Step 8.
(For a high-stakes or contested session you may spawn a subagent to re-verify the draft against the
transcript independently; otherwise do the self-check inline.)

### 5. Write the session recap (canon)
Create `kb/sessions/ch0X-sNN.md` per the `session` schema: frontmatter (`id, type, chapter, number,
title, date_real, date_inworld, characters, locations, quests, summary`) and body `## Recap`
(third-person present-tense, hedged per G1), `## Key facts learned`, `## Threads opened / advanced`.
Canon-only — no table chatter.

### 6. Write the prose session notes (style artifact)
Create `notes/session-NN.md` following **`style/session-notes-style.md`** in full (register,
structure, and what to include/omit live there). Skill-specific reconciliation only: the notes may
analyse and infer more freely than the KB records, but the fidelity rules still bind the structured
KB — a reading the notes carry as "strongly implied" becomes, in a KB entry, a hedged/attributed
claim or an open thread, never an unqualified hard fact (report suspicions as suspicions, per G1).

### 7. Regenerate the wiki
Run `py generator/build.py`. Confirm it reports **"All wikilinks resolved."** Fix any unresolved
`[[links]]` (usually a typo'd id or a missing entity) and rebuild.

### 8. Report + confirmation ledger — do not finalise silently
Summarise for the user, and explicitly surface what needs their ruling:
- Session id/title and one-line summary; new entities created and existing entities changed (a short diff); quest progress applied.
- **In-game / out-of-game judgment calls** (so they can correct mis-classifications).
- **Confirmation ledger** — the heart of the safeguard. List, for the DM to confirm or correct:
  1. **Claims I softened or left as suspected/unknown** (and why), so the DM can *promote* any they
     know to be true.
  2. **Secret-shaped facts** (a true culprit, hidden identity, real motive/parentage, a causal link)
     that the evidence *suggests* but the table didn't confirm — ask outright rather than assert.
  3. Any **who-did-what beat** you're less than certain about (direction, attribution).
- Confirm the wiki rebuilt cleanly and give the path to `notes/session-NN.md`.

Offer to adjust classification or detail, and to **harden** any ledger item the DM confirms. Only
commit/publish if the user asks.

## Cautions
- Reuse canonical ids; normalise spelling variants; search `kb/` before creating a new file.
- Keep every `summary` to one sentence.
- Prefer an honest "unknown / the party suspects" over a confident wrong answer — under-claiming is
  cheap to fix later; a fabricated fact silently becomes canon.
- If the transcript is long, work in passes (orient → classify → extract → verify → write) and keep
  the canonical-id list handy to avoid duplicates.
