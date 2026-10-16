"""Build outputs/Uber_TAM_SAM_SOM.xlsx (live formulas) for Uber Find My Ride.

Run from the repo root:  python3 scripts/build_tam_sam_som.py
All calculations are Excel formulas; inputs live only on the Assumptions sheet.
"""
from pathlib import Path
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

OUT = Path("outputs/Uber_TAM_SAM_SOM.xlsx")
OUT.parent.mkdir(exist_ok=True)

ILLUS = "Illustrative Assumption — Not Research Evidence"
RESEARCH = "Research-derived"
LOWCONF = "Low-confidence secondary estimate (range illustrative)"

HDR = PatternFill("solid", fgColor="1F3A5F")
HFONT = Font(bold=True, color="FFFFFF")
INPUT = Font(color="0000FF")
ILLUS_FILL = PatternFill("solid", fgColor="FFF2CC")
WRAP = Alignment(wrap_text=True, vertical="top")
thin = Side(style="thin", color="BBBBBB")
BOX = Border(left=thin, right=thin, top=thin, bottom=thin)


def header(ws, row, labels):
    for i, lab in enumerate(labels, 1):
        c = ws.cell(row=row, column=i, value=lab)
        c.fill, c.font, c.alignment, c.border = HDR, HFONT, WRAP, BOX


def widths(ws, ws_widths):
    for i, w in enumerate(ws_widths, 1):
        ws.column_dimensions[get_column_letter(i)].width = w


wb = Workbook()

# ------------------------------------------------------------------ README
ws = wb.active
ws.title = "README_Methodology"
lines = [
    ("Uber Find My Ride — TAM / SAM / SOM model (ILLUSTRATIVE, NOT A VALIDATED MARKET ESTIMATE)", True),
    ("Prepared for a product-management assignment. Built " + "2026-10-16" + ". Geography: India. Unit of analysis: annual ride-hailing pickup events (trips).", False),
    ("", False),
    ("WHY ILLUSTRATIVE", True),
    ("No credible public source gives Uber India's annual trip count, the share of pickups with coordination problems, or the effectiveness of any fix. "
     "Public research supplies distance (11.6 bn km in 2025), a company-claimed Rapido ride count and low-confidence market-share estimates. "
     "Every other input is an editable assumption labelled 'Illustrative Assumption — Not Research Evidence'. Results show what the funnel looks like IF those assumptions hold.", False),
    ("", False),
    ("DEFINITIONS (distinct quantities — never interchangeable)", True),
    ("TAM = total annual ride-hailing pickup events in India (all platforms) that could theoretically benefit from pickup-coordination improvement. Model!row 6.", False),
    ("SAM = the part of TAM Uber can serve: Uber's share x eligible ride categories x rollout geography. Model!row 7.", False),
    ("SOM = the part of SAM realistically obtainable within the time horizon (reach, Assumptions A6). Model!row 8.", False),
    ("Because Find My Ride improves an existing service, four further quantities are modelled separately:", False),
    ("  (1) Addressable annual pickup events = SAM / SOM.  (2) Events with relevant coordination problems = events x problem rate (Model rows 9-10).", False),
    ("  (3) Events the improvement could successfully address = problem events in SOM x effectiveness (row 11).  (4) Incremental economic value (rows 12-15).", False),
    ("", False),
    ("'TIM' — no use of the term was found in the project repository (searched .md and .gs files). TIM is not treated as TAM. "
     "If it appears in your earlier materials (e.g. Total Industry Market?), send the definition and it will be documented here.", False),
    ("", False),
    ("HOW TO USE", True),
    ("Edit blue cells on the Assumptions sheet only (columns D-F = Conservative / Base / Optimistic). Yellow rows are illustrative. All other sheets recalculate.", False),
    ("Conservative = smallest opportunity; Optimistic = largest. Sensitivity sheet shows the two-way grid and one-way swings around the Base case.", False),
    ("", False),
    ("KEY LIMITATIONS", True),
    ("1. Distance-to-trips conversion (A2) is the weakest link: Uber publishes km, not trips. A cross-check using Rapido's claimed rides is on Model rows 18-20.", False),
    ("2. Source figures were retrieved via web-search summaries; the original pages could not be opened from the build environment (network blocked). See 'Verification status' on Source_Registry.", False),
    ("3. Market shares are undated secondary estimates; Rapido's ride count is a company claim for one quarter, annualised (x4) ignoring seasonality; it includes bike/auto/cab.", False),
    ("4. The 26-person convenience survey is NOT used to set the problem rate (A7) — it is not representative and measures experiences, not trip-level incidence.", False),
    ("5. Value model counts only platform revenue from retained trips and rider time; it excludes driver earnings, brand effects, support-cost savings and implementation cost.", False),
    ("6. Results must not be quoted as Uber's market size or forecast.", False),
]
for r, (t, b) in enumerate(lines, 1):
    c = ws.cell(row=r, column=1, value=t)
    c.font = Font(bold=b, size=13 if r == 1 else 11)
    c.alignment = WRAP
