# Uber Find My Ride: Submission QA

_Run 2026-10-17. Deck: `outputs/Uber_FindMyRide_Final_Presentation.pptx` (built by `scripts/build_final_deck.py`, which asserts the numbers below against the source files on every run)._

## 1. Number consistency (source files vs brief)
| Item | Brief | Source file | Result |
|---|---|---|---|
| Survey rows received / valid Uber users | 27 / 24 | `Cleaned_Primary_Research.csv` | Match |
| Gate/entrance confusion | 13/24 | Q6 column | Match |
| Long waiting | 11/24 | Q6 column | Match |
| Incorrect/inconvenient pickup pin | 10/24 | Q6 column | Match |
| Driver could not find exact location | 9/24 | Q6 column | Match |
| Rider asked to walk elsewhere | 8/24 | Q6 column | Match |
| Secondary reviews analysed | 33 | `Secondary_Reviews_Verified.csv` | Match; 33 unique IDs, 0 duplicate texts |
| Cancellation / fare trust / communication / waiting | 22 / 9 / 9 / 8 of 33 | `theme_codes` | Match |
| Driver location difficulty / gate / pin | 4 / 2 / 2 of 33 | `theme_codes` | Match |
| TAM / SAM / SOM (base) | ~2,417M / ~406M / ~101.5M | `Uber_TAM_SAM_SOM.xlsx` Model rows 6-8 | Match (2,416.7 / 406.0 / 101.5) |
| Potentially improved events | ~3.55M | Model row 11 | Match (3.553M) |
| Incremental platform revenue | ~INR 5.33 crore | Model row 14 | Match (5.329) |
| Workbook formulas | no errors | all 109 formulas | 0 errors, 0 uncached |

Primary and secondary counts are never combined into one denominator (n=24 and n=33 are always shown separately).

## 2. Secondary evidence verification
- **Exact verified date range: 12 Sep 2026 to 14 Oct 2026 (33 days, about five weeks).** The deck states this on slides 2, 4, 5 and 8's source line and does not claim six months.
- Dates come from Apple's customer-reviews RSS feed (`updated` field). Every review falls inside the requested 17 Apr to 17 Oct 2026 window; the window itself is not covered (Apple's feed holds only the latest 500 reviews).
- **URLs:** Apple provides no per-review permalink. The CSV records the feed URL, the app listing URL and Apple's review ID. No per-review URLs were invented.
- Duplicates: 0 duplicate review IDs, 0 duplicate texts.
- Pickup relevance: all 33 were screened "include". 23 of 33 carry at least one coordination-related code (gate, pin, driver location, waiting, communication, walking, vehicle ID, false arrival, access). The other 10 are mainly cancellation or fare complaints, which are on the edge of "find my ride". They are retained in the cancellation and fare counts and not presented as pickup-location evidence.
- Fare-only complaints: 0 reviews are fare-only (all 9 fare-coded reviews also carry another code; 5 also mention cancellation). Fare trust is shown separately from pickup-coordination evidence on slide 4.
- No review is described as "verified" beyond its date and ID. Review text is Apple-published, reviewer identity is unverified.
- Not used: 24 of the 57 screening "include" IDs could not be matched to the feed.
- Not accessible: Google Play (no review text), Reddit (HTTP 403).

## 3. Claims the deck deliberately does not make
- Reviews are not described as representative of Uber users.
- No claim that gate or pin confusion causes cancellations (0 of 22 cancellation reviews carry a gate or pin code).
- Survey and review frequencies are not used to estimate pickup-problem incidence in the market model.
- Revenue is labelled incremental platform revenue, not profit.
- No power calculation is claimed for the experiment sample; the 20% median coordination-time reduction is labelled a proposed decision criterion.
- No feature is preselected.

## 4. Deck structure and format
- 9 slides: Slides 1-8 main, Slide 9 references. Matches the brief's structure.
- Opened and exported all 9 slides to images through PowerPoint (COM) with no errors; slides were visually inspected after two layout adjustments (table column width, font sizes).
- Charts are existing project charts (`q6_difficulties.png`, `secondary_theme_frequency.png`, `primary_vs_secondary_themes.png`). Chart title on the secondary chart corrected from "cancellation and waiting dominate" to "cancellation dominates" (fare trust and communication rank above waiting).
- Slide 5's comparison chart has small axis text but is legible at slide size; it carries a "not directly comparable" label.
- The illustrative-model disclaimer is visible on Slide 6 as a tagline plus the assumption list.
- Speaker notes present on all 9 slides (word counts 58, 95, 81, 73, 99, 121, 119, 70, 16).

