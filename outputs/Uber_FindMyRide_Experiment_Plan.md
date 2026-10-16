# Experiment Plan: Structured Pickup Meeting-Point Guidance

**Status:** proposal for discovery. Thresholds below are proposed decision criteria, not proven improvements. No feature is preselected; "structured guidance" is a test condition, not a committed solution.

**Framework fit:** the experiment is a Lean Startup Build-Measure-Learn cycle (Build = prototype of condition B; Measure = metrics below; Learn = decision rules below). Its metrics map onto a metric tree: meeting success, calls/messages and extra walking drive coordination time; meeting success may also reduce pickup cancellations; these may in turn affect retained trips and rider time (hypotheses, not measured).

## Research question
Does clearer, mutually understood meeting-point guidance help riders and drivers meet more successfully at complex pickup locations?

## Why this experiment
- Prioritised hypothesis: **H1, meeting-point ambiguity** (weighted score 2.45 of 3, rank 1 of 3, first under all four weightings tested; rubric, weights and sensitivity in `Uber_FindMyRide_Frameworks_Appendix.md` and `Uber_FindMyRide_Problem_Prioritization.csv`). Scores and weights are analytical judgements, not measured data.
- Primary survey (n=24, convenience): gate/entrance confusion 13, long waiting 11, incorrect or inconvenient pin 10, driver could not find exact location 9, asked to walk elsewhere 8.
- Secondary reviews (n=33, 12 Sep to 14 Oct 2026, not representative): gate confusion 2, pin mismatch 2, driver location difficulty 4. Thin support, so the experiment tests the survey signal rather than assuming it.
- H2 (coordination friction) is a related mechanism and is measured here. H3 (cancellation) is a downstream outcome; no gate/pin code appears in any of the 22 cancellation-coded reviews, so no causal link is assumed.

## Target segment
Riders and drivers using malls, large residential complexes or other venues with multiple entrances and restricted vehicle access.

## Phase 1: moderated usability testing
- **Participants:** approximately 8-12 riders and 5-8 drivers, subject to recruitment feasibility. Not statistically powered; the aim is to find failure modes and direction of effect, not to estimate effect size.
- **Conditions (within-participant where practical, order counterbalanced):**
  - **A:** existing pickup pin and current guidance.
  - **B:** pickup pin plus clearly labelled entrance/gate, an accessible meeting-point description and confirmation of the intended location.
- **Scenarios:** realistic venue scenarios (for example a multi-entrance mall, a gated residential complex with restricted vehicle access), with rider and driver tested as a pair or via a simulated counterpart.
- **Measures:**
  - Whether both participants identify the same accessible meeting point
  - Time to identify the correct meeting point
  - Number of clarification steps (calls, messages, re-asks)
  - Task success
  - Perceived clarity and confidence (short post-task rating)

## Phase 2: small field pilot (only if Phase 1 supports further testing)
- Compare the current pickup experience with structured guidance in similar venue conditions.
- **Primary outcome:** percentage of eligible pickup attempts completed successfully within a predefined time threshold (threshold to be set from baseline observation, for example a few minutes after driver arrival near the venue).
- **Secondary outcomes:** time from driver arrival near the venue to successful meeting; number of coordination calls or messages; extra rider walking distance; pickup-related cancellations (reported descriptively, no causal claim).
- **Sample size:** to be set by a power calculation once baseline variance is known. No power is claimed for the proposed sample.

## Guardrails (any breach can pause or stop the test)
- Rider and driver safety (no encouraging unsafe stopping or walking)
- Accessibility (meeting points must be reachable for riders with mobility or visual needs)
- Driver distraction (no added interaction while driving)
- Privacy (no unnecessary location or venue-level data exposure)
- Additional pickup complexity (extra steps, confusion, longer interactions)

## Proposed success threshold
- **Proposed decision criterion:** at least a 20% reduction in median coordination time (condition B vs A in Phase 1; pilot vs baseline in Phase 2), together with no deterioration in task success. This is a proposed criterion for deciding whether to continue; it is not evidence of improvement.

## Decision rules
| Decision | Condition |
|---|---|
| **Continue** (to Phase 2, then wider discovery) | B beats A on shared-meeting-point agreement and task success, coordination time meets the proposed criterion, drivers and riders both benefit, and no guardrail concern appears |
| **Iterate** | Mixed results (helps riders but not drivers, helps some venue types only, adds clarification steps) or minor guardrail concerns that a redesign could address |
| **Stop** | No meaningful improvement over A, a guardrail breach (safety, accessibility, distraction, privacy), or evidence that the added complexity outweighs the benefit |

## What this experiment cannot show
- Prevalence of pickup problems across Uber users or India
- That meeting-point ambiguity causes cancellations (H3 needs separate causal validation)
- Revenue impact; the TAM/SAM/SOM scenario is illustrative and uses unvalidated assumptions

## Dependencies and risks
- Recruiting drivers is harder than riders; Phase 1 can proceed with the lower end of the driver range.
- Lab scenarios may not reproduce real traffic and access restrictions; Phase 2 exists to check this.
- Venue consent and location privacy need to be settled before any field work.