ws.column_dimensions["A"].width = 150

# ------------------------------------------------------------ Source registry
sr = wb.create_sheet("Source_Registry")
header(sr, 1, ["ID", "Market input", "Value", "Unit", "Geography", "Reporting period", "Source URL",
               "Publication date", "Calculation / transformation applied", "Confidence", "Limitations",
               "Verification status", "Used in model?"])
SEARCH_ONLY = "Seen in web-search result summary 2026-10-16; page itself not opened (fetch blocked by network policy)."
src = [
    ("S1", "Uber ride distance in India", 11.6, "billion km (total trip distance)", "India", "Calendar 2025",
     "https://www.uber.com/en-IN/newsroom/how-india-ubered-in-2025-everyday-travel-extraordinary-scale",
     "January 2026 (per secondary coverage; exact date not verified)",
     "Used directly as A1; converted to trips by dividing by assumed km/trip (A2)",
     "Medium (company disclosure)", "Distance, not trips; includes all vehicle types; unclear whether pickup-approach km are excluded. Same page also states +26.5% vs 2024.",
     SEARCH_ONLY, "Yes — A1"),
    ("S2", "Uber ride distance in India (prior year)", 9.2, "billion km", "India", "Calendar 2024",
     "https://www.storyboard18.com/how-it-works/india-logs-9-2-bn-kilometers-with-uber-in-2024-report-52740.htm",
     "Not verified", "Context only (11.6 / 9.2 = +26%)", "Medium (media report of company data)",
     "Secondary reporting.", SEARCH_ONLY, "No (context)"),
    ("S3", "Rapido rides, Q2 FY25", 207, "million rides (quarter)", "India", "Q2 FY25 (Jul-Sep 2024)",
     "https://entrackr.com/news/rapido-claims-207-mn-rides-in-q2-fy25-with-25x-surge-in-gov-7579785",
     "Not verified (2024)", "x4 to annualise = 828 million rides/yr (cross-check only)", "Low-Medium (company claim)",
     "Company-claimed; one quarter annualised ignores seasonality/growth; includes bike, auto and cab, and may include non-comparable products.",
     SEARCH_ONLY, "Cross-check only — Model rows 18-20"),
    ("S4", "Share of India ride-hailing rides: Rapido ~50%, Uber ~40% (all vehicle types); Uber ~45% of four-wheeler segment",
     0.40, "share of rides (Uber, all vehicle types)", "India", "Not stated",
     "https://www.outlookbusiness.com/news/uber-pumps-3000-cr-into-india-arm-as-rapido-overtakes-in-total-rides",
     "Not verified", "Used as base A3 (0.40); cons 0.45 / opt 0.35 are illustrative", "Low (undated; underlying estimator unknown)",
     "Original estimator and period not confirmed; a different search result gave other shares.", SEARCH_ONLY, "Yes — A3"),
    ("S5", "Daily trips: Uber ~840k, Ola ~460k, Rapido ~320k", 840000, "trips/day (Uber)", "India", "Undated",
     "https://www.equentis.com/blog/?p=48722", "Not verified",
     "NOT used. 840k x 365 = ~307 million/yr is inconsistent with S1/S3 and is likely dated or on a different basis.",
     "Low", "Undated; conflicts with other sources; shown to document the range of uncertainty.", SEARCH_ONLY, "No (conflicting)"),
    ("S6", "CCPA warning to Uber/Ola on complaints about cancellations, cancellation charges, surge pricing and long waits; National Consumer Helpline April grievances: Ola 2,482, Uber 770",
     None, "n/a (qualitative; grievance counts)", "India", "2022",
     "https://www.moneylife.in/article/indian-regulator-warns-uber-ola-to-fix-customer-complaints-else-face-penal-action/67142.html",
     "2022 (exact date not verified)", "None — qualitative context for 'problem exists'", "Medium (regulatory action reported by media)",
     "Grievance counts are not a trip-level incidence rate; no share attributed to pickup coordination.", SEARCH_ONLY, "No (context)"),
    ("S7", "LocalCircles survey: 71% of customers report driver cancellation issues", 0.71, "share of survey respondents", "India", "2018",
     "https://qz.com/india/1472888/indians-are-sick-of-ola-ubers-surge-pricing-cancellations", "2018",
     "NOT used as a rate: perception survey, not per-trip incidence", "Low for sizing", "Dated (2018); self-selected online panel; measures experience not trip share.",
     SEARCH_ONLY, "No"),
    ("S8", "Uber official airport driver pages (e.g. LAX): queue/staging lots, designated pickup zones, advice to contact rider on crowded pickups",
     None, "n/a (documented functionality)", "International (US/Canada airports)", "Pages current at retrieval",
     "https://www.uber.com/global/en/r/airports/lax/driver-information/", "Not stated", "None — qualitative documentation; not India-specific",
     "Medium for documented process", "International; does not show performance or incidence.", SEARCH_ONLY, "No (qualitative)"),
]
for r, row in enumerate(src, 2):
    for c, v in enumerate(row, 1):
        cell = sr.cell(row=r, column=c, value=v)
        cell.alignment, cell.border = WRAP, BOX
