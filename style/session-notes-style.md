# Session-Notes Format

Rules for the prose session notes produced by `/session-ingest` (one file per session in
`notes/session-NN.md`). The notes are a **detailed, impersonal record of events** — a neutral
chronicle with no authorial voice, personality, or humour. They report and analyse what happened;
they do not perform it. *Impersonal* refers to **register**, not depth: the notes are analytically thorough and may read subtext and infer
motivation (see §2) — they simply do so flatly, without a narrator's personality.

## 1. No authorial identity — the governing rule
- No narratorial voice, opinion, humour, wit, or editorial aside. Do not label events funny,
  clever, dramatic, touching, or ironic — and do not write to entertain.
- Do not colour the account with a character's personality or the writer's. Report and analyse;
  do not flavour. ("X argues for caution," not "X, ever the worrier, frets…").
- Neutral, even register throughout: plain, precise, factual. No rhetorical flourish, no jokes,
  no knowing tone, no dramatic build-up.

## 2. Inference & subtext — welcome, grounded, impersonal
- **Capturing social subtext, insight, motivation, and implication is expected**, not avoided.
  The note-taker **may infer directly from context** — *where the reading is broadly discussed at
  the table or heavily implied in-fiction.*
- State inferences plainly, as an analyst would, and **anchor them to their basis**: *"The party
  reads the Greenheart's reluctance as concealment — he appears to know more than he admits,"*
  *"Torston's evasions strongly imply he is steering suspicion elsewhere."* The grounding (table
  consensus, an NPC's manner, a spell result, the weight of evidence) should be visible.
- Do **not** invent subtext with no support at the table or in the fiction, and do not promote a
  grounded inference into an unqualified hard fact about a hidden truth — keep "strongly implies"
  as "strongly implies." (Certainty in the structured KB is governed separately; see the foot of
  this file.)

## 3. Voice & tense
- **Third person, present tense**, impersonal: *"The party travels to the estate. Caspian casts
  Detect Thoughts on the guard."* No first person, no direct address, no "our heroes."

## 4. Heading & dating
- Head each session: `Session NN - DD/MM/YYYY` (real-world date).
- Add an in-world date line where the in-game day begins or rolls over: `24 Ashend, 1568` (full
  on first use; `25 Ashend` / `1 Threadbind` thereafter, no year).
- For a new arc, a brief factual preamble naming the job is fine (e.g. `Source — Chancellor
  Wicklow. Reward — official favour + 1400 gold.`). No scene-setting flourish.

## 5. Structure within a session
- Chronological prose in short paragraphs (2–5 sentences).
- **Location sub-header** when the scene moves (e.g. `Silver Moon Bathhouse`, `The Boathouse`).
- When the party splits, use **named character sub-headers** (`Dakir & Rell`, `Fabian & Caspian`)
  and mark cuts plainly (*"Meanwhile, at the boathouse,"*).
- Downtime or parallel actions may be given as a bulleted list.

## 6. The "facts learned" device
- Render information the party gathers as a **bulleted list introduced by a colon**: *"The party
  learns the following:"*, *"Damar states:"*. Nested sub-bullets for sub-points.
- Quote letters, documents, and Speak-with-Dead answers **verbatim**, set off by `---` rules
  (Speak-with-Dead as Q/A bullets).

## 7. Level of detail
- High on plot, clues, investigation, social dynamics, and decisions — including the **inferred
  motivations and subtext** of §2 alongside the literal events.
- **Combat is compressed** to a factual account of who acted and the result — not a blow-by-blow
  log, and not dramatised.
- Name spells explicitly and capitalised (Detect Thoughts, Calm Emotions, Pass Without Trace).
- State mechanical outcomes plainly in-fiction ("the spell takes hold," "it resists"); record
  loot/gold directly ("347 gold is recovered").

## 8. Introducing NPCs & locations
- First mention of an NPC: **name + a factual descriptor**, introduced as the party learns it —
  *"the establishment's owner, Gladys Henshaw,"* *"the Lord of Greymere, Mathis Irdane."*
- First mention of a place: a brief functional description; sensory detail only where it bears on
  events.

## 9. Dialogue
- Default to **reported/indirect speech**: *"Torston asks why they think this concerns him."*
- Use **direct quotes** only for verbatim documents, Speak-with-Dead answers, or where the exact
  wording matters — not for effect.

## 10. Formatting
- Bullets (`-`) for facts and parallel actions; `---` rules to set off quoted documents.
- Use punctuation functionally, not for tone. Avoid trailing ellipses, dramatic em-dashes, scare
  quotes, and emphasis added for colour. No bold for emphasis within the prose.

## 11. Included vs omitted
- **Include:** who did what; what was learned; social subtext, insight, and grounded inference
  (§2); negotiation outcomes; loot; spell usage; NPC reactions and stated positions; decisions;
  and plot implications.
- **Omit:** all out-of-game material (rules/mechanics debate, dice, scheduling, real-world
  tangents, table chatter), **and all authorial colour** — humour, asides, characterisation by
  the writer, and dramatisation.
- A session may end at the last event of the night; no engineered cliffhanger phrasing.

## 12. Exemplars (the target register)
> *"Torston summons Fabian and Caspian and reports that his rival, Lord Harrington, has been found
> dead in the Silver Moon Bathhouse, drained of blood, with a vampire rumoured responsible. He
> offers a reward for a slain vampire and gives Fabian a sunblade."*

> *"Trevick determines the killer left through the window; Rell finds blood flushed down the
> drain, inconsistent with a vampire feeding, and the body had been deliberately displayed. The
> party reads the scene as a staged killing rather than a true vampire attack."*  ← grounded
> inference, stated flatly

> *"The Greenheart counsels patience and declines to investigate. The party reads his reluctance
> as concealment — he appears to know more than he admits — though he offers no reason."*

(Inference is present in the last two, but carried as analysis anchored to evidence — no judgement,
humour, or framing.)

## 13. Normalisation
Normalise all names to their canonical KB spelling/id (Caspian, Torston, Eldryn, Trevick, …) —
see `SCHEMA.md` and the existing `kb/` files.

---

**Relationship to the structured KB.** These notes may read more interpretively than the
`kb/` entries. The KB's structured facts still follow the `/session-ingest` fidelity rules
(G1–G5): a reading the notes state as "strongly implied" becomes, in a KB entry, a hedged or
attributed claim or an open thread — never an unqualified hard fact about a hidden truth. Same
events, two registers: the notes analyse freely but flatly; the KB records certainty precisely.
