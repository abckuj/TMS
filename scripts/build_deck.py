"""Build outputs/Uber_FindMyRide_Insights.pptx (5-minute walkthrough deck).

Numbers on the slides are computed from data/clean/Cleaned_Primary_Research.csv (base = included Uber users);
charts come from charts/*.png (produced by notebooks/Uber_Primary_EDA.ipynb and scripts/make_funnel_chart.py).
Market-model numbers are read from outputs/Uber_TAM_SAM_SOM.xlsx (cached values; illustrative model).
Run from the project root: python scripts/build_deck.py
"""
from pathlib import Path
import pandas as pd
import openpyxl
from PIL import Image
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR

ROOT = Path(__file__).resolve().parents[1]
CH, OUT = ROOT / 'charts', ROOT / 'outputs'

# ---------- data (computed, not typed) ----------
c = pd.read_csv(ROOT / 'data/clean/Cleaned_Primary_Research.csv')
u = c[c['include_in_analysis'] & (c['respondent_group'] == 'uber_user')]
N = len(u)
n_rows, n_test_or_nonuser = len(c), len(c) - N
pct = lambda n: f'{100 * n / N:.0f}%'
cnt = lambda col: int(u[col].sum())
Q3_yes = int((u['Q3'] != 'No').sum())
mean_rating = u['Q2_rating'].mean()
q6 = {k: cnt(col) for k, col in {
    'gate': 'Q6__confusion_about_which_entrance_or_gate_t', 'wait': 'Q6__long_waiting_time',
    'pin': 'Q6__pickup_pin_showed_an_incorrect_or_inconv', 'find': 'Q6__driver_could_not_find_my_exact_location',
    'walk': 'Q6__driver_asked_me_to_walk_to_another_locat'}.items()}
late = cnt('Q9__worried_about_being_late')
q10 = u['Q10'].value_counts()
cancelled = int(q10.get('I cancelled the booking', 0) + q10.get('Driver cancelled the booking', 0))
met_delay = int(q10.get('Successfully met the driver after a delay', 0))
met_ok = int(q10.get('Successfully met the driver without much delay', 0))
q5_conf = int((u['Q5'] == 'Sometimes confusing or inaccurate').sum())
q5_good = int((u['Q5'] == 'Very helpful and accurate').sum())
call = cnt('Q7__called_and_politely_asked_for_directions')
unclear = cnt('Q7__did_not_communicate_clearly')
helped_mp = cnt('Q7__helped_identify_a_suitable_meeting_point')
extra_money = int((u['Q11'] == 'Yes').sum())
rival = int(u['Q14'].isin(['Rapido', 'Ola']).sum())
mall_wait = int((u['Q4__shopping_mall'].astype(bool) & u['Q6__long_waiting_time'].astype(bool)).sum())
mall_n = cnt('Q4__shopping_mall')
res_wait = int((u['Q4__residential_complex'].astype(bool) & u['Q6__long_waiting_time'].astype(bool)).sum())
res_n = cnt('Q4__residential_complex')
assert (N, q6['gate'], late) == (24, 13, 15), 'cleaned data changed - re-check slide text'

wb = openpyxl.load_workbook(OUT / 'Uber_TAM_SAM_SOM.xlsx', data_only=True)
m = {str(r[0]): r for r in wb['Model'].iter_rows(values_only=True) if r[0] is not None}
tam, sam, som = (float(m[k][4]) for k in ('6', '7', '8'))
prob_som, addr, rev_cr = float(m['10'][4]), float(m['11'][4]), float(m['14'][4])
rev_lo, rev_hi = float(m['14'][3]), float(m['14'][5])

# ---------- styling ----------
INK, MUTED, ACC, SOFT, WARN = (RGBColor(0x1F, 0x29, 0x33), RGBColor(0x6B, 0x77, 0x85), RGBColor(0x2A, 0x6F, 0x97),
                               RGBColor(0xF1, 0xF5, 0xF9), RGBColor(0xB4, 0x53, 0x09))
prs = Presentation()
prs.slide_width, prs.slide_height = Inches(13.333), Inches(7.5)
BLANK = prs.slide_layouts[6]


def text(slide, x, y, w, h, paras, size=18, color=INK, bold=False, anchor=MSO_ANCHOR.TOP, align=PP_ALIGN.LEFT):
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame
    tf.word_wrap, tf.vertical_anchor = True, anchor
    tf.margin_left = tf.margin_right = Inches(0.05)
    for i, p in enumerate(paras if isinstance(paras, list) else [paras]):
        para = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        para.alignment, para.space_after = align, Pt(8)
        run = para.add_run()
        run.text = p
        run.font.size, run.font.bold, run.font.color.rgb, run.font.name = Pt(size), bold, color, 'Calibri'
    return tb