widths(sr, [6, 38, 12, 22, 16, 18, 52, 22, 40, 20, 46, 40, 22])
sr.freeze_panes = "C2"

# ---------------------------------------------------------------- Assumptions
asm = wb.create_sheet("Assumptions")
asm["A1"] = "Assumption inputs — edit blue cells only. Yellow = Illustrative Assumption, not research evidence."
asm["A1"].font = Font(bold=True, size=12)
asm["A2"] = "Scenario direction: Conservative = smallest opportunity, Optimistic = largest. Time horizon for SOM: 3 years (editable label, applied via A6)."
header(asm, 4, ["ID", "Parameter", "Unit", "Conservative", "Base", "Optimistic", "Evidence status", "Source / rationale (why needed)"])
A = [
    ("A1", "Uber India annual trip distance", "billion km", 11.6, 11.6, 11.6, RESEARCH, "S1. Same in all scenarios."),
    ("A2", "Average rider trip distance (converts km to trips)", "km per trip", 17.5, 12, 8, ILLUS,
     "Uber publishes km, not trips. Needed to get a trip count. Conservative value 17.5 is chosen so Uber trips ~ 0.66 bn, matching the Rapido-based cross-check (rows 18-20); base/optimistic assume shorter trips."),
    ("A3", "Uber share of India ride-hailing trips (all platforms)", "share", 0.45, 0.40, 0.35, LOWCONF,
     "S4 base 0.40. Needed to scale Uber trips up to an all-platform TAM. Higher share = smaller TAM (conservative)."),
    ("A4", "Share of Uber trips in ride categories eligible for the improvement", "share", 0.50, 0.70, 0.90, ILLUS,
     "Needed because rollout may exclude some categories (e.g. bike, shared, intercity). No public split used."),
    ("A5", "Share of eligible trips within initial rollout geography", "share", 0.40, 0.60, 0.80, ILLUS,
     "Needed because launch would not cover all cities. S1 only names top cities qualitatively."),
    ("A6", "Reach achieved within time horizon (3 years): share of SAM", "share", 0.10, 0.25, 0.40, ILLUS,
     "Needed to turn SAM (serviceable) into SOM (obtainable). No adoption evidence exists."),
    ("A7", "Coordination-problem rate: share of pickups with a relevant problem", "share of trips", 0.05, 0.10, 0.15, ILLUS,
     "No credible published trip-level rate found (S6/S7 are not rates). Deliberately NOT taken from the 26-person survey."),
    ("A8", "Effectiveness: share of problem events the improvement resolves", "share", 0.20, 0.35, 0.50, ILLUS,
     "Unknown until tested. Placeholder to show sensitivity."),
    ("A9", "Share of resolved problem events that would otherwise have lost the trip (cancel/no-show)", "share", 0.20, 0.30, 0.40, ILLUS,
     "Needed to link coordination problems to lost revenue. Not measured."),
    ("A10", "Average fare per trip", "INR", 200, 250, 300, ILLUS, "No fare source gathered; editable placeholder."),
    ("A11", "Platform take rate on fare", "share", 0.15, 0.20, 0.25, ILLUS, "No India take-rate source gathered; editable placeholder."),
    ("A12", "Rider minutes saved per resolved problem event", "minutes", 3, 5, 8, ILLUS, "Placeholder for rider-side benefit (hours, not monetised)."),
    ("R1", "Rapido rides in Q2 FY25 (cross-check)", "million rides", 207, 207, 207, RESEARCH + " (company claim)", "S3."),
    ("R2", "Rapido share of India ride-hailing rides (cross-check)", "share", 0.50, 0.50, 0.50, LOWCONF, "S4."),
]
for i, row in enumerate(A):
    r = 5 + i
    for c, v in enumerate(row, 1):
        cell = asm.cell(row=r, column=c, value=v)
        cell.alignment, cell.border = WRAP, BOX
        if c in (4, 5, 6):
            cell.font = INPUT
            if isinstance(v, float) and v < 1:
                cell.number_format = "0.0%" if row[2].startswith("share") else "0.00"
        if row[6] == ILLUS:
            cell.fill = ILLUS_FILL
