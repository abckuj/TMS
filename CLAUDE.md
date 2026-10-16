# Uber "Find My Ride" — Pickup Coordination Research

Product-management research project (IIMA AGMP). Full brief: `PROMPT.md`.

## Rules
- Never fabricate survey responses, reviews, quotes, counts, statistics or citations. If data is missing, stop and name the missing input.
- Question wording source of truth: the Google Form scripts in `uber-pickup-survey/create_uber_form.gs` and `ride-pickup-survey/create_form.gs`. Read them before building the data dictionary.
- Multi-select questions: report counts with the correct denominator (respondents who answered that question); never sum overlapping categories into "affected users".
- Small convenience sample (~26): descriptive statistics only; no causal or market-wide claims.
- Keep India and international review evidence separate; record source URL for every review.
- Never silently drop records; log every cleaning decision.
- Claim a file exists only after verifying it.

## Layout
- `data/raw/` — survey export (CSV/XLSX), reviews, IIMA PDFs (git-ignored)
- `data/clean/` — Cleaned_Primary_Research.csv, Coded_Secondary_Reviews.csv
- `notebooks/` — Uber_Primary_EDA.ipynb, Uber_Secondary_Review_Analysis.ipynb
- `charts/` — PNG figures
- `outputs/` — PDF report, evidence matrix XLSX, summary MD, PPTX

## Working style (token saving)
- Run one or two phases per session; start each session with: "Read CLAUDE.md and existing outputs, continue from Phase N."
- Keep phase reports to ~5 lines; detail goes into files, not chat.
