# Session-Notes Style Ruleset

The rules for writing prose session notes that match the established Kaelindor chronicle voice
(the "Chapter 02" style). When `/session-ingest` produces the human-readable notes artifact, it
writes to these rules. Each note is one file in `notes/session-NN.md`.

## 1. Voice & tense
- **Third person, present tense**, omniscient chronicle: *"Fabian receives an urgent message…",
  "Mags casts Augury…"* Slip into past tense only for backstory or reported earlier events.
- The narrator knows the party's perceptions and spell results, but reports NPC interiority
  **only as the party learns it** — through a spell (Detect Thoughts), an Insight read, or
  spoken word. Never narrate a secret the party hasn't earned.
- Tone is **wry, affectionate, character-forward**. The party is a bickering found-family;
  let their established traits colour the reporting (Fabian's vanity, Mags's bluntness,
  Caspian's pedantry, Rell's detachment). Give emotional beats room, but stay economical.

## 2. Heading & dating
- Head each session: `Session NN - DD/MM/YYYY` (real-world date).
- Add an **in-world date line** where the in-game day begins or rolls over:
  `24 Ashend, 1568` (full on first use; `25 Ashend` / `1 Threadbind` thereafter, no year).
- For a new arc, open with a short **titled prose preamble** in a slightly grander register
  summarising the job, optionally tagged `Source — … / reward — …`.

## 3. Structure within a session
- Loosely chronological prose in **short paragraphs (2–5 sentences)**.
- Insert a **location sub-header** when the scene moves (e.g. `Silver Moon Bathhouse`,
  `At the boathouse`).
- When the party splits, use **named character sub-headers** (`Dakir & Rell`,
  `Fabian & Caspian`) and cut between them with *"Meanwhile,"* / *"Back at the boathouse,"*.
- For downtime or parallel actions, a bulleted list is fine (*"During the journey: • …"*).

## 4. The "facts learned" device (signature)
- Render discrete information the party gathers as a **bulleted list introduced by a colon**:
  *"Further details we are informed of:"*, *"The party discuss what they know of vampires:"*,
  *"Damar knows: • …"*. Use nested sub-bullets for sub-points.
- Quote **letters, documents, and Speak-with-Dead answers verbatim**, set off by `---` rules
  (Speak-with-Dead as Q/A bullets).

## 5. Level of detail
- High on plot, clues, and social manoeuvring. **Combat is compressed** to a running account of
  who did what and whether it landed — not a blow-by-blow log.
- Name spells explicitly and capitalised (Detect Thoughts, Calm Emotions, Pass Without Trace).
- Describe mechanical outcomes **in fiction** ("the spell takes hold", "it resists") rather than
  with numbers. Loot/gold may be noted plainly (*"347 gold goes into Dakir's bag"*).

## 6. Introducing NPCs & locations
- First mention of an NPC: **name + one-clause descriptor**, introduced casually as the party
  learns it — *"the owner of the establishment, Gladys Henshaw"*, *"Lord of Greymere, Mathis
  Irdane — a new lord."* Don't front-load a cast list.
- First mention of a place: a brief sensory/functional sketch — *"The tower is a substantial
  structure with a sturdy door in a courtyard; the ground floor is windowless."*

## 7. Dialogue
- Default to **reported/indirect speech**: *"Mags says they'll take the figure home", "Torston
  asks why they think this is of interest to him."*
- Reserve **direct quotes** for punchy beats or verbatim documents. This keeps the chronicle brisk.

## 8. Formatting
- Bullets (`-`) for facts and parallel actions; `---` rules to set off quoted documents.
- Em-dashes and ellipses carry tone and trailing implication. Sparing bold; no heavy styling.

## 9. Included vs omitted
- **Include**: who did what, what was learned, social subtext, loot, spell usage, NPC reactions,
  plot implications, and the established character humour.
- **Omit**: dice numbers (mostly), rules debates, scheduling, and all real-world player chatter.
  (The KB recap is canon-only; the prose notes may keep a *little* dry table-humour as flavour,
  but never out-of-game logistics.)
- It's in keeping to **end a session mid-scene on a hook**.

## Exemplars (the target voice)
> *"Together, they travel to meet with Torston. He informs them that in light of recent events
> he has called them there… While details have been suppressed, there is a rumour that the death
> was the result of a vampire attack."*

> *"Further details we are informed of:*
> *- Harrington was found in the Silver Moon Bathhouse… he had a private room…*
> *- he arrived with a woman whose face was kept hidden…"*

> *"Mags just stares in cold, quiet disapproval."*

## Normalisation
The source notes are full of inconsistent spellings (Caspian/Caspain, Torston/Torsten,
Eldryn/Eldrin, Trevick/Trevik). **Always normalise names to their canonical KB spelling/id**
when writing notes and KB entries. See `SCHEMA.md` and the existing `kb/` files for canon spellings.