widths(asm, [6, 56, 16, 14, 12, 14, 34, 90])
asm.freeze_panes = "D5"
# row map: A1=5 ... A12=16, R1=17, R2=18
ROW = {row[0]: 5 + i for i, row in enumerate(A)}

# ------------------------------------------------------------------- Model
md = wb.create_sheet("Model")
md["A1"] = "TAM / SAM / SOM and incremental-value model — all cells are formulas on the Assumptions sheet (annual, India)"
md["A1"].font = Font(bold=True, size=12)
header(md, 4, ["Row", "Quantity", "Unit", "Conservative", "Base", "Optimistic", "Formula logic"])


def f(col, expr):
    return expr.replace("{c}", col)


def a(idn):
    return f"Assumptions!{{c}}{ROW[idn]}"


model_rows = [
    (5, "Uber India annual trips (derived from km)", "million trips", f"={a('A1')}*1000/{a('A2')}", "A1 bn km x 1000 / km per trip (A2)"),
    (6, "TAM — all-platform India ride-hailing pickup events", "million events", f"={{c}}5/{a('A3')}", "Uber trips / Uber share (A3)"),
    (7, "SAM — Uber-serviceable pickup events", "million events", f"={{c}}6*{a('A3')}*{a('A4')}*{a('A5')}", "TAM x Uber share x eligible categories x rollout geography"),
    (8, "SOM — obtainable within horizon", "million events", f"={{c}}7*{a('A6')}", "SAM x reach (A6)"),
    (9, "Events with coordination problems — within SAM", "million events", f"={{c}}7*{a('A7')}", "SAM x problem rate (A7)"),
    (10, "Events with coordination problems — within SOM", "million events", f"={{c}}8*{a('A7')}", "SOM x problem rate (A7)"),
    (11, "Events the improvement could successfully address (SOM)", "million events", f"={{c}}10*{a('A8')}", "Problem events in SOM x effectiveness (A8)"),
    (12, "Trips retained (would otherwise be lost)", "million trips", f"={{c}}11*{a('A9')}", "Addressed events x A9"),
    (13, "Incremental platform revenue", "INR million", f"={{c}}12*{a('A10')}*{a('A11')}", "Retained trips x fare x take rate"),
    (14, "Incremental platform revenue", "INR crore", "={c}13/10", "1 crore = 10 million"),
    (15, "Rider time saved", "million hours", f"={{c}}11*{a('A12')}/60", "Addressed events x minutes / 60"),
]
for r, name, unit, expr, logic in model_rows:
    md.cell(row=r, column=1, value=r)
    md.cell(row=r, column=2, value=name)
    md.cell(row=r, column=3, value=unit)
    for col in "DEF":
        c = md[f"{col}{r}"]
        c.value = f(col, expr)
        c.number_format = "#,##0.0" if r not in (14,) else "#,##0.00"
    md.cell(row=r, column=7, value=logic)
    for cc in range(1, 8):
        md.cell(row=r, column=cc).border = BOX
        md.cell(row=r, column=cc).alignment = WRAP

