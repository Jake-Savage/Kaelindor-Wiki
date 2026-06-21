# KB Entity Schema

Every file in `kb/<type>/` is markdown with a YAML frontmatter block followed by a prose body.
The frontmatter is machine-parseable (drives the wiki + agent queries); the body is for humans
and the agent both. **The filename must equal the `id`** (e.g. `kb/characters/caspian-talon.md`).

Cross-reference other entities anywhere in the body with `[[id]]` or `[[id|display text]]`.

## Shared rules

- `id`: kebab-case of the canonical name. Stable forever once chosen.
- `type`: one of `character | location | quest | faction | item | lore | session`.
- `title`: human display name.
- `summary`: one sentence. Used in list pages, search results, and top-level agent summaries.
- `tags`: optional list of free keywords to boost search.
- Session references use the form `S<chapter>.<number>` in prose progress logs (e.g. `S2.04`),
  and the numeric `*_session` fields hold the absolute session count where useful.

## `character`
```yaml
---
id: caspian-talon
type: character
title: Caspian Talon
category: pc            # pc | npc
player: Cade           # PCs only; omit for NPCs
species: Human
role: Divination Wizard   # class for PCs, role/occupation for NPCs
status: alive          # alive | dead | unknown | transformed | undead
home: Crownspire        # optional
affiliations: [the-tower-of-heaven]   # faction ids
relationships:          # optional, freeform but keyed by id
  - who: fabian-perennius
    note: Frequent collaborator; mutual museum-fame ambitions.
first_session: S1
last_session: S2.21
tags: [scholar, vampire-suspicious]
summary: Coldly rational divination wizard obsessed with studying the Uthrel and dragon remains.
---

## Overview
Who they are, role in the party / world.

## Knowledge & motivations
What drives them, what they know, their agenda.

## Appearances
- S2.01: Introduced investigating the bathhouse murder.

## DM notes / secrets
(Single-view KB — kept in one place but clearly headed.)
```

## `location`
```yaml
---
id: greymere
type: location
title: Greymere
location_type: village    # city | town | village | wilds | dungeon | landmark | plane
region: Kaelindor
controlled_by: lady-aldara   # optional, character/faction id
connected_to: [the-eldryn-forest, lake-therro]
status: active
first_session: S2.05
tags: [fishing, lake]
summary: Lakeside fishing village beset by the Quickened and the spread of the Uthrel.
---

## Overview
## Notable inhabitants & sites
## Events here
## DM notes
```

## `quest`
```yaml
---
id: source-of-the-uthrel
type: quest
title: Identify the Source of the Uthrel
status: active            # active | stalled | resolved | abandoned
priority: main            # main | side
opened_session: S2.??
last_updated_session: S2.21
involves_characters: [trevick, dakir, rell-aetris]
involves_locations: [the-eldryn-forest, the-feywild]
factions: [the-eldryn]
tags: [uthrel, feywild]
summary: The party races to find where the magic-devouring Uthrel comes from and how to stop it.
---

## Hook
## Progress log
- S2.19: The Eldryn react to the word "uthrel"; confirmed not a moss.
- S2.20: Learned it came from the Feywild; party permitted to learn disposal on patrols.

## Open threads
- How did it enter the Feywild?
- Connection to the Elves leaving / the war?

## Leads / next steps
```

## `faction`
```yaml
---
id: the-covenant-of-naelos
type: faction
title: The Covenant of Naelos
kind: church            # church | order | nation | guild | group | family
leader: null
notable_members: [mags]
status: active
tags: [naelos, oaths]
summary: The faith of Naelos, god of community, oaths, and transparent dealing.
---

## Overview
## Structure / ranks
## Relationship to the party
```

## `item`
```yaml
---
id: sunblade-of-torston
type: item
title: Torston's Sunblade
kind: weapon            # weapon | artifact | tome | trinket | consumable
owner: fabian-perennius
status: held            # held | lost | destroyed | sought
tags: [vampire, anti-undead]
summary: An heirloom sunblade gifted by Lord Torston for the vampire hunt.
---

## Description
## History
```

## `lore`
```yaml
---
id: the-uthrel
type: lore
category: threat        # religion | deity | history | cosmology | people | threat | concept
tags: [feywild, arcanophage]
summary: A parasitic, magic-devouring growth from the Feywild that resembles moss but is not.
related: [the-horizon-doors, the-feywild]
---

## What it is
## What's known
## Open questions
```

## `session`
```yaml
---
id: ch02-s01
type: session
chapter: 2
number: 1
title: Searching for a Murderous Vampire
date_real: 2025-09-30
date_inworld: 24 Ashend 1568
characters: [caspian-talon, fabian-perennius, mags, trevick, rell-aetris]
locations: [snowdrop-house, silver-moon-bathhouse, the-floodgate]
quests: [the-bathhouse-vampire]
summary: Lord Torston hires the party to hunt a vampire behind a high-profile bathhouse murder.
---

## Recap
Chronicle-style narrative of what happened in-world this session.

## Key facts learned
- ...

## Threads opened / advanced
- ...
```
