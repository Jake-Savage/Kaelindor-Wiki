---
name: codex
description: >-
  Answer a natural-language question about the Kaelindor D&D campaign by searching and
  synthesizing the knowledge base in kb/. Use for questions like "what's the progress on the
  Uthrel?", "what's the significance of <NPC>?", "we're in <place> — what should we do?", or
  any lookup about characters, locations, quests, factions, items, lore, or past sessions.
  Supports follow-up questions in the same thread.
---

# Consult the Kaelindor Codex

Answer the user's question (passed in args) from the knowledge base in `kb/` — the markdown is
the source of truth (not `site/`). This is the interactive companion to the query contract in
`CLAUDE.md`; read that too if present.

## 1. Understand the question
Identify (a) the **subject(s)** — a person, place, quest, faction, item, or concept — and
(b) the **shape** of the question: progress/status, significance, situational advice, or a plain
lookup. Note whether it's a **follow-up** to the previous answer (resolve pronouns like "that
NPC" / "there" to the last-named entity).

## 2. Find the right entries
Entities live in `kb/<type>/<id>.md` where `id` is the kebab-case of the canonical name
(`source-of-the-uthrel`, `serris-dane`, `greymere`).
- **Try the direct path first**: guess the id and open `kb/<type>/<id>.md`.
- **If unsure of the name/spelling**, `Grep` the subject term across `kb/` (case-insensitive) to
  find the matching file(s) and related mentions, then open the best matches.
- **Follow `[[id]]` links** out of the entry as far as the question needs — relationships,
  involved quests, referenced lore. For "significance" and "situational" questions this matters.
- Don't stop at one file when the answer spans several (e.g. a location + the active quests that
  reference it).

## 3. Answer, by shape
- **Progress / status** (a quest): lead with `status` + one-line `summary`, then synthesize the
  **Progress log** newest-first into a coherent recap; surface **Open threads** and **Leads /
  next steps**. Cite the sessions facts came from (e.g. `S2.21`).
- **Significance** (a character/entity): give role + current `status`, then *why they matter* —
  follow `relationships`, `affiliations`, and `[[links]]` into the quests and lore they touch.
- **Situational** ("we're in X, anything to do?"): open the location, then cross-reference which
  **active** quests list it in `involves_locations`, which NPCs are there, and what **Open
  threads** point back to it — then recommend concrete next actions grounded in those threads.
- **Lookup / general**: answer from the matching entry plus its closely-linked context.

## 4. Rules
- **Lead with the answer.** Be concrete and grounded in the files; cite source sessions/entities
  so the user can verify.
- **Don't invent canon.** If the KB doesn't say, say so; preserve in-world uncertainty (what the
  party *believes* vs what's *confirmed*).
- **DM vs player view.** Default to a full answer (the user is the DM). If the user asks for a
  *player-safe* / spoiler-free answer, omit anything under `## DM notes / secrets` and any
  summary lines that reveal a secret (e.g. "secretly the murderer").
- **Follow-ups**: keep the prior answer's entities in working memory; pull the next file rather
  than guessing.

## 5. Offer the thread onward
After answering, if useful, note the obvious follow-up the user might want ("I can go deeper on
[[hesk]] or the [[the-bright-gate|tampered gate]] next"). Keep it brief.