def picture(slide, path, x, y, w, h):
    iw, ih = Image.open(path).size
    s = min(w / iw, h / ih)
    pw, ph = iw * s, ih * s
    slide.shapes.add_picture(str(path), Inches(x + (w - pw) / 2), Inches(y + (h - ph) / 2), Inches(pw), Inches(ph))


def new_slide(title, source, notes, tag=None):
    s = prs.slides.add_slide(BLANK)
    bar = s.shapes.add_shape(1, 0, 0, Inches(0.18), prs.slide_height)
    bar.fill.solid(); bar.fill.fore_color.rgb = ACC; bar.line.fill.background()
    text(s, 0.5, 0.3, 12.3, 1.0, title, size=28, bold=True, anchor=MSO_ANCHOR.MIDDLE)
    if tag:
        text(s, 0.5, 1.2, 12.3, 0.4, tag, size=13, color=WARN, bold=True)
    text(s, 0.5, 7.0, 12.3, 0.4, 'Source: ' + source, size=10, color=MUTED)
    s.notes_slide.notes_text_frame.text = notes
    return s


def bullets(slide, items, x=7.4, y=1.7, w=5.5, h=5.1, size=17):
    text(slide, x, y, w, h, ['•  ' + t for t in items], size=size)


SURVEY = f'Uber Ride & Pickup Experience Survey, n={N} Uber users (convenience sample)'

# 1 Title
s = prs.slides.add_slide(BLANK)
bg = s.shapes.add_shape(1, 0, 0, prs.slide_width, prs.slide_height)
bg.fill.solid(); bg.fill.fore_color.rgb = INK; bg.line.fill.background()
text(s, 0.8, 2.0, 11.7, 1.6, 'Uber "Find My Ride"', size=48, bold=True, color=RGBColor(255, 255, 255))
text(s, 0.8, 3.4, 11.7, 1.2, 'Why riders and drivers struggle to find each other at pickup, and what the early evidence says',
     size=24, color=RGBColor(0xCB, 0xD5, 0xE1))
text(s, 0.8, 5.4, 11.7, 1.0, ['Product-management research project, IIMA AGMP',
                              f'Progress update: primary survey (n={N}) and an illustrative market-sizing model'],
     size=16, color=RGBColor(0x94, 0xA3, 0xB8))
s.notes_slide.notes_text_frame.text = (
    '[0:00-0:15] Hi, this is a quick walkthrough of my Uber "Find My Ride" project. The question: why do riders and '
    'drivers struggle to find each other at pickup, and is there a product opportunity? I will cover what I did, the '
    'main insights, a rough market sizing, and what is still to do.')

# 2 Approach
s = new_slide('What I did: a survey, cleaned with every decision logged',
              'notebooks/Uber_Primary_EDA.ipynb; data/clean/Cleaning_Log.csv; uber-pickup-survey/create_uber_form.gs',
              '[0:15-0:55] I built a Google Form on pickup experience and got 27 responses. One person had never used '
              f'Uber, and two looked like test entries with keyboard-mash text, so the analysis base is {N} Uber users. '
              'I did not delete anything: those rows are flagged and every cleaning step is in a log. Question wording '
              'comes straight from the form script. Because multi-select questions overlap, I report each option over '
              f'the {N} people who answered, and never add options together. This is a small convenience sample, so '
              'everything here is descriptive, not market-wide.')
bullets(s, [f'{n_rows} responses received; {N} Uber users analysed',
            f'{n_test_or_nonuser} rows excluded but kept in the file and flagged: 1 non-user, 2 suspected test entries (keyboard text)',
            'Question wording and options parsed from the form script, not retyped',
            f'Multi-select shares use n={N} as denominator and overlap, so they are never summed',
            'Convenience sample: descriptive only, no causal or market-wide claims'], x=0.7, y=1.7, w=7.2, size=19)
box = s.shapes.add_shape(1, Inches(8.5), Inches(1.9), Inches(4.3), Inches(4.4))
box.fill.solid(); box.fill.fore_color.rgb = SOFT; box.line.fill.background()
text(s, 8.7, 2.0, 3.9, 4.2, ['Data used so far', f'Survey Excel export ({n_rows} rows x 29 columns)',
                             'Illustrative TAM/SAM/SOM workbook', '',
                             'Not yet analysed', 'App Store review pages (India and US)'], size=15, color=INK)