md["A17"] = "Cross-check: is the km-to-trips conversion plausible? (not used in the funnel)"
md["A17"].font = Font(bold=True)
xrows = [
    (18, "Rapido rides, annualised (Q2 FY25 x 4)", "million rides", f"={a('R1')}*4", "S3 x 4; ignores seasonality; company claim"),
    (19, "Implied Uber trips if Uber/Rapido ride ratio = A3/R2", "million trips", f"={{c}}18*{a('A3')}/{a('R2')}", "Rapido annualised x (Uber share / Rapido share)"),
    (20, "Model Uber trips vs cross-check (ratio)", "x", "={c}5/{c}19", "1.0 = agreement; far from 1.0 = conversion A2 needs work"),
]
for r, name, unit, expr, logic in xrows:
    md.cell(row=r, column=1, value=r)
    md.cell(row=r, column=2, value=name)
    md.cell(row=r, column=3, value=unit)
    for col in "DEF":
        c = md[f"{col}{r}"]
        c.value = f(col, expr)
        c.number_format = "#,##0.00" if r == 20 else "#,##0.0"
    md.cell(row=r, column=7, value=logic)
widths(md, [6, 58, 16, 16, 14, 16, 70])

# ------------------------------------------------------------- Sensitivity
sn = wb.create_sheet("Sensitivity")
sn["A1"] = "Sensitivity around the BASE case — incremental platform revenue (INR crore, annual, within SOM)"
sn["A1"].font = Font(bold=True, size=12)
sn["A2"] = "Table 1: two-way grid. Rows = coordination-problem rate (A7); columns = effectiveness (A8). All other inputs at Base."
rates = [0.02, 0.05, 0.10, 0.15, 0.20]
effs = [0.10, 0.20, 0.35, 0.50, 0.70]
sn["A4"] = "Problem rate \\ Effectiveness"
sn["A4"].font = Font(bold=True)
for j, e in enumerate(effs):
    c = sn.cell(row=4, column=2 + j, value=e)
    c.number_format, c.font = "0%", Font(bold=True, color="0000FF")
