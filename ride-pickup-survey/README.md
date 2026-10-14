# Ride Pickup Experience Study

Independent product-discovery survey on pickup coordination across Uber, Ola and Rapido.

## Build the form (2 min)
1. Go to <https://script.google.com> → **New project**.
2. Paste `create_form.gs`, run `createRidePickupForm`, authorise.
3. Open the **Edit URL** from the log → *Responses* → link to Google Sheets.
4. Preview every branch once before sharing the live URL.

## Flow & branching
| # | Section | Branch rule |
|---|---------|-------------|
| 0 | Consent | No → submit |
| 1 | Eligibility (age, use in last 3 months) | Under 18 or No → submit |
| 2 | Usage profile (city, frequency, purpose, ride types, apps, primary app) | Primary app → 3/4/5; "about equally" → 6 |
| 3–5 | Uber / Ola / Rapido-specific (reasons, ease of pickup, frustration) | All → 6 |
| 6 | Setting & reaching the pickup point | Pickup difficulty? Yes → 7, No → 8 |
| 7 | Pickup difficulty deep-dive (issue types, location, app, coordination, time lost, outcome, severity, story) | → 8 |
| 8 | Waiting times & cancellations (ETA accuracy, wait, tolerance) | Cancellation? Yes → 9, No → 10 |
| 9 | Cancellation details (who, why, fees, next action) | → 10 |
| 10 | App comparison grid, NPS, improvement priorities, one change | Follow-up? Yes → 11, No → submit |
| 11 | Opt-in contact | submit |

## Neutrality & ethics checklist
- No company affiliation claimed; app order rotated in comparison grid columns only where possible.
- Frequency/behaviour questions before opinion questions; balanced scales; "Not sure / No difference" options.
- Personal data only via opt-in; deleted at study end; aggregate reporting only.

## Analysis framework

**Research questions**
1. Where and why do riders and drivers fail to meet at pickup?
2. How much time and how many rides are lost to pickup friction and cancellations?
3. How do Uber, Ola and Rapido differ on pickup-related attributes, and does this drive preference/switching?

**Core metrics**
| Metric | Source |
|--------|--------|
| Pickup friction rate = % "Yes" to difficulty in 3 months | §6 |
| Exact-pickup accuracy = % Always/Most of the time | §6 |
| Coordination load = % calling/messaging on most/every ride | §6 |
| Time lost per incident (median band) | §7 |
| Incident failure rate = % ending in cancel/rebook/other transport | §7 |
| ETA gap & wait tolerance (gap vs. tolerance = cancel risk) | §8 |
| Cancellation incidence, driver- vs rider-initiated share | §8–9 |
| Unfair-fee rate; post-cancel switching rate | §9 |
| Pickup-NPS by primary app | §10 |
| Attribute "best app" share per row | §10 grid |

**Segmentation cuts:** primary app × ride type (bike/auto/cab) × city × frequency × pickup location type × age group.

**Pain-point prioritisation:** for each issue type in §7, score = *frequency* (% selecting) × *severity* (mean frustration of those selecting) × *failure rate* (% ending in cancellation). Plot on a frequency-vs-severity 2×2; top-right = priority opportunities.

**Qualitative coding (open text in §3–5, §7, §10):** tag each response with
`location-accuracy`, `entry/access`, `crowding`, `communication`, `language`, `vehicle-ID`, `driver-behaviour`, `ETA`, `cancellation-coercion`, `fees`, `safety`, `other`.
Affinity-map tags into themes; quote 2–3 representative verbatims per theme.

**Hypotheses to test**
- H1: Pickup friction is highest at gated/large venues (societies, tech parks, airports, stations).
- H2: Bike-taxi and auto rides show higher driver-initiated cancellations than cabs.
- H3: Riders whose ETA gap exceeds their wait tolerance report higher switching.
- H4: Communication/language difficulty is a leading driver of failed pickups.

**Sample & quality:** target ≥150 complete responses (≥40 per primary app) for comparisons; drop speeders (< 3 min) and straight-liners; report n for every chart; treat findings as directional (self-selected sample).

**Deliverables:** pain-point heat map, platform attribute matrix, journey map of a failed pickup, 3–5 opportunity statements ("How might we…"), interview recruit list.