# 3 Q6
s = new_slide(f'Difficulty is the norm: {Q3_yes} of {N} have booked from a crowded place',
              SURVEY + ', Q3 and Q6 (multi-select, shares overlap)',
              f'[0:55-1:40] Of the {N} riders, {Q3_yes} have booked from a crowded or complex location, and only 2 said '
              f'they had no difficulties. The most common problem is not the driver being far away. It is confusion '
              f'about which entrance or gate to use, {q6["gate"]} of {N}. Next is long waiting at {q6["wait"]}, then a '
              f'wrong or inconvenient pickup pin at {q6["pin"]}. Overall rating averages {mean_rating:.2f} out of 5, '
              'which is moderate rather than low. Percentages overlap because people tick several options.')
picture(s, CH / 'q6_difficulties.png', 0.5, 1.5, 6.7, 5.4)
bullets(s, [f'Entrance/gate confusion leads: {q6["gate"]} of {N} ({pct(q6["gate"])})',
            f'Long waiting {q6["wait"]} ({pct(q6["wait"])}); wrong pickup pin {q6["pin"]} ({pct(q6["pin"])})',
            f'Driver could not find spot: {q6["find"]}; asked rider to walk: {q6["walk"]}',
            f'Mean overall rating {mean_rating:.2f} / 5: moderate, not low'])

# 4 heatmap
s = new_slide('Where it happens: difficulty is reported across many location types',
              SURVEY + ', Q4 x Q6 respondent-level cross-tab. Cells are counts; small cells are anecdotal',
              f'[1:40-2:25] This heatmap crosses where people had difficulty with what went wrong. Each cell counts '
              f'respondents who ticked both. Shopping malls and crowded markets have the darkest cells, but they are also the most-ticked locations. For example, '
              f'{mall_wait} of the {mall_n} people who reported mall difficulty also reported long waiting, and '
              f'{res_wait} of {res_n} for residential complexes. Treat this as a pattern to test, not a failure rate, '
              'because the cells are tiny and these are counts of respondents, not of rides.',
              tag='Pattern to test, not a measured failure rate (cells are small)')
picture(s, CH / 'heatmap_location_x_difficulty.png', 0.4, 1.6, 8.3, 5.3)
bullets(s, [f'Malls: long waiting {mall_wait} of {mall_n} who reported mall difficulty',
            f'Residential complexes: long waiting {res_wait} of {res_n}',
            'Gate confusion is highest at crowded markets and railway/bus stations',
            'Counts are respondents, not rides, so locations cannot be ranked by failure rate'],
        x=8.9, y=1.8, w=4.1, size=16)

# 5 impact
s = new_slide(f'The cost to riders: time pressure, and {cancelled} of {N} pickups ended in cancellation',
              SURVEY + ', Q9 (multi-select) and Q10 (single-select, shares add to 100%)',
              f'[2:25-3:10] The biggest impact is time pressure: {late} of {N} said they worried about being late, '
              f'ahead of frustration or stress at 6 each. On outcomes, only {met_ok} of {N} met their driver without '
              f'much delay. {met_delay} met after a delay, and {cancelled} ended in a cancellation, either the rider or '
              'the driver. Q10 is single-select so those shares do add up. Cancellations and delay are where revenue '
              'and trust leak.')
picture(s, CH / 'q9_feelings.png', 0.4, 1.5, 6.2, 5.3)
picture(s, CH / 'q10_outcomes.png', 6.8, 1.5, 6.2, 5.3)

# 6 app + coordination
s = new_slide('The app helps only partly: calls fill the last few metres',
              SURVEY + ', Q5 (single-select) and Q7 (multi-select, shares overlap)',
              f'[3:10-3:50] On the app itself, {q5_conf} of {N} find the pickup display sometimes confusing or '
              f'inaccurate, and only {q5_good} call it very helpful and accurate. Coordination falls back on manual '
              f'contact: {call} say the driver called for directions, {unclear} say the driver did not communicate '
              f'clearly, and only {helped_mp} say the driver helped identify a suitable meeting point. The pattern '
              'suggests a gap in how the app helps riders and drivers agree on an exact meeting point.')
picture(s, CH / 'q5_app_helpfulness.png', 0.4, 1.6, 6.2, 2.6)
picture(s, CH / 'q7_driver_coordination.png', 6.8, 1.5, 6.2, 4.4)
text(s, 0.5, 4.5, 6.0, 2.4, [f'{q5_conf} of {N} ({pct(q5_conf)}) find the app sometimes confusing or inaccurate',
                             f'Only {helped_mp} of {N} saw the driver help pick a meeting point'], size=16)

