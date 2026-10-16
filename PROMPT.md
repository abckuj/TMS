# Research Brief — Uber Find My Ride (paste into Claude Code)

> Before starting: put the Google Form export in `data/raw/` (CSV/XLSX), any collected reviews in `data/raw/reviews*.csv`, and IIMA AGMP PDFs in `data/raw/iima/`. Read `CLAUDE.md` and the form scripts (`*.gs`) first.

## ROLE
Senior Product Data Analyst (Python/Pandas EDA) + UX Researcher (interviews, thematic analysis) + Product Manager (evidence-based discovery) + research consultant applying relevant IIM Ahmedabad AGMP frameworks.
Produce a professional, reproducible, evidence-based research report on **pickup coordination difficulties after a driver has been assigned**.
Do not fabricate survey responses, reviews, interview quotes, numerical results, statistical significance or citations.

## 1. DATA SOURCES
**Dataset A — Primary research:** Google Form responses (~26) exported into `data/raw/`. Read the actual data, inspect original questions, verify all counts.
Previously reported (provisional — verify; may come from different questions, some multi-select; check denominators, eligibility, overlaps, wording):
Entrance/gate confusion 13 · Incorrect/inconvenient pickup pin 12 · Long waiting 11 · Driver unable to find exact location 9 · Driver did not communicate clearly 8 · Driver asked rider to walk elsewhere 8 · Driver unable to access pickup point 4 · Repeated calls/messages 3 · Rider cancellation 6 · Driver cancellation 4 · Avg Uber rating ≈3.7/5.
If data is missing, report it and stop. Never substitute synthetic data.

**Dataset B — Secondary research:** public reviews/discussions on pickup coordination from: Google Play (Uber); App Store (Uber India); Reddit rider and driver communities; Rapido & Ola reviews (competitor comparison); Uber official help/pickup docs; airport/venue pickup guidance.
Use an attached review dataset first. If collecting, respect site restrictions/ToS, record exact URLs, no invented reviews. Keep India vs international separate.
Capture per review: ID, platform/source, company, review date, collection date, country/city, rating, rider/driver perspective, text or short excerpt, URL, relevance.
De-duplicate; document inclusion/exclusion criteria. Target 30–50 relevant reviews; if fewer, report the limitation. Purposive samples are not representative.

## 2. DATA AUDIT AND CLEANING
1. List input files/sheets. 2. Shape, columns, dtypes, first 5 rows. 3. Missing values, duplicates, inconsistent categories. 4. Single- vs multi-select questions. 5. Normalize multi-select without losing originals. 6. Preserve open-ended text. 7. Check eligibility per question. 8. Verify counts vs raw. 9. Data dictionary (question → variable). 10. Log cleaning decisions.
Never silently delete records. Output cleaned CSVs.

## 3. QUANTITATIVE EDA — PRIMARY
Python: Pandas, NumPy, Matplotlib (Plotly optional).
- **A. Descriptives:** totals & valid n per question; missingness; rating distribution/mean/median/SD; categorical frequencies; multi-select frequencies with correct denominators.
- **B. Pickup difficulties:** pin issues, gate confusion, waiting, driver can't find rider, restricted access, communication, rider walking, rider/driver cancellations. Don't add overlapping categories.
- **C. Journey stages:** 1 Driver assigned → 2 Pickup interpretation → 3 Driver approaches → 4 Coordination → 5 Meeting → 6 Outcome. Evidence matrix: frequency, denominator, source question, interpretation.
- **D. Locations:** airports, malls, rail/bus stations, office/IT parks, residential complexes, busy streets, markets. Compare only if respondent-level data allows; raw counts ≠ failure rates.
- **E. Cross-tabs (only if linkable):** location × difficulty; difficulty × rating; communication × cancellation; walking request × satisfaction; competitor preference × reason. Report small cells; no causal claims.
- **F. Stats:** descriptive primary; explain why inferential tests are inappropriate for n≈26 convenience sample.

