# Uber Find My Ride: Frameworks Appendix

Supports the final presentation. Primary survey (n=24, convenience sample) and secondary app-store reviews (n=33, 12 Sep 2026 to 14 Oct 2026, purposive, not representative) are kept separate throughout. **All framework scores are analytical judgements, not measured data.**

## 1. Jobs to Be Done (JTBD)

**Definition.** JTBD frames demand as the progress a person is trying to make in a circumstance, independent of any product feature (Christensen et al., 2016; Ulwick, 2016).

**Core rider job.** When I have booked a ride from a busy or complex place, I want to meet my driver quickly and with certainty, so I can start my trip on time without stress.

**Core driver job (hypothesis, not evidenced by the data).** When I arrive near a pickup, I want to know exactly where to stop and whom to meet, so I can complete the pickup quickly and move to the next trip.

**Evidence for the rider job (primary only).** 15 of 24 worried about being late; 11 reported long waiting; 9 met the driver only after a delay. The driver job rests on 1 driver review in the secondary sample and no driver survey data, so it is a hypothesis to test.

## 2. Customer journey mapping

**Definition.** A journey map lays out the stages a customer passes through and the friction at each (Gibbons, 2018). The six stages come from the project brief (`PROMPT.md`): 1 Driver assigned, 2 Pickup interpretation, 3 Driver approaches, 4 Coordination, 5 Meeting, 6 Outcome.

**Assumption.** Mapping survey options and review codes to stages is the analyst's judgement. Counts are respondents or reviews that mention an item, not rates; items overlap and must not be summed.

### Primary survey (n=24)

| Stage | Items mapped and respondent counts |
|---|---|
| 1 Driver assigned | not measured in survey |
| 2 Pickup interpretation | gate/entrance confusion 13; wrong pin 10 |
| 3 Driver approaches | long waiting 11 |
| 4 Coordination | driver called for directions 11; unclear communication 8 |
| 5 Meeting | driver could not find location 9; asked to walk 8 |
| 6 Outcome | cancelled 10 (rider 6, driver 4); met after delay 9 |

### Secondary reviews (n=33; reviews touching each stage)

| Stage | Reviews |
|---|---|
| 1 Driver assigned | 2 |
| 2 Pickup interpretation | 4 |
| 3 Driver approaches | 15 |
| 4 Coordination | 14 |
| 5 Meeting | 9 |
| 6 Outcome | 20 |

**Reading.** In the survey, friction is reported at stage 2 (interpreting the pickup point). In reviews it clusters at stages 3, 4 and 6 (approach, coordination, outcome). The two lenses answer different questions (see the triangulation matrix), so this is a difference in emphasis, not a contradiction.

## 3. Weighted problem-prioritisation matrix

**Method.** Multi-criteria weighted scoring: each hypothesis is scored 1-3 on six criteria; the weighted score is the sum of weight x score (range 1-3). Weights express how much each criterion should count for a discovery decision. **Scores and weights are judgements, not measurements.**

### Rubric and base-case weights

| Criterion | Weight | Scoring guide |
|---|---|---|
| Strength of supporting evidence | 25% | 3 = consistent across both lenses and sizeable; 1 = thin, indirect or single-source |
| Observed customer impact | 20% | 3 = severe or costly outcome reported (e.g. lost trip, safety, large delay); 1 = mild or not reported |
| Frequency in the relevant samples | 15% | 3 = among the most-cited items in the sample(s); 1 = rarely cited |
| Relevance to Find My Ride scope | 15% | 3 = directly about locating/meeting at pickup; 1 = mostly outside pickup coordination |
| Potential for product intervention | 15% | 3 = clear levers within product design; 1 = driven mainly by factors outside product control |
| Confidence (inverse of remaining uncertainty) | 10% | 3 = low uncertainty; 1 = high uncertainty (key assumptions untested) |

### Scores and rationale

| Hypothesis | evidence | impact | frequency | scope | intervention | confidence | Weighted score | Rank |
|---|---|---|---|---|---|---|---|---|
| H1 Meeting-point ambiguity | 2 | 2 | 3 | 3 | 3 | 2 | 2.45 | 1 |
| H2 Coordination friction | 2 | 2 | 2 | 3 | 2 | 2 | 2.15 | 2 |
| H3 Cancellation-related friction | 1 | 3 | 3 | 1 | 1 | 1 | 1.70 | 3 |

**H1 Meeting-point ambiguity.** Riders and drivers lack a shared understanding of the exact, physically accessible pickup location, particularly at complex venues.

- Evidence 2: primary gate/entrance confusion 13/24, wrong pin 10/24, driver could not find location 9/24; secondary only gate 2/33, pin 2/33, driver location 4/33.
- Impact 2: 15/24 worried about being late; delay and walking reported, but not a lost trip by itself.
- Frequency 3: gate confusion is the most-ticked primary difficulty (13/24).
- Scope 3: directly about meeting at pickup.
- Intervention 3: information design levers exist without presupposing a feature.
- Confidence 2: mainly one small convenience survey.

**H2 Coordination friction.** Riders and drivers rely on calls, messages and additional walking to resolve uncertainty, increasing pickup effort and delay.