for i, rt in enumerate(rates):
    rr = 5 + i
    c = sn.cell(row=rr, column=1, value=rt)
    c.number_format, c.font = "0%", Font(bold=True, color="0000FF")
    for j in range(len(effs)):
        col = get_column_letter(2 + j)
        cell = sn.cell(row=rr, column=2 + j,
                       value=f"=Model!$E$8*$A{rr}*{col}$4*Assumptions!$E${ROW['A9']}*Assumptions!$E${ROW['A10']}*Assumptions!$E${ROW['A11']}/10")
        cell.number_format = "#,##0.00"

sn["A12"] = "Table 2: one-way swing. Each row swaps ONE input to its Conservative / Optimistic value; all others at Base (INR crore)."
header(sn, 13, ["Input swapped", "Conservative value -> result", "Base result", "Optimistic value -> result", "Swing (opt - cons)", "Note"])
base = "Model!$E$14"
one_way = [
    ("A2 km per trip", f"={base}*Assumptions!$E${ROW['A2']}/Assumptions!$D${ROW['A2']}", f"={base}*Assumptions!$E${ROW['A2']}/Assumptions!$F${ROW['A2']}", "Trips scale with 1 / km per trip"),
    ("A4 eligible categories", None, None, ""),
    ("A5 rollout geography", None, None, ""),
    ("A6 reach in horizon", None, None, ""),
    ("A7 problem rate", None, None, ""),
    ("A8 effectiveness", None, None, ""),
    ("A9 trips otherwise lost", None, None, ""),
    ("A10 average fare", None, None, ""),
    ("A11 take rate", None, None, ""),
]
mult_ids = [None, "A4", "A5", "A6", "A7", "A8", "A9", "A10", "A11"]
for i, (label, lo, hi, note) in enumerate(one_way):
    r = 14 + i
    idn = mult_ids[i]
    if idn:
        lo = f"={base}*Assumptions!$D${ROW[idn]}/Assumptions!$E${ROW[idn]}"
        hi = f"={base}*Assumptions!$F${ROW[idn]}/Assumptions!$E${ROW[idn]}"
        note = "Linear (multiplicative) input"
    sn.cell(row=r, column=1, value=label)
    sn.cell(row=r, column=2, value=lo).number_format = "#,##0.00"
    sn.cell(row=r, column=3, value=f"={base}").number_format = "#,##0.00"
    sn.cell(row=r, column=4, value=hi).number_format = "#,##0.00"
    sn.cell(row=r, column=5, value=f"=D{r}-B{r}").number_format = "#,##0.00"
    sn.cell(row=r, column=6, value=note)
r = 14 + len(one_way)
sn.cell(row=r, column=1, value="A3 Uber share")
sn.cell(row=r, column=2, value=f"={base}").number_format = "#,##0.00"
sn.cell(row=r, column=3, value=f"={base}").number_format = "#,##0.00"
sn.cell(row=r, column=4, value=f"={base}").number_format = "#,##0.00"
sn.cell(row=r, column=5, value=f"=D{r}-B{r}").number_format = "#,##0.00"
sn.cell(row=r, column=6, value="No effect on SAM/SOM/value (share cancels); affects TAM only")
r += 2
sn.cell(row=r, column=1, value="All inputs Conservative").font = Font(bold=True)
sn.cell(row=r, column=2, value="=Model!D14").number_format = "#,##0.00"
sn.cell(row=r + 1, column=1, value="All inputs Optimistic").font = Font(bold=True)
sn.cell(row=r + 1, column=2, value="=Model!F14").number_format = "#,##0.00"
sn.cell(row=r + 2, column=1, value="Reading: results are products of uncertain inputs; the range between all-conservative and all-optimistic spans orders of magnitude, so only the structure of the funnel, not the level, is informative.").alignment = WRAP
widths(sn, [34, 26, 16, 26, 20, 56])

OUT_PATH = OUT
wb.save(OUT_PATH)
print("saved", OUT_PATH)
