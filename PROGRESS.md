# Project progress — Uber Find My Ride

_Last updated 2026-10-16_

## Done and verified (cloud session)
| Item | Path | Status |
|---|---|---|
| TAM/SAM/SOM workbook (5 sheets, 109 live formulas, 0 errors after LibreOffice recalculation; base case hand-checked) | `outputs/Uber_TAM_SAM_SOM.xlsx` | Done — **illustrative model, not a validated market estimate** |
| Funnel chart | `charts/TAM_SAM_SOM_funnel.png` | Done |
| Build scripts | `scripts/build_tam_sam_som.py`, `scripts/make_funnel_chart.py` | Done (rerun to regenerate) |

## NOT done — needs files that exist only on the user's computer
The survey export, `notebooks/Uber_Primary_EDA.ipynb` and `data/clean/Cleaned_Primary_Research.csv` were never pushed to GitHub (checked 2026-10-16: branch ends at `b4aa8c4`).
- PermissionError diagnosis, seven bar charts (Q2,Q4,Q5,Q6,Q7,Q9,Q10), two heatmaps
- Secondary review dataset
- Findings interpretation (needs verified survey counts)
- PowerPoint (needs survey charts and verified findings; will not be built on unverified numbers)

## Known limitations of the market model
- Source pages could not be opened (network policy); inputs come from web-search summaries. See `Source_Registry` "Verification status".
- Uber publishes km (11.6 bn, 2025), not trips; km-to-trips conversion is an assumption. Base case is 1.46x a Rapido-based cross-check (Model row 20).
- Problem rate, effectiveness, reach, eligibility, rollout, fare, take rate are all labelled Illustrative Assumptions. The 26-person survey is deliberately not used for the problem rate.
- "TIM" does not appear anywhere in the repository; it is not treated as TAM. Definition needed from the user.
