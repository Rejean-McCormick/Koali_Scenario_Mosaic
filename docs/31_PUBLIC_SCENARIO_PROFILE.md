# Public Scenario Profile — v3.2

## Decision

The Mosaic is a **general-public discovery interface**. Its hover/focus indicators must therefore characterize the scenario in language a first-time visitor can understand without learning Koali's internal architecture.

The earlier component gauges — Kristal, Konnaxion, Orgo, UCKK — are removed from the hover profile. Those names remain valid architectural concepts and can still appear deeper in the full scenario text, where their role is explained in context.

## Public hover profile

Every scenario exposes four layers of public characterization.

### 1. Category

The category name and its color family provide the broadest orientation, for example:

- Find & Understand
- Learn & Share
- Collaborate & Create
- Choose & Govern
- Organize & Act
- Respond & Coordinate
- Remember & Improve
- Disseminate & Connect to the Public

The public UI does not need to display `CAT-##` codes.

### 2. Typical motion

The scenario's recurring pattern is shown as a short phrase, for example:

- Investigate a signal
- Assemble a team around a problem
- Carry a plan through execution
- Turn an incident into coordinated response
- Turn action into a lesson

The public UI does not need to display `PAT-##` codes.

### 3. What happens here

Seven binary visual indicators summarize the scenario's activity profile:

| Public indicator | Existing palette tags that activate it |
| --- | --- |
| Understand | `find`, `understand`, `verify` |
| Learn & share | `learn`, `teach-share` |
| Create together | `collaborate`, `create` |
| Decide | `deliberate`, `choose` |
| Organize & act | `organize`, `act` |
| Respond | `respond`, `coordinate` |
| Remember & share | `remember`, `disseminate` |

These are **not scores**. A light is active when the canonical scenario palette contains at least one corresponding verb. This avoids inventing false numerical precision while still giving every scenario a distinctive visual signature.

### 4. Human context

Three compact metadata rows complete the profile:

- **Scale** — individual, team, organization, inter-organizational, community, public institution;
- **Context** — a compact combination of existing `settings` and `domains`, such as Enterprise · Maintenance · Automotive or Crisis · Emergency;
- **Special conditions** — only cross-cutting conditions explicitly present in scenario metadata, such as Offline, Multilingual, Sensitive Data, Public Facing, Intermittent Connectivity, High Consequence, Local First, AI Optional, Role Routing.

If no special condition is assigned, the UI says **None highlighted** rather than claiming that no special constraint exists.

## Why this is better for the public

A first-time visitor can understand:

> This is a team/organization scenario, in maintenance, mostly about understanding and acting, with no special operating condition highlighted.

They do not need to know what a Kristal or Orgo is before they can understand the use case.

## Detailed scenario pages

The top of each detailed scenario page follows the same public profile language: typical motion, scale, context, special conditions, and activity indicators.

Internal architecture can still appear later in the editorial body under explanatory sections such as component roles. This preserves architectural depth without making it a prerequisite for exploration.

## Layout stability

The v3.1 fixed-height preview behavior remains unchanged:

- desktop: 330 px reserved preview height;
- tablet: 392 px;
- mobile: 622 px;
- titles and summaries remain line-clamped.

Changing scenario indicators must never move the Mosaic vertically.