# 7 funnel
s = new_slide('Market size (illustrative): a large pool, with a small addressable slice',
              'outputs/Uber_TAM_SAM_SOM.xlsx (Model, Assumptions, Source_Registry); Uber India newsroom 2025 (11.6 bn km)',
              f'[3:50-4:30] To size the opportunity I built a TAM, SAM, SOM model. TAM is about {tam:,.0f} million '
              f'pickup events a year across India ride-hailing. SAM, the part Uber can serve, is about {sam:,.0f} '
              f'million, and SOM within three years is about {som:,.1f} million. After applying a problem rate and an '
              f'effectiveness rate, about {addr:.1f} million events could be addressed, worth roughly {rev_cr:.1f} '
              'crore rupees a year in the base case. Important: only the distance figure and market shares are '
              'sourced. Problem rate, effectiveness, reach, fare and take rate are my assumptions, so this shows '
              'sensitivity and is not a market estimate. The range runs from a very small to a very large number.',
              tag='ILLUSTRATIVE MODEL. NOT A VALIDATED MARKET ESTIMATE')
picture(s, CH / 'TAM_SAM_SOM_funnel.png', 0.4, 1.7, 8.2, 5.2)
bullets(s, [f'TAM {tam:,.0f}M, SAM {sam:,.0f}M, SOM {som:,.1f}M events a year (base)',
            f'{addr:.1f}M events addressable; value about INR {rev_cr:.1f} crore (range {rev_lo:.2f} to {rev_hi:.0f})',
            'Sourced: Uber 11.6 bn km and market shares only',
            'Assumptions, not evidence: problem rate, effectiveness, reach, fare, take rate',
            'Survey was not used to set the problem rate'], x=8.8, y=1.8, w=4.2, size=15)

# 8 so-what
s = new_slide('So what: three hypotheses to test, plus the limits of this evidence',
              SURVEY + '; outputs/Uber_TAM_SAM_SOM.xlsx. Hypotheses are not findings',
              f'[4:30-5:00] Putting it together. First, the problem is mostly about the exact meeting point, not just '
              f'the pin. Second, communication is manual and cancellations follow delay. Third, {rival} of {N} named '
              f'Rapido or Ola as preferred, and {extra_money} of {N} reported extra-money requests. That is a '
              'separate issue, so I keep it out of the pickup claim. Limits: small sample, one convenience group, '
              'and the market model is illustrative. Next: analyse the App Store reviews for India versus '
              'international, then validate with larger or better-targeted data. Thanks for watching.')
text(s, 0.6, 1.5, 6.3, 0.5, 'Hypotheses to test', size=20, bold=True, color=ACC)
text(s, 0.6, 2.1, 6.3, 4.8, [
    '1. Riders and drivers need an exact meeting point (gate or entrance), not just a pin',
    '2. In-app guidance and messaging could replace manual calls and cut delay-driven cancellations',
    f'3. Related but separate: {extra_money} of {N} report extra-money requests; {rival} of {N} prefer Rapido or Ola. Tracked, not part of the pickup claim'],
     size=16)
text(s, 7.2, 1.5, 5.8, 0.5, 'Limits and next steps', size=20, bold=True, color=WARN)
text(s, 7.2, 2.1, 5.8, 4.8, [f'n={N}, convenience sample: descriptive only',
                             'Survey counts are respondents, not rides, so no failure rates',
                             'Market model: key inputs are assumptions',
                             'Next: App Store reviews (India vs international kept separate)',
                             'Next: validate with a larger or targeted sample'], size=16)

# 9 references
s = new_slide('References and evidence trail', 'All paths are relative to the project root',
              'Reference slide, not part of the 5-minute talk track. Pause here if you want to show the evidence trail.')
refs = [
    f'Primary data: data/raw/Uber Ride & Pickup Experience Survey (Responses).xlsx ("Form Responses 1", {n_rows} rows x 29 columns; raw folder is git-ignored)',
    'Question wording: uber-pickup-survey/create_uber_form.gs (Google Form builder script)',
    'Analysis: notebooks/Uber_Primary_EDA.ipynb; outputs data/clean/Cleaned_Primary_Research.csv, Cleaning_Log.csv, Count_Reconciliation.csv, Data_Dictionary.csv',
    'Charts: charts/*.png (bar charts and heatmaps from the notebook; funnel from scripts/make_funnel_chart.py)',
    'Market model: outputs/Uber_TAM_SAM_SOM.xlsx. Sources: Uber India newsroom "How India Ubered in 2025" (11.6 bn km); Entrackr (Rapido 207M rides, Q2 FY25); Outlook Business (market shares). Retrieved via web-search summaries, not independently verified',
    'Rebuild this deck: python scripts/build_deck.py']
text(s, 0.6, 1.5, 12.2, 5.4, ['•  ' + r for r in refs], size=15)

OUT.mkdir(exist_ok=True)
path = OUT / 'Uber_FindMyRide_Insights.pptx'
prs.save(path)
print('saved', path, '| slides:', len(prs.slides))