## 4. QUALITATIVE — PRIMARY
Thematic analysis of all open-ended responses/interviews: familiarise → initial codebook → code (multi-code allowed) → themes → contradictions/positives → short accurate quotes → separate observation vs interpretation.
Seed codes: PIN_MISMATCH, GATE_CONFUSION, ACCESS_RESTRICTION, WAITING, COMMUNICATION, RIDER_WALKING, DRIVER_LOCATION_DIFFICULTY, CANCELLATION, FARE_TRUST, SUCCESSFUL_COORDINATION (refine from data). Don't infer driver motivation from rider accounts.
Table: Theme | Definition | # coded responses | Supporting evidence | Contradictory evidence | Interpretation | Confidence

## 5. SECONDARY REVIEW ANALYSIS
- Quant content analysis: counts by source, company, geography, perspective; theme & journey-stage frequencies; ratings by theme.
- Qual: recurring complaints; positives/recovery; driver operational constraints; separate location/communication/waiting/cancellation/fare; rider vs driver differences.
- Competitors (Uber/Rapido/Ola) only where equivalent evidence exists; distinguish perception, allegation, documented functionality, verified performance. No GPS-accuracy claims from preferences.

## 6. TRIANGULATION
Matrix: Problem theme | Primary survey | Primary interview | Secondary reviews | Official docs | Contradictions | Confidence | Further research.
Classify: multiple independent sources / one source / mixed / hypothesis / not supported. No numeric confidence without a transparent rubric.

## 7. IIMA FRAMEWORKS
From the provided AGMP materials, apply only relevant ones: Kotler/Keller research process, Design Thinking & Empathy Map, JTBD, Customer Journey Map, Service Blueprint, Operations Process Analysis, SERVQUAL gaps, Customer Value Proposition. Cite exact document + page/section; never fabricate citations.

## 8. VISUALIZATIONS (PNG → `charts/`)
1 Respondent overview · 2 Rating distribution · 3 Top difficulties (horizontal bar) · 4 Difficult locations · 5 Journey-stage friction · 6 Pickup outcomes · 7 Difficulty vs rating · 8 Review themes by source · 9 Rider vs driver themes · 10 Primary vs secondary themes.
Titles, denominators, source notes; note multi-select % can exceed 100%. Skip charts without data.

## 9. PM INTERPRETATION
Per finding: what observed; evidence; journey stage; stakeholder; possible business consequence; uncertainty; validation needed. Distinguish frequency, severity, business impact. Do not jump to solutions.

## 10. DELIVERABLES
- `outputs/EDA_Research_Report.pdf` (exec summary, method, data quality, descriptives, charts, themes, triangulation, limitations, conclusions)
- `notebooks/Uber_Primary_EDA.ipynb`
- `notebooks/Uber_Secondary_Review_Analysis.ipynb`
- `data/clean/Cleaned_Primary_Research.csv`
- `data/clean/Coded_Secondary_Reviews.csv`
- `outputs/Research_Evidence_Matrix.xlsx` (evidence, URLs, coding, confidence, open questions)
- `charts/*.png`
- `outputs/Assignment_Step4_Step5_Summary.md`
- `outputs/Research_Presentation.pptx` (< 5 min)
Claim a file exists only after verifying it.

## 11. EXECUTION
Execute code, inspect outputs, fix errors, generate deliverables — not just plans.
Phases: 1 Access & audit → 2 Cleaning & dictionary → 3 Primary quant EDA → 4 Primary qual → 5 Secondary reviews → 6 Triangulation → 7 IIMA frameworks → 8 Charts, report, deck.
After each phase: what was done, evidence available, what couldn't be verified. If blocked, name the exact blocker and request only the missing input.

## 12. FINAL QUALITY CHECK
Reconcile counts with sources · verify denominators · multi-select handled correctly · review URLs/attribution verified · no fabricated quotes · India vs international separated · sampling limits disclosed · charts match data · all files verified · no unsupported causal/market-wide claims.

**Begin with Phase 1.**
