# Project progress — Uber Find My Ride

_Last updated 2026-10-17. Replaces the 2026-10-16 version, which predated the primary EDA, secondary research and final deck._

## Current state
| Workstream | Status | Key files |
|---|---|---|
| Primary survey cleaning and EDA (27 rows received, 24 valid Uber users) | Done | `notebooks/Uber_Primary_EDA.ipynb`, `data/clean/Cleaned_Primary_Research.csv`, `Cleaning_Log.csv`, `Count_Reconciliation.csv`, `Data_Dictionary.csv`, `charts/*.png` |
| Secondary app-store review analysis (33 reviews, verified dates 12 Sep 2026 to 14 Oct 2026) | Done (pilot sample; see limits) | `data/clean/Secondary_Reviews_Verified.csv`, `notebooks/Uber_Secondary_Reviews.ipynb`, `outputs/secondary_*.png` |
| Primary vs secondary triangulation | Done | `outputs/Triangulation_Matrix.csv`, `outputs/primary_vs_secondary_themes.png` |
| TAM/SAM/SOM workbook (illustrative) | Done; values re-verified 2026-10-17 | `outputs/Uber_TAM_SAM_SOM.xlsx`, `charts/TAM_SAM_SOM_funnel.png`, `scripts/build_tam_sam_som.py` |
| Problem prioritisation (H1/H2/H3) | Done | `outputs/Uber_FindMyRide_Problem_Prioritization.csv` |
| Validation experiment design | Done (proposal only) | `outputs/Uber_FindMyRide_Experiment_Plan.md` |
| Final presentation (9 slides: 8 + references) with speaker notes | Done | `outputs/Uber_FindMyRide_Final_Presentation.pptx`, `outputs/Uber_FindMyRide_Final_Speaker_Notes.md`, built by `scripts/build_final_deck.py` |
| Frameworks appendix (JTBD, journey map, weighted matrix with sensitivity, Build-Measure-Learn, metric tree) | Done; scores are analytical judgements | `outputs/Uber_FindMyRide_Frameworks_Appendix.md` |
| Submission QA | Done | `outputs/Uber_FindMyRide_Submission_QA.md` |

Earlier decks are preserved unchanged: `outputs/Uber_FindMyRide_Insights.pptx` (original 5-minute deck) and `Uber_FindMyRide_Insights_v2.pptx` (original + one secondary slide).

## Git state (checked 2026-10-17)
- Branch `claude/ride-pickup-research-survey-2xg76o`. Remote `origin` (github.com/abckuj/TMS) is at `fa49d39`.
- Local commit `402fd78` (secondary research) is **not pushed** (branch is 1 commit ahead).
- Final-deck files, speaker notes, prioritisation, experiment plan, QA file and this update are **uncommitted** at the time of writing. Nothing has been committed or pushed without explicit authorisation.
- `data/raw/` (survey export) is git-ignored by design.

## Known limitations
**Secondary evidence**
- Only Apple App Store (India) was accessible. Google Play showed no review text; Reddit returned HTTP 403.
- Apple's feed returns only the latest 500 reviews, so the evidence covers 12 Sep 2026 to 14 Oct 2026 (about five weeks), not the requested 17 Apr to 17 Oct 2026 window.
- Apple provides no per-review URL; provenance is the feed URL plus Apple's review ID.
- 24 of the 57 reviews marked "include" in `Secondary_Review_Screening.csv` could not be matched to the feed and were not used.
- 1 driver review and 32 rider reviews; reviews skew to 1-star. The sample is purposive, not representative.

**Primary evidence**: 24 valid respondents from a convenience sample; multi-select options overlap and must not be summed.

**Market model**
- Source pages could not be opened (network policy); inputs come from web-search summaries (see `Source_Registry`).
- Uber publishes km (11.6 bn, 2025), not trips. Base case is 1.46x a Rapido-based cross-check (Model row 20).
- Problem rate, effectiveness, reach, eligibility, rollout, fare, take rate are Illustrative Assumptions. Survey and review frequencies are deliberately not used to set the problem rate.
- `README_Methodology` in the workbook still says "26-person survey"; the current figures are 27 received / 24 valid (workbook left unchanged; see QA file).
- "TIM" does not appear in the repository and is not treated as TAM.