- Evidence 2: waiting 11/24, drivers called for directions 11/24, unclear communication 8/24; secondary communication 9/33, waiting 8/33.
- Impact 2: extra effort and delay.
- Frequency 2: common in both, but below gate confusion in the survey and below cancellation in reviews.
- Scope 3: coordination is the find-my-ride mechanism.
- Intervention 2: levers exist but calls/waiting have other causes.
- Confidence 2: cause of calls and waiting not separated from other causes.

**H3 Cancellation-related friction.** Some pickup cancellations may be associated with coordination difficulties; other causes include driver availability, incentives, traffic, fares and operations.

- Evidence 1 (for a coordination link): 0 of 22 cancellation reviews carry a gate or pin code; 5 also carry a fare code.
- Impact 3: lost trips and fees; primary 10/24 outcomes were cancellations (rider 6, driver 4).
- Frequency 3: most-cited review theme (22/33), but reviews are self-selected.
- Scope 1: many causes lie outside meeting-point information.
- Intervention 1: causes are mixed (availability, incentives, fares, operations).
- Confidence 1: causal path untested.

### Sensitivity (does the ranking depend on the weights?)

| Weighting | Weights (evidence / impact / frequency / scope / intervention / confidence) | H1 | H2 | H3 | Order |
|---|---|---|---|---|---|
| Base case | 25% / 20% / 15% / 15% / 15% / 10% | 2.45 | 2.15 | 1.70 | H1 > H2 > H3 |
| Equal weights | 17% / 17% / 17% / 17% / 17% / 17% | 2.50 | 2.17 | 1.67 | H1 > H2 > H3 |
| Impact-heavy | 15% / 35% / 15% / 10% / 15% / 10% | 2.40 | 2.10 | 2.00 | H1 > H2 > H3 |
| Scope excluded | 30% / 25% / 20% / 0% / 15% / 10% | 2.35 | 2.00 | 1.90 | H1 > H2 > H3 |

**Conclusion.** H1 ranks first under all four weightings, so the recommendation to prioritise H1 is supported by the scoring as specified. The margin over H3 is smaller when impact is weighted heavily (0.4) or scope is excluded, and the scores themselves are judgements, so the recommendation is a discovery priority, not a proof.

**Why not H2 or H3 first.** H2 (coordination friction) is likely a mechanism downstream of H1: calls, waiting and walking are how ambiguity gets resolved, and have other causes too, so it is measured within the experiment rather than treated as the root problem. H3 (cancellation) is the most cited review theme (22/33) and costly, but the link to coordination is not shown (0 of 22 cancellation reviews carry a gate or pin code; 5 carry a fare code) and many causes sit outside meeting-point information. It is kept as an outcome metric and a research question needing causal validation.

**Limits.** The scope criterion favours H1 and H2 by construction; the "scope excluded" run checks this. Scores rely on small, self-selected samples.

## 4. Lean Startup: Build-Measure-Learn

**Definition.** Build a minimum test, measure against a pre-stated criterion, learn and decide whether to persevere, iterate or stop (Ries, 2011).

| Step | This project |
|---|---|
| Build | Minimum prototype of structured meeting-point guidance (condition B) versus the current pin and guidance (condition A). Not a feature commitment |
| Measure | Phase 1: same meeting point identified, time to identify, clarification steps, task success, clarity and confidence. Phase 2 (only if Phase 1 supports): % eligible pickups completed within a predefined time threshold; secondary: arrival-to-meeting time, calls/messages, extra walking, pickup cancellations |
| Learn | Proposed criterion of at least 20% lower median coordination time with no loss of task success (a proposed decision criterion, not proven). Continue / iterate / stop rules in `Uber_FindMyRide_Experiment_Plan.md`. No statistical power is claimed |

## 5. Metric tree

**Definition.** A metric tree decomposes an outcome into the metrics that drive it, so product measures can be linked to business results. Links here are hypotheses to test, not established causes.

```
Potential business outcomes (not measured): retained trips, rider time saved, platform revenue
|-- Fewer pickup-related cancellations  <-- (hypothesis) meeting success
`-- Shorter coordination time           <-- meeting success, fewer calls/messages, less extra walking
```

**Guardrail metrics:** rider and driver safety, accessibility, driver distraction, privacy, added pickup complexity. The TAM/SAM/SOM model (illustrative, unvalidated assumptions, not a forecast) is not used to set any of these metrics.

## 6. Assumptions

- Framework scores, weights and stage mapping are analyst judgements.
- Primary and secondary counts have different denominators and are never combined.
- Secondary reviews: Apple App Store India only, 33 reviews, 12 Sep 2026 to 14 Oct 2026 (about five weeks of the requested six months); 1 driver review; no per-review URL.
- Driver job and driver-side metrics are hypotheses; the data contain almost no driver evidence.
- No feature is preselected; "structured meeting-point guidance" is a test condition.

## 7. References

- Christensen, C. M., Hall, T., Dillon, K., & Duncan, D. S. (2016). *Competing Against Luck*. Harper Business.
- Ulwick, A. W. (2016). *Jobs to Be Done: Theory to Practice*. Idea Bite Press.
- Ries, E. (2011). *The Lean Startup*. Crown Business.
- Gibbons, S. (2018). Journey Mapping 101. Nielsen Norman Group (nngroup.com).
- Weighted scoring and metric trees are standard product-management practices; no specific source is cited for them.
- AGMP course materials were not supplied to this analysis, so no course page citations are included. Add them from the course documents if required.
