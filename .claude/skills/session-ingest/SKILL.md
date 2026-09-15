---
name: session-ingest
description: >-
  Ingest a D&D session transcript (e.g. a Whisper transcription) into the Kaelindor knowledge
  base. Separates in-game canon from out-of-game table chatter, then produces two artifacts:
  (1) KB + wiki updates (new/updated entity files, quest progress, a session recap, regenerated
  HTML), and (2) prose session notes matching style/session-notes-style.md. Use whenever a new
  session recording/transcript needs to be turned into canon + notes. Invoked bare, it pulls the
  repo and ingests whatever transcripts the latest transcript-adding commit brought in.
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
- **Nothing.** By default the skill finds its own work: it pulls the repo and ingests the
  transcripts the pull brought in (Step 0). This is the normal invocation.
- Optionally, an explicit transcript file (usually in `transcripts/`) or pasted transcript text —
  give one of these to ingest a specific transcript and **skip Step 0 entirely**.
- The session's real-world date (Step 0 derives it from the filename; ask if it can't) and, if
  known, the in-world date.
- **`dm` (optional but recommended):** which speaker is the Dungeon Master — a diarisation
  label (e.g. `SPEAKER_00`) or a name. Diarisation labels are per-recording, so this is given
  per run — and **per transcript** when Step 0 finds more than one. The DM is a special speaker
  (see Step 2). If omitted, infer the DM (the speaker doing the narration/adjudication) and record
  that assumption in the Step 8 ledger for correction. The same input may carry a speaker→character
  map; the DM is the high-value one — infer the rest.

## Procedure

### 0. Sync and find the transcripts
**Skip this step** if the user handed you a specific transcript path or pasted text — they have
already chosen the input. Otherwise the skill selects its own input, as follows.

**a. Pull.** Check the tree is clean first (`git status --porcelain`); if it is dirty, stop and
report rather than pulling over uncommitted work. Then:

```sh
BEFORE=$(git rev-parse HEAD)
git pull --ff-only
AFTER=$(git rev-parse HEAD)
```

If the pull fails (diverged branch, no upstream, no network), stop and report — do not ingest
against a stale tree without saying so.

**b. Collect candidates.** Transcripts added by the pull:

```sh
git diff --name-only --diff-filter=A "$BEFORE".."$AFTER" -- transcripts/
```

If `BEFORE` = `AFTER` (nothing came down — usually the user already pulled) or that list is empty,
fall back to the **most recent commit that added a transcript**, which is the "latest commit" that
matters here — note it is often *not* `HEAD`, since the ingest commits that follow it are newer:

```sh
C=$(git log -1 --format=%H --diff-filter=A -- transcripts/)
git show --name-only --format= --diff-filter=A "$C" -- transcripts/
```

Say which of the two paths you took, and name the commit(s).

**c. Drop what is already ingested.** Transcript filenames carry the real session date
(`Record YYYY-MM-DD at HHhMMmSSs.txt`), and every session file records the same value as
`date_real`. So a transcript is already canon iff a session file matches its date:

```sh
grep -l '^date_real: 2026-08-25$' kb/sessions/*.md
```

Drop every candidate that matches, and list what you dropped. If **all** candidates are already
ingested, report that and stop — do not re-ingest.

**d. Order them.** Sort the survivors by the **date in the filename, ascending**, and ingest oldest
first. Do not take session numbers or ordering from commit messages: they are written by hand and
have been wrong before (the commit titled "Session 33 transcript" added session **32**'s recording).
The filename date is the reliable key.

**e. Confirm before ingesting.** Report the transcripts you are about to ingest, in order, with the
session id each will become, and ask the user for the `dm` speaker label **for each** (diarisation
labels are per-recording, so a label from a previous session does not carry over). Then proceed.

**f. Run the ingest once per transcript, serially, oldest first.** Complete Steps 1–7 in full for a
transcript — including the wiki rebuild — before starting the next. Never run them in parallel and
never batch them: a later session's recap, quest **Progress log** entries, entity `last_session`
values and session numbering all depend on the earlier session already being canon. Give one Step 8
report per transcript, then a short combined summary at the end.

### 1. Orient
- Read the transcript fully (the one Step 0 selected, or the one the user gave).
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

**The DM is a special speaker — do not treat their out-of-character lines as chatter by default.**
The DM speaks in two registers in one voice, and they split differently:
- **World-facing DM speech is canon** — scene narration, NPC dialogue, lore, history, descriptions,
  and answers to "what do I see / know / recall" (e.g. *"the Horizon Doors predate the Valenwyr,"*
  *"Itharis's clergy have held this gate for centuries"*). Capture all of it. This is the single
  most **authoritative** source in the room: a DM statement of a world fact is **confirmed canon**,
  not a claim to be hedged. (Watch the one edge: if the DM explicitly flags something as a
  player-only aside the *characters* don't yet know, record it as DM-known but not yet in-world.)
- **Table-facing DM speech is out-of-game** — calling for rolls, rules adjudication, initiative,
  scheduling, recaps-as-housekeeping, and OOC banter. Drop it like any chatter.

This also calibrates **confidence** against the fidelity rules (G1): a fact the **DM** states is
*confirmed*; the **same fact asserted by a player** is *suspicion* unless the DM or events bear it
out (the Torston-the-murderer error was a player's belief). When you know who the DM is, weight
their world-facing statements as ground truth and players' theories as suspicions.

Apply the `dm` input here. If it wasn't given, infer the DM from who narrates/adjudicates, apply
the above, and flag the assumption in the Step 8 ledger.

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

**Formatting — Google-Docs-compatible markdown (per style §10):** do **not** hard-wrap. Write one
physical line per paragraph and one per bullet, blank line between blocks. Hard-wrapped notes paste
into Google Docs as broken, non-rendering line-stacks — this is the format the DM actually consumes.

### 7. Regenerate the wiki
Run `py generator/build.py`. Confirm it reports **"All wikilinks resolved."** Fix any unresolved
`[[links]]` (usually a typo'd id or a missing entity) and rebuild.

### 8. Report + confirmation ledger — do not finalise silently
Summarise for the user, and explicitly surface what needs their ruling:
- Session id/title and one-line summary; new entities created and existing entities changed (a short diff); quest progress applied.
- **In-game / out-of-game judgment calls** (so they can correct mis-classifications). If you
  **inferred** which speaker is the DM (no `dm` input given), state that assumption up front — it
  underpins what you treated as authoritative canon vs chatter, so a wrong guess is worth catching.
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