## 5. Timing
At about 150 words per minute, the Slide 1-8 notes (716 words) take about 286 seconds (4.8 minutes). Allowing for slide transitions and pauses this fits a five-minute slot. Per-slide estimates are in `Uber_FindMyRide_Final_Speaker_Notes.md` (23, 38, 32, 29, 40, 48, 48, 28 seconds against budgets of 20, 35, 40, 40, 50, 45, 45, 25; slides 1, 2, 6, 7, 8 run a few seconds over budget, slides 3-5 under, total within 300 s). Actual pace should be rehearsed once.

## 5b. Framework integration check (added 2026-10-17)
- JTBD (slides 1, 8), customer journey map (slides 3-5; primary and secondary shown separately), weighted matrix (slide 6), Build-Measure-Learn and metric tree (slide 7), decision chain (slide 8). Still 8 main slides plus references.
- Weighted matrix: six criteria, written 1-3 rubric, base weights 25/20/15/15/15/10. Weighted scores: H1 2.45, H2 2.15, H3 1.70. Rank checked under four weightings (base, equal, impact-heavy, scope-excluded): H1 first in all four; the script asserts this and would stop if it failed. Lead over H3 narrows to 0.4 under impact-heavy weights.
- All framework scores, weights and the stage mapping are labelled analytical judgements, not measured data, on slides 2, 3, 6 and in the appendix.
- Primary (n=24) and secondary (n=33) are never pooled; the journey mapping, scores and triangulation keep separate denominators.
- Framework references (Christensen et al. 2016; Ulwick 2016; Ries 2011; Gibbons, Nielsen Norman Group, 2018) are cited from memory as published works and have not been re-checked online; AGMP course pages were not supplied, so none are cited. Verify bibliographic details before submission.
- Rendering re-checked through PowerPoint export after fixes (decision-chain arrow tips clipped text; adjusted).

## 6. Discrepancies and how each was handled
| # | Discrepancy | Handling |
|---|---|---|
| 1 | `PROGRESS.md` was stale (said survey, EDA, secondary and deck were not done; said remote ended at `b4aa8c4`) | Rewritten; remote now confirmed at `fa49d39`, local secondary commit `402fd78` not pushed |
| 2 | No separate secondary source register | `Secondary_Reviews_Verified.csv` serves as the record (review ID, date, source, feed URL, listing URL, geography, stakeholder, rating, text, codes). Gap documented: no per-review permalink |
| 3 | Slide 9 (added in `Insights_v2`) lacked speaker notes | Final deck has notes on every slide, including the references slide |
| 4 | References slide lacked secondary evidence | Added, with verified/unverified split |
| 5 | Date coverage could be read as six months | Exact dates (12 Sep to 14 Oct 2026) shown; "NOT the full six months" stated on Slide 2 |
| 6 | Workbook `README_Methodology` and PROGRESS referred to a "26-person survey" | Left unchanged (workbook retained as instructed; no formula errors). Current figures are 27 received / 24 valid. Consider editing the README text before submission |
| 7 | `Source_Registry` row S6 appears to have a column shift (a value sits in the wrong column) | Cosmetic; the row is context only and not used in the model. Not edited |
| 8 | Registry lists old context (CCPA 2022, LocalCircles 2018) | Marked as un-used context on Slide 9 |

## 7. Unresolved verification limits
- Market-model inputs (Uber 11.6 bn km, Rapido 207M rides, market shares) came from web-search summaries; original pages were not opened. Labelled "not independently verified" on Slide 9.
- The km-to-trips conversion and all problem, effectiveness, reach, fare and take-rate inputs are illustrative assumptions. Base-case trips are 1.46x a Rapido-based cross-check.
- Secondary evidence is Apple India only, five weeks, 1 driver review, mostly 1-star, city rarely stated.

## 8. Preservation
Original `Uber_FindMyRide_Insights.pptx`, `Uber_FindMyRide_Insights_v2.pptx`, `Uber_TAM_SAM_SOM.xlsx`, primary data, primary EDA notebook and source files are unchanged. Changes in the working tree: the secondary notebook was re-executed after a chart-title fix (`notebooks/Uber_Secondary_Reviews.ipynb`, `outputs/secondary_theme_frequency.png`), and new files were added. No commit or push was made.
