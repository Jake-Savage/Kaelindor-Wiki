# Kaelindor KB — Agent Query Contract

This repo is a D&D campaign knowledge base. When the user asks a natural-language question
about the campaign, **answer from the `kb/` files** — they are the source of truth. This file
tells you how to navigate them.

## Where things live

| The user asks about… | Read from… |
|----------------------|-----------|
| A person (PC or NPC) | `kb/characters/<id>.md` |
| A place              | `kb/locations/<id>.md` |
| A mission / plot thread / "progress" | `kb/quests/<id>.md` |
| A church, order, nation, group | `kb/factions/<id>.md` |
| An object            | `kb/items/<id>.md` |
| A world concept (the Uthrel, gods, Horizon Doors, history) | `kb/lore/<id>.md` |
| "What happened in session N" | `kb/sessions/` |
| Overview / "where are we" | `kb/index.md`, then active quests |

Every file has YAML frontmatter (structured facts) + a prose body. Cross-references are
`[[id]]` links — follow them to answer relationship and significance questions.

## How to answer the three core question shapes

1. **Progress / status** ("what's the progress on identifying the source of the Uthrel?")
   - Open the matching `kb/quests/<id>.md`. Lead with its `status` + `summary`, then
     synthesize the **Progress log** newest-first into a coherent top-level summary. Surface
     **Open threads** and **Leads / next steps**. Cite the sessions (`S2.20`) the facts came from.

2. **Significance** ("what's the significance of that NPC?")
   - Open `kb/characters/<id>.md`. Give role + current `status`, then explain why they matter:
     follow `relationships`, `affiliations`, and `[[links]]` into the quests and lore they touch.
     Distinguish what the party knows from DM-only notes if asked as the DM vs as a player.

3. **Situational advice** ("we're in Greymere — anything we should do?")
   - Open the `kb/locations/<id>.md` for the place, then cross-reference: which **active**
     quests list this location in `involves_locations`, which NPCs are here, what **Open
     threads** point back to it. Recommend concrete next actions grounded in those threads.

## Follow-up questions

The user will drill down ("what's that NPC's significance?", "tell me more about X"). Keep the
prior answer's entities in mind; resolve pronouns to the last-named entity; pull the next file
rather than guessing.

## Style of answers

Lead with the answer. Be a knowledgeable game-master's assistant: concrete, grounded in the
files, honest about what is unknown or unresolved in-world. Cite source sessions/entities so
the user can verify. Don't invent canon — if the KB doesn't say, say so.

## Editing the KB

- Conform to `SCHEMA.md`. Filename must equal `id`. Keep `summary` to one sentence.
- After content changes, regenerate the wiki: `py generator/build.py`.
- New canon from a session goes in via the `/session-ingest` skill, which also appends to
  quest **Progress logs** and bumps `last_updated_session`.
