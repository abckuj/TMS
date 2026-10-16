"""Build the final 9-slide presentation plus companion files.

Outputs (all in outputs/):
  Uber_FindMyRide_Final_Presentation.pptx, Uber_FindMyRide_Final_Speaker_Notes.md,
  Uber_FindMyRide_Problem_Prioritization.csv, Uber_FindMyRide_Frameworks_Appendix.md
Every number is read from the source files and asserted against the brief; nothing is typed in by hand.
Framework scores are analytical judgements (rubric and weights below), not measured data.
Original decks (Insights, Insights_v2) are never modified.
Run from the project root: python scripts/build_final_deck.py
"""
from pathlib import Path
import pandas as pd
import openpyxl
from PIL import Image
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR

ROOT = Path(__file__).resolve().parents[1]
CH, OUT, CLEAN = ROOT / 'charts', ROOT / 'outputs', ROOT / 'data/clean'

# ---------- data, verified against the brief ----------
pri_all = pd.read_csv(CLEAN / 'Cleaned_Primary_Research.csv')
pri = pri_all[pri_all['include_in_analysis'] & (pri_all['respondent_group'] == 'uber_user')]
N, N_ROWS = len(pri), len(pri_all)
P = lambda col: int(pri[col].astype(float).sum())
prim = {'gate': P('Q6__confusion_about_which_entrance_or_gate_t'), 'wait': P('Q6__long_waiting_time'),
        'pin': P('Q6__pickup_pin_showed_an_incorrect_or_inconv'), 'find': P('Q6__driver_could_not_find_my_exact_location'),
        'walk': P('Q6__driver_asked_me_to_walk_to_another_locat')}
assert (N_ROWS, N) == (27, 24)
assert prim == {'gate': 13, 'wait': 11, 'pin': 10, 'find': 9, 'walk': 8}, prim

sec = pd.read_csv(CLEAN / 'Secondary_Reviews_Verified.csv', encoding='utf-8-sig', dtype={'review_id': str})
M = len(sec)
codes = sec['theme_codes'].str.split(';')
S = lambda t: int(codes.apply(lambda x: t in x).sum())
secn = {'canc': S('CANCELLATION'), 'fare': S('FARE_TRUST'), 'comm': S('COMMUNICATION'), 'wait': S('WAITING'),
        'loc': S('DRIVER_LOCATION_DIFFICULTY'), 'gate': S('GATE_CONFUSION'), 'pin': S('PIN_MISMATCH')}
assert M == 33 and not sec['review_id'].duplicated().any() and not sec['review_text'].duplicated().any()
assert secn == {'canc': 22, 'fare': 9, 'comm': 9, 'wait': 8, 'loc': 4, 'gate': 2, 'pin': 2}, secn
D0, D1 = sec['pub_date'].min(), sec['pub_date'].max()
assert '2026-04-17' <= D0 and D1 <= '2026-10-17'
fmt = lambda d: pd.Timestamp(d).strftime('%d %b %Y').lstrip('0')
SPAN_DAYS = (pd.Timestamp(D1) - pd.Timestamp(D0)).days + 1
DATES = f'{fmt(D0)} to {fmt(D1)}'
canc_mask = codes.apply(lambda x: 'CANCELLATION' in x)
canc_fare = int((canc_mask & codes.apply(lambda x: 'FARE_TRUST' in x)).sum())
canc_gatepin = int((canc_mask & codes.apply(lambda x: bool({'GATE_CONFUSION', 'PIN_MISMATCH'} & set(x)))).sum())
drivers = int((sec['stakeholder'] == 'driver').sum())

q10 = pri['Q10'].value_counts()
rider_cancel = int(q10.get('I cancelled the booking', 0)); driver_cancel = int(q10.get('Driver cancelled the booking', 0))
prim_cancel = rider_cancel + driver_cancel
met_delay = int(q10.get('Successfully met the driver after a delay', 0))
prim_call = P('Q7__called_and_politely_asked_for_directions')
prim_unclear = P('Q7__did_not_communicate_clearly')
prim_late = P('Q9__worried_about_being_late')
assert (prim_call, prim_unclear, prim_late, prim_cancel) == (11, 8, 15, 10)

STAGES = ['1 Driver assigned', '2 Pickup interpretation', '3 Driver approaches', '4 Coordination', '5 Meeting', '6 Outcome']
sec_stage = sec['journey_stages'].str.split(';').explode().value_counts().reindex(STAGES).fillna(0).astype(int)

wb = openpyxl.load_workbook(OUT / 'Uber_TAM_SAM_SOM.xlsx', data_only=True)
mm = {str(r[0]): r for r in wb['Model'].iter_rows(values_only=True) if r[0] is not None}
tam, sam, som = (float(mm[k][4]) for k in ('6', '7', '8'))
addr, rev_cr = float(mm['11'][4]), float(mm['14'][4])
assert (round(tam), round(sam), round(som, 1), round(addr, 2), round(rev_cr, 2)) == (2417, 406, 101.5, 3.55, 5.33)

# ---------- weighted prioritisation (analytical judgement; rubric and weights are explicit) ----------
CRIT = [  # key, name, base weight, scoring guide
 ('evid', 'Strength of supporting evidence', .25, '3 = consistent across both lenses and sizeable; 1 = thin, indirect or single-source'),
 ('impact', 'Observed customer impact', .20, '3 = severe or costly outcome reported (e.g. lost trip, safety, large delay); 1 = mild or not reported'),
 ('freq', 'Frequency in the relevant samples', .15, '3 = among the most-cited items in the sample(s); 1 = rarely cited'),
 ('scope', 'Relevance to Find My Ride scope', .15, '3 = directly about locating/meeting at pickup; 1 = mostly outside pickup coordination'),
 ('interv', 'Potential for product intervention', .15, '3 = clear levers within product design; 1 = driven mainly by factors outside product control'),
 ('conf', 'Confidence (inverse of remaining uncertainty)', .10, '3 = low uncertainty; 1 = high uncertainty (key assumptions untested)'),
]
KEYS = [c[0] for c in CRIT]
SHORT = ['evidence', 'impact', 'frequency', 'scope', 'intervention', 'confidence']
HYP = {
 'H1': ('Meeting-point ambiguity',
        'Riders and drivers lack a shared understanding of the exact, physically accessible pickup location, particularly at complex venues.',
        [2, 2, 3, 3, 3, 2],
        [f'Evidence 2: primary gate/entrance confusion {prim["gate"]}/{N}, wrong pin {prim["pin"]}/{N}, driver could not find location {prim["find"]}/{N}; secondary only gate {secn["gate"]}/{M}, pin {secn["pin"]}/{M}, driver location {secn["loc"]}/{M}.',
         f'Impact 2: {prim_late}/{N} worried about being late; delay and walking reported, but not a lost trip by itself.',
         f'Frequency 3: gate confusion is the most-ticked primary difficulty ({prim["gate"]}/{N}).',
         'Scope 3: directly about meeting at pickup.',
         'Intervention 3: information design levers exist without presupposing a feature.',
         'Confidence 2: mainly one small convenience survey.']),
 'H2': ('Coordination friction',
        'Riders and drivers rely on calls, messages and additional walking to resolve uncertainty, increasing pickup effort and delay.',
        [2, 2, 2, 3, 2, 2],
        [f'Evidence 2: waiting {prim["wait"]}/{N}, drivers called for directions {prim_call}/{N}, unclear communication {prim_unclear}/{N}; secondary communication {secn["comm"]}/{M}, waiting {secn["wait"]}/{M}.',
         'Impact 2: extra effort and delay.',
         'Frequency 2: common in both, but below gate confusion in the survey and below cancellation in reviews.',
         'Scope 3: coordination is the find-my-ride mechanism.',
         'Intervention 2: levers exist but calls/waiting have other causes.',
         'Confidence 2: cause of calls and waiting not separated from other causes.']),
 'H3': ('Cancellation-related friction',
        'Some pickup cancellations may be associated with coordination difficulties; other causes include driver availability, incentives, traffic, fares and operations.',
        [1, 3, 3, 1, 1, 1],
        [f'Evidence 1 (for a coordination link): {canc_gatepin} of {secn["canc"]} cancellation reviews carry a gate or pin code; {canc_fare} also carry a fare code.',
         f'Impact 3: lost trips and fees; primary {prim_cancel}/{N} outcomes were cancellations (rider {rider_cancel}, driver {driver_cancel}).',
         f'Frequency 3: most-cited review theme ({secn["canc"]}/{M}), but reviews are self-selected.',
         'Scope 1: many causes lie outside meeting-point information.',
         'Intervention 1: causes are mixed (availability, incentives, fares, operations).',
         'Confidence 1: causal path untested.']),
}
WEIGHTS = {'Base case': [c[2] for c in CRIT],
           'Equal weights': [1 / 6] * 6,
           'Impact-heavy': [.15, .35, .15, .10, .15, .10],
           'Scope excluded': [.30, .25, .20, 0.0, .15, .10]}
for k, w in WEIGHTS.items():
    assert abs(sum(w) - 1) < 1e-9, k
score = lambda hid, w: sum(a * b for a, b in zip(HYP[hid][2], w))
RESULT = {k: {h: score(h, w) for h in HYP} for k, w in WEIGHTS.items()}
RANK = {k: sorted(HYP, key=lambda h: -r[h]) for k, r in RESULT.items()}
assert all(r[0] == 'H1' for r in RANK.values()), 'H1 is not first under every weighting: revise the recommendation before building'
base = RESULT['Base case']
rank_base = {h: i + 1 for i, h in enumerate(RANK['Base case'])}
gap_h3_impact = RESULT['Impact-heavy']['H1'] - RESULT['Impact-heavy']['H3']
ROLE = {'H1': 'Recommended initial priority', 'H2': 'Related mechanism to investigate',
        'H3': 'Downstream outcome requiring causal validation'}
SCALE = ('Each criterion scored 1-3 (see rubric). Weighted score = sum(weight x score), range 1-3. Scores and weights are analytical judgements, '
         'not measured data. Rank checked under four weightings.')
rows = []
for h, (name, defn, sc, why) in HYP.items():
    r = {'hypothesis_id': h, 'hypothesis': name, 'definition': defn}
    r.update({f'score_{k}': s for k, s in zip(KEYS, sc)})
    r.update({f'weighted_{k.lower().replace(" ", "_").replace("-", "_")}': round(RESULT[k][h], 2) for k in WEIGHTS})
    r.update({'rank_base_case': rank_base[h], 'role': ROLE[h], 'rationale': ' | '.join(why), 'method_note': SCALE})
    rows.append(r)
wrow = {'hypothesis_id': 'WEIGHTS', 'hypothesis': 'Base-case weights', 'definition': '; '.join(f'{c[1]} {c[2]:.0%}' for c in CRIT)}
pd.DataFrame([wrow] + rows).to_csv(OUT / 'Uber_FindMyRide_Problem_Prioritization.csv', index=False, encoding='utf-8-sig')

# ---------- styling & helpers ----------
INK, MUTED, ACC, SOFT, WARN, WHITE = (RGBColor(0x1F, 0x29, 0x33), RGBColor(0x6B, 0x77, 0x85), RGBColor(0x2A, 0x6F, 0x97),
                                      RGBColor(0xF1, 0xF5, 0xF9), RGBColor(0xB4, 0x53, 0x09), RGBColor(255, 255, 255))
PEACH = RGBColor(0xFD, 0xEB, 0xD0)
prs = Presentation()
prs.slide_width, prs.slide_height = Inches(13.333), Inches(7.5)
BLANK = prs.slide_layouts[6]
NOTES = {}


def text(slide, x, y, w, h, paras, size=16, color=INK, bold=False, anchor=MSO_ANCHOR.TOP, align=PP_ALIGN.LEFT, space=6):
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame
    tf.word_wrap, tf.vertical_anchor = True, anchor
    tf.margin_left = tf.margin_right = Inches(0.05)
    for i, p in enumerate(paras if isinstance(paras, list) else [paras]):
        para = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        para.alignment, para.space_after = align, Pt(space)
        head = isinstance(p, tuple)
        run = para.add_run()
        run.text = p[0] if head else p
        run.font.size, run.font.name = Pt(size), 'Calibri'
        run.font.bold = bold or head
        run.font.color.rgb = (p[1] if head else color)
    return tb


def box(slide, x, y, w, h, fill=SOFT, shape=1):
    b = slide.shapes.add_shape(shape, Inches(x), Inches(y), Inches(w), Inches(h))
    b.fill.solid(); b.fill.fore_color.rgb = fill; b.line.fill.background()
    return b


def line(slide, x1, y1, x2, y2):
    c = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Inches(x1), Inches(y1), Inches(x2), Inches(y2))
    c.line.color.rgb = MUTED; c.line.width = Pt(1.5)


def picture(slide, path, x, y, w, h):
    iw, ih = Image.open(path).size
    s = min(w / iw, h / ih)
    pw, ph = iw * s, ih * s
    slide.shapes.add_picture(str(path), Inches(x + (w - pw) / 2), Inches(y + (h - ph) / 2), Inches(pw), Inches(ph))


def new_slide(n, title, source, notes, tag=None):
    s = prs.slides.add_slide(BLANK)
    bar = s.shapes.add_shape(1, 0, 0, Inches(0.18), prs.slide_height)
    bar.fill.solid(); bar.fill.fore_color.rgb = ACC; bar.line.fill.background()
    text(s, 0.5, 0.25, 12.3, 0.95, title, size=26, bold=True, anchor=MSO_ANCHOR.MIDDLE)
    if tag:
        text(s, 0.5, 1.18, 12.3, 0.4, tag, size=13, color=WARN, bold=True)
    text(s, 0.5, 7.0, 12.3, 0.4, 'Source: ' + source, size=10, color=MUTED)
    s.notes_slide.notes_text_frame.text = notes
    NOTES[n] = notes
    return s


def bl(slide, items, x, y, w, h, size=16):
    text(slide, x, y, w, h, ['•  ' + t for t in items], size=size)


SURVEY = f'Uber Ride & Pickup Experience Survey, n={N} valid Uber users (convenience sample)'
REVIEWS = f'Apple App Store India reviews, {DATES}, n={M} (purposive, not representative)'
JOB = 'When I have booked a ride from a busy or complex place, I want to meet my driver quickly and with certainty, so I can start my trip on time without stress.'

# ---- Slide 1 (JTBD: core customer job)
n1 = ('I will show why riders and drivers struggle to find each other at pickup, and which problem to take into discovery first. '
      'I frame it with the job the rider is hiring Uber to do at that moment: meet my driver quickly and with certainty from a busy place. '
      'Evidence, priority and experiment all hang off that job.')
s = prs.slides.add_slide(BLANK)
bg = s.shapes.add_shape(1, 0, 0, prs.slide_width, prs.slide_height)
bg.fill.solid(); bg.fill.fore_color.rgb = INK; bg.line.fill.background()
text(s, 0.8, 1.0, 11.7, 1.6, 'Uber Find My Ride: The Pickup Coordination Problem', size=42, bold=True, color=WHITE)
text(s, 0.8, 2.8, 11.7, 1.4, [('Research question', RGBColor(0x94, 0xA3, 0xB8)),
                              'Why do Uber riders and drivers struggle to find each other at pickup, and which problem should be prioritised for product discovery?'],
     size=21, color=RGBColor(0xCB, 0xD5, 0xE1))
text(s, 0.8, 4.5, 11.7, 1.4, [('Core customer job (Jobs to Be Done)', RGBColor(0x94, 0xA3, 0xB8)), JOB], size=21, color=WHITE)
text(s, 0.8, 6.3, 11.7, 0.6, 'AI Product Management assignment, IIMA AGMP', size=16, color=RGBColor(0x94, 0xA3, 0xB8))
s.notes_slide.notes_text_frame.text = n1; NOTES[1] = n1

# ---- Slide 2 (methodology + framework map)
n2 = (f'Two lenses: a survey with 27 responses, {N} valid Uber users, and {M} App Store reviews from India, collected {fmt(D0)} to '
      f'{fmt(D1)}, about five weeks, not six months. Both are small and self-selected, so they show what to test, not how common anything is. '
      'I use five light frameworks, each for a reason: jobs to be done to define the need, a journey map to locate the friction, '
      'a weighted matrix to make prioritisation explicit, build-measure-learn to keep the experiment small, and a metric tree to tie it to business outcomes.')
s = new_slide(2, 'Methodology: two research lenses, five frameworks to turn them into a decision',
              'data/clean/Cleaning_Log.csv; data/clean/Secondary_Reviews_Verified.csv; outputs/Uber_FindMyRide_Frameworks_Appendix.md', n2)
box(s, 0.5, 1.4, 6.0, 3.0)
text(s, 0.65, 1.45, 5.7, 2.9, [('Primary survey', ACC), f'{N_ROWS} responses received; {N} valid Uber users after documented exclusions (rows kept and flagged)',
                               'Respondent-level multi-select counts; options overlap and are never summed', 'Convenience sample'], size=14, space=5)
box(s, 6.8, 1.4, 6.0, 3.0)
text(s, 6.95, 1.45, 5.7, 2.9, [('Secondary app-store reviews', WARN), f'{M} Apple App Store (India) reviews; verified dates {DATES} ({SPAN_DAYS} days), NOT the full six months',
                               'Apple feed only; Google Play and Reddit not accessible; no per-review URL',
                               f'{drivers} driver and {M - drivers} rider reviews; self-selected, skewed to 1-star'], size=14, space=5)
FW = [('Jobs to Be Done', 'Defines the need', 'Slides 1, 8'), ('Journey map', 'Locates friction', 'Slides 3-5'),
      ('Weighted matrix', 'Ranks hypotheses', 'Slide 6'), ('Build-Measure-Learn', 'Structures the test', 'Slide 7'),
      ('Metric tree', 'Links to outcomes', 'Slides 7-8')]
text(s, 0.5, 4.55, 12.3, 0.4, 'Frameworks used (framework scores are analytical judgements, not measured data)', size=14, bold=True, color=ACC)
for k, (a, b, c) in enumerate(FW):
    x = 0.5 + k * 2.5
    box(s, x, 5.0, 2.3, 1.8)
    text(s, x + 0.08, 5.05, 2.15, 1.7, [(a, ACC), b, c], size=14, space=3)

# ---- Slide 3 (primary + journey)
PS = [('1 Driver assigned', 'not measured in survey'),
      ('2 Pickup interpretation', f'gate/entrance confusion {prim["gate"]}; wrong pin {prim["pin"]}'),
      ('3 Driver approaches', f'long waiting {prim["wait"]}'),
      ('4 Coordination', f'driver called for directions {prim_call}; unclear communication {prim_unclear}'),
      ('5 Meeting', f'driver could not find location {prim["find"]}; asked to walk {prim["walk"]}'),
      ('6 Outcome', f'cancelled {prim_cancel} (rider {rider_cancel}, driver {driver_cancel}); met after delay {met_delay}')]
n3 = (f'Here is the survey on the customer journey. Friction piles up early, at stage two, where riders interpret the pickup point: gate confusion '
      f'{prim["gate"]} of {N}, wrong pin {prim["pin"]}. Then waiting {prim["wait"]}, and calls for directions {prim_call}. I used a journey map because it shows where the '
      'breakdown starts, not just what is reported. The stage mapping is my judgement, and these are respondent counts, not rates. '
      'The implication: the earliest place to intervene is shared understanding of where to meet.')
s = new_slide(3, f'Primary survey: friction starts at "interpreting the pickup point" (n={N})',
              SURVEY + ', Q6, Q7, Q10 (multi-select except Q10; counts overlap). Stage mapping is analyst judgement', n3)
picture(s, CH / 'q6_difficulties.png', 0.4, 1.4, 6.6, 5.5)
text(s, 7.2, 1.4, 5.7, 0.4, 'Customer journey: respondents reporting each friction', size=15, bold=True, color=ACC)
text(s, 7.2, 1.9, 5.7, 4.9, [f'{a}: {b}' for a, b in PS], size=14, space=8)

# ---- Slide 4 (secondary + journey)
n4 = (f'Reviews map differently. Of {M}, {secn["canc"]} mention cancellation, and the journey view shows them clustering at the outcome stage and during the approach. '
      f'Waiting and communication appear again, about a quarter each. Fare disputes, {secn["fare"]} reviews, I keep separate, since they are not about finding the rider. '
      f'Gate and pin appear in only {secn["gate"]} reviews each. Reviews describe how a trip ended, so I treat cancellation as a symptom to measure, not diagnose.')
s = new_slide(4, f'Secondary reviews: cancellation dominates and the friction clusters late (n={M})',
              REVIEWS + '; themes and stages multi-coded', n4)
picture(s, OUT / 'secondary_theme_frequency.png', 0.4, 1.4, 6.6, 5.5)
text(s, 7.2, 1.4, 5.7, 0.4, f'Journey stages touched by reviews (of {M}; overlap)', size=15, bold=True, color=ACC)
text(s, 7.2, 1.85, 5.7, 3.0, [f'{st}: {int(sec_stage[st])}' for st in STAGES], size=14, space=4)
bl(s, [f'Fare trust {secn["fare"]}/{M} kept separate from pickup evidence ({canc_fare} also mention cancellation)',
       f'Gate {secn["gate"]} and pin {secn["pin"]}: few; {drivers} driver review only'], 7.2, 4.85, 5.7, 2.0, size=14)

# ---- Slide 5 (triangulation)
n5 = ('Side by side, waiting and communication appear in both lenses, which gives some confidence they are real. The survey asks where and how pickups get hard, '
      'so it surfaces stage two: gates and pins. Reviews capture bad outcomes, so cancellation dominates. Fewer gate and pin mentions in reviews does not '
      'contradict the survey: different questions, people and weeks. What I cannot say is how common any of this is, or that gate or pin confusion causes '
      'cancellations. Nothing in the reviews links them. Use the survey to choose where to dig, and the reviews to choose what to track.')
s = new_slide(5, 'Triangulation: convergence on waiting and communication, different emphasis elsewhere',
              'outputs/Triangulation_Matrix.csv; ' + SURVEY + '; ' + REVIEWS + '. Percentages use different denominators and are not directly comparable', n5)
picture(s, OUT / 'primary_vs_secondary_themes.png', 0.3, 1.3, 7.4, 5.6)
bl(s, ['Converge: waiting and communication appear in both lenses',
       'Differ: the survey shows friction at stage 2 (interpreting the pickup point); reviews show late stages (approach, outcome)',
       'Why: question wording, review self-selection, geography, collection period, coding',
       f'Cannot conclude: prevalence, representativeness, or that gate/pin confusion causes cancellation ({canc_gatepin} of {secn["canc"]} cancellation reviews carry a gate or pin code)'],
   7.6, 1.6, 5.3, 5.3, size=15)

# ---- Slide 6 (weighted matrix + market)
n6 = ('To decide what to prioritise I used a weighted matrix, because it forces me to show my reasoning. Six criteria, weights on the slide, each hypothesis scored one to three. '
      'These are my judgements, not measurements. Meeting-point ambiguity scores highest, and stays first under three alternative weightings. Coordination friction is the '
      'related mechanism. Cancellation scores high on impact and frequency, but evidence linking it to coordination is weak and many causes sit outside scope, so it is an '
      'outcome to measure, not the first bet. On market size, this is an illustrative scenario: about 2.4 billion pickup events at the top, 3.5 million potentially improved, '
      'roughly five crore rupees of platform revenue, resting on unvalidated assumptions. Not a forecast, not profit.')
s = new_slide(6, 'Prioritised opportunity: H1 ranks first on a transparent weighted matrix',
              'outputs/Uber_FindMyRide_Problem_Prioritization.csv; outputs/Uber_FindMyRide_Frameworks_Appendix.md; outputs/Uber_TAM_SAM_SOM.xlsx. Scores are analytical judgements',
              n6, tag='Market model: illustrative scenario based on published inputs and unvalidated assumptions, not a market forecast.')
tbl = s.shapes.add_table(4, 4, Inches(0.5), Inches(1.7), Inches(7.4), Inches(2.5)).table
for j, (hd, wd) in enumerate([('Hypothesis', 3.2), ('Score (1-3)', 1.2), ('Rank', 0.8), ('Role', 2.2)]):
    tbl.columns[j].width = Inches(wd)
    tbl.cell(0, j).text = hd
roles = {'H1': 'Initial priority', 'H2': 'Related mechanism', 'H3': 'Downstream outcome'}
for i, h in enumerate(HYP, 1):
    for j, v in enumerate([f'{h} {HYP[h][0]}', f'{base[h]:.2f}', str(rank_base[h]), roles[h]]):
        tbl.cell(i, j).text = v
for r in range(4):
    for j in range(4):
        for p in tbl.cell(r, j).text_frame.paragraphs:
            for run in p.runs:
                run.font.size, run.font.name = Pt(15), 'Calibri'
wtxt = ', '.join(f'{n} {c[2]:.0%}' for n, c in zip(SHORT, CRIT))
text(s, 0.5, 4.3, 7.4, 2.6, [
    f'Weights: {wtxt}. Each criterion scored 1-3 on a written rubric.',
    f'H1 stays first under equal weights, impact-heavy and scope-excluded weightings (lead over H3 narrows to {gap_h3_impact:.1f} when impact is heavily weighted).',
    'H2 and H3 are preserved as research questions: H2 the mechanism, H3 the outcome. Scores are judgements, not data. No feature is preselected.'], size=13, color=MUTED, space=5)
box(s, 8.2, 1.7, 4.7, 5.1)
text(s, 8.35, 1.75, 4.4, 5.0, [('Illustrative base case (annual pickup events)', WARN),
                               f'TAM ~{tam:,.0f}M | SAM ~{sam:,.0f}M | SOM ~{som:,.1f}M',
                               f'~{addr:.2f}M potentially improved events',
                               f'~INR {rev_cr:.2f} crore incremental platform revenue (not profit)',
                               'Assumptions: trip length, eligible categories, rollout reach, problem incidence, effectiveness, trip-retention share, average fare, take rate. Survey and review frequencies are NOT used to estimate incidence.'],
     size=16, space=9)

# ---- Slide 7 (Build-Measure-Learn + metric tree)
n7 = ('The experiment follows build, measure, learn, so we spend little before we learn. Build: a clickable prototype of structured meeting-point guidance against today\'s pin, '
      'not a committed feature. Measure: whether both sides agree on the same accessible spot, time to meet, clarification steps. Phase one is moderated testing with about eight to twelve riders and five to eight drivers; '
      'a field pilot follows only if it looks promising. The metric tree links meeting success to coordination time, calls and walking, and to cancellations, then to retained trips and rider time. '
      'The twenty percent cut in median coordination time is a proposed criterion, not a claim, and I am not claiming statistical power. Safety, accessibility, distraction and privacy are guardrails.')
s = new_slide(7, 'Proposed experiment: Structured Pickup Meeting-Point Guidance (Build-Measure-Learn)',
              'outputs/Uber_FindMyRide_Experiment_Plan.md; outputs/Uber_FindMyRide_Frameworks_Appendix.md. Proposed design; thresholds are proposed decision criteria, not proven improvements', n7)
BML = [('BUILD', 'Minimum prototype, not a feature commitment. A: current pin and guidance. B: pin + labelled entrance/gate, accessible meeting-point description, confirmation of intended spot. Venues: malls, large residential complexes, multi-entrance or restricted-access sites.'),
       ('MEASURE', 'Phase 1, moderated usability: ~8-12 riders, ~5-8 drivers. Same meeting point identified, time to identify, clarification steps, task success, clarity/confidence. Phase 2 field pilot, only if Phase 1 supports it: % eligible pickups completed within a predefined time threshold; also arrival-to-meeting time, calls/messages, extra walking, pickup cancellations.'),
       ('LEARN', 'Proposed criterion: at least 20% lower median coordination time with no loss of task success (not proven; no statistical power claimed). Continue if B wins; iterate if mixed; stop if no gain or a guardrail breach. Guardrails: safety, accessibility, driver distraction, privacy, added complexity.')]
for k, (hd, body) in enumerate(BML):
    y = 1.35 + k * 1.85
    box(s, 0.5, y, 7.3, 1.75)
    text(s, 0.6, y + 0.03, 7.1, 1.7, [(hd, ACC), body], size=13, space=3)
text(s, 8.1, 1.3, 4.9, 0.35, 'Metric tree (hypotheses to test, not established causes)', size=12, bold=True, color=ACC)
box(s, 8.1, 1.7, 4.8, 0.85, PEACH)
text(s, 8.15, 1.72, 4.7, 0.8, [('Potential business outcomes (not measured)', WARN), 'Retained trips, rider time saved, platform revenue'], size=11, space=1)
box(s, 8.1, 3.05, 2.3, 0.85); box(s, 10.6, 3.05, 2.3, 0.85)
text(s, 8.12, 3.07, 2.25, 0.8, [('Fewer pickup cancellations', ACC)], size=12)
text(s, 10.62, 3.07, 2.25, 0.8, [('Shorter coordination time', ACC)], size=12)
line(s, 9.25, 3.05, 9.25, 2.55); line(s, 11.75, 3.05, 11.75, 2.55)
for k, lab in enumerate(['Meeting success (same point agreed)', 'Calls and messages', 'Extra rider walking']):
    x = 8.1 + k * 1.65
    box(s, x, 4.5, 1.5, 1.05)
    text(s, x + 0.02, 4.52, 1.46, 1.0, lab, size=11)
    line(s, x + 0.75, 4.5, 11.75, 3.9)
line(s, 8.85, 4.5, 9.25, 3.9)
text(s, 8.1, 5.65, 4.8, 0.55, 'Primary outcome: share of eligible pickups completed within the predefined threshold.', size=11, color=MUTED)
box(s, 8.1, 6.25, 4.8, 0.6, PEACH)
text(s, 8.15, 6.27, 4.7, 0.55, 'Guardrails: safety, accessibility, driver distraction, privacy, complexity', size=11, color=WARN, bold=True)

# ---- Slide 8 (decision chain)
n8 = ('This is the decision chain. The customer job: meet my driver quickly and with certainty. The friction we observed in both sources. The prioritised hypothesis, H1. '
      'One experiment. And an investment decision. We know confusion, waiting and communication problems appear in both sources. We hypothesise shared meeting-point information '
      'reduces effort. We will test it. Investment follows observed gains in pickup success and coordination time, with no safety or accessibility harm.')
s = new_slide(8, 'Recommendation: a decision chain from customer job to investment decision',
              f'{SURVEY}; {REVIEWS}; outputs/Uber_FindMyRide_Frameworks_Appendix.md', n8)
CHAIN = [('Customer job', 'Meet my driver quickly and with certainty from a busy or complex place'),
         ('Observed friction', f'Survey (n={N}): gate/pin confusion, waiting, calls. Reviews (n={M}): cancellation, waiting, communication'),
         ('Prioritised hypothesis', 'H1 meeting-point ambiguity; H2 is the mechanism, H3 the outcome'),
         ('Validation experiment', 'Structured meeting-point guidance vs current pin (Build-Measure-Learn)'),
         ('Investment decision', 'Invest only if task success and coordination time improve with no safety or accessibility harm')]
for k, (hd, body) in enumerate(CHAIN):
    x = 0.5 + k * 2.5
    pent = box(s, x, 1.5, 2.45, 2.7, ACC if k < 4 else WARN, MSO_SHAPE.PENTAGON)
    pent.adjustments[0] = 0.12
    text(s, x + 0.08, 1.55, 2.15, 2.6, [(hd, WHITE), body], size=14, color=WHITE, space=4)
QUAD = [('What we know', 'Pickup-location confusion, waiting and communication difficulties are reported in the research (small, self-selected samples).'),
        ('What we hypothesize', 'Better shared meeting-point information may reduce coordination effort.'),
        ('What we will test', 'Structured meeting-point guidance versus the existing pickup experience.'),
        ('What determines investment', 'Observed gains in pickup task success and coordination time, without adverse safety or accessibility effects.')]
for k, (hd, body) in enumerate(QUAD):
    x = 0.5 + k * 3.1
    box(s, x, 4.5, 2.95, 2.35)
    text(s, x + 0.08, 4.55, 2.8, 2.25, [(hd, ACC), body], size=14, space=4)

# ---- Slide 9 (references)
n9 = 'These are the supporting research datasets, source records and analysis files. They are available for review.'
s = new_slide(9, 'References and evidence trail', 'All paths relative to the project root (TMS/). Verification status shown per source', n9)
refs = [('Independently verified (files and live fetch)', ACC),
        'Primary: survey export (data/raw, git-ignored); data/clean/Cleaned_Primary_Research.csv, Cleaning_Log.csv; notebooks/Uber_Primary_EDA.ipynb',
        f'Secondary: data/clean/Secondary_Reviews_Verified.csv (n={M}; review IDs, dates {DATES}; Apple India customer-reviews RSS feed itunes.apple.com/in/rss/customerreviews/id=368677368; listing apps.apple.com/in/app/uber-rides-eats-and-more/id368677368). No per-review URL exists. 24 screened IDs unmatched and unused',
        'Analysis: notebooks/Uber_Secondary_Reviews.ipynb; outputs/Triangulation_Matrix.csv; outputs/Uber_FindMyRide_Problem_Prioritization.csv (scores = analytical judgements); outputs/Uber_FindMyRide_Frameworks_Appendix.md; Experiment_Plan.md',
        ('Not independently verified (web-search summaries; originals not opened)', WARN),
        'Market model: outputs/Uber_TAM_SAM_SOM.xlsx. Uber India newsroom 11.6 bn km in 2025 (S1); Entrackr Rapido 207M rides Q2 FY25, company claim (S3); Outlook Business market shares, undated (S4). Registry also lists older, un-used context (CCPA 2022, LocalCircles 2018)',
        ('Frameworks (published works; definitions in the appendix)', ACC),
        'Christensen, Hall, Dillon & Duncan, Competing Against Luck (2016); Ulwick, Jobs to Be Done: Theory to Practice (2016); Ries, The Lean Startup (2011); Gibbons, Journey Mapping 101, Nielsen Norman Group (2018)']
text(s, 0.5, 1.3, 12.3, 5.6, [r if isinstance(r, tuple) else '•  ' + r for r in refs], size=13, space=5)

path = OUT / 'Uber_FindMyRide_Final_Presentation.pptx'
prs.save(path)

# ---------- speaker notes file + timing ----------
ALLOC = {1: 20, 2: 35, 3: 40, 4: 40, 5: 50, 6: 45, 7: 45, 8: 25}
WPS = 2.5
lines = ['# Uber Find My Ride: Final Speaker Notes', '',
         f'Target: about 5 minutes across slides 1-8 (~150 words/min). Secondary evidence window: {DATES}.', '']
FWNOTE = ['', '## Why each framework was chosen (for Q&A)', '',
          '- **Jobs to Be Done** defines the need independent of any feature, so the problem is not framed as "a better pin".',
          '- **Customer journey map** shows where in the pickup the breakdown starts (stage 2 in the survey; late stages in reviews), which tells us where to intervene.',
          '- **Weighted matrix** makes the prioritisation auditable: criteria, weights and scores are visible and can be challenged. Scores are judgements, not data.',
          '- **Build-Measure-Learn** keeps the next step small and decision-oriented: learn before committing to build.',
          '- **Metric tree** connects pickup metrics (meeting success, coordination time, calls, walking, cancellations) to potential business outcomes without claiming they are measured.']
tot_w = tot_t = 0
for n in range(1, 10):
    w = len(NOTES[n].split()); t = w / WPS
    if n <= 8:
        tot_w += w; tot_t += t
    lines += [f'## Slide {n}' + (f' (budget {ALLOC[n]}s, notes ~{t:.0f}s, {w} words)' if n <= 8 else ' (references, not timed)'), '', NOTES[n], '']
lines += [f'**Total slides 1-8: {tot_w} words, about {tot_t:.0f} seconds ({tot_t / 60:.1f} minutes) at 150 words/min.**'] + FWNOTE
(OUT / 'Uber_FindMyRide_Final_Speaker_Notes.md').write_text('\n'.join(lines), encoding='utf-8')

# ---------- frameworks appendix ----------
A = ['# Uber Find My Ride: Frameworks Appendix', '',
     f'Supports the final presentation. Primary survey (n={N}, convenience sample) and secondary app-store reviews (n={M}, {DATES}, purposive, not representative) are kept separate throughout. '
     '**All framework scores are analytical judgements, not measured data.**', '',
     '## 1. Jobs to Be Done (JTBD)', '',
     '**Definition.** JTBD frames demand as the progress a person is trying to make in a circumstance, independent of any product feature (Christensen et al., 2016; Ulwick, 2016).', '',
     f'**Core rider job.** {JOB}', '',
     '**Core driver job (hypothesis, not evidenced by the data).** When I arrive near a pickup, I want to know exactly where to stop and whom to meet, so I can complete the pickup quickly and move to the next trip.', '',
     f'**Evidence for the rider job (primary only).** {prim_late} of {N} worried about being late; {prim["wait"]} reported long waiting; {met_delay} met the driver only after a delay. '
     f'The driver job rests on {drivers} driver review in the secondary sample and no driver survey data, so it is a hypothesis to test.', '',
     '## 2. Customer journey mapping', '',
     '**Definition.** A journey map lays out the stages a customer passes through and the friction at each (Gibbons, 2018). The six stages come from the project brief (`PROMPT.md`): 1 Driver assigned, 2 Pickup interpretation, 3 Driver approaches, 4 Coordination, 5 Meeting, 6 Outcome.', '',
     "**Assumption.** Mapping survey options and review codes to stages is the analyst's judgement. Counts are respondents or reviews that mention an item, not rates; items overlap and must not be summed.", '',
     f'### Primary survey (n={N})', '', '| Stage | Items mapped and respondent counts |', '|---|---|']
A += [f'| {a} | {b} |' for a, b in PS]
A += ['', f'### Secondary reviews (n={M}; reviews touching each stage)', '', '| Stage | Reviews |', '|---|---|']
A += [f'| {st} | {int(sec_stage[st])} |' for st in STAGES]
A += ['', '**Reading.** In the survey, friction is reported at stage 2 (interpreting the pickup point). In reviews it clusters at stages 3, 4 and 6 (approach, coordination, outcome). The two lenses answer different questions (see the triangulation matrix), so this is a difference in emphasis, not a contradiction.', '',
      '## 3. Weighted problem-prioritisation matrix', '',
      '**Method.** Multi-criteria weighted scoring: each hypothesis is scored 1-3 on six criteria; the weighted score is the sum of weight x score (range 1-3). Weights express how much each criterion should count for a discovery decision. **Scores and weights are judgements, not measurements.**', '',
      '### Rubric and base-case weights', '', '| Criterion | Weight | Scoring guide |', '|---|---|---|']
A += [f'| {c[1]} | {c[2]:.0%} | {c[3]} |' for c in CRIT]
A += ['', '### Scores and rationale', '', '| Hypothesis | ' + ' | '.join(SHORT) + ' | Weighted score | Rank |', '|---|' + '---|' * (len(CRIT) + 2)]
for h, (name, defn, sc, why) in HYP.items():
    A.append(f'| {h} {name} | ' + ' | '.join(map(str, sc)) + f' | {base[h]:.2f} | {rank_base[h]} |')
A += ['']
for h, (name, defn, sc, why) in HYP.items():
    A += [f'**{h} {name}.** {defn}', ''] + [f'- {w}' for w in why] + ['']
A += ['### Sensitivity (does the ranking depend on the weights?)', '', '| Weighting | Weights (evidence / impact / frequency / scope / intervention / confidence) | H1 | H2 | H3 | Order |', '|---|---|---|---|---|---|']
for k, w in WEIGHTS.items():
    A.append(f'| {k} | ' + ' / '.join(f'{x:.0%}' for x in w) + f' | {RESULT[k]["H1"]:.2f} | {RESULT[k]["H2"]:.2f} | {RESULT[k]["H3"]:.2f} | ' + ' > '.join(RANK[k]) + ' |')
A += ['', f'**Conclusion.** H1 ranks first under all four weightings, so the recommendation to prioritise H1 is supported by the scoring as specified. The margin over H3 is smaller when impact is weighted heavily ({gap_h3_impact:.1f}) or scope is excluded, and the scores themselves are judgements, so the recommendation is a discovery priority, not a proof.', '',
      '**Why not H2 or H3 first.** H2 (coordination friction) is likely a mechanism downstream of H1: calls, waiting and walking are how ambiguity gets resolved, and have other causes too, so it is measured within the experiment rather than treated as the root problem. '
      f'H3 (cancellation) is the most cited review theme ({secn["canc"]}/{M}) and costly, but the link to coordination is not shown ({canc_gatepin} of {secn["canc"]} cancellation reviews carry a gate or pin code; {canc_fare} carry a fare code) and many causes sit outside meeting-point information. It is kept as an outcome metric and a research question needing causal validation.', '',
      '**Limits.** The scope criterion favours H1 and H2 by construction; the "scope excluded" run checks this. Scores rely on small, self-selected samples.', '',
      '## 4. Lean Startup: Build-Measure-Learn', '',
      '**Definition.** Build a minimum test, measure against a pre-stated criterion, learn and decide whether to persevere, iterate or stop (Ries, 2011).', '',
      '| Step | This project |', '|---|---|',
      '| Build | Minimum prototype of structured meeting-point guidance (condition B) versus the current pin and guidance (condition A). Not a feature commitment |',
      '| Measure | Phase 1: same meeting point identified, time to identify, clarification steps, task success, clarity and confidence. Phase 2 (only if Phase 1 supports): % eligible pickups completed within a predefined time threshold; secondary: arrival-to-meeting time, calls/messages, extra walking, pickup cancellations |',
      '| Learn | Proposed criterion of at least 20% lower median coordination time with no loss of task success (a proposed decision criterion, not proven). Continue / iterate / stop rules in `Uber_FindMyRide_Experiment_Plan.md`. No statistical power is claimed |', '',
      '## 5. Metric tree', '',
      '**Definition.** A metric tree decomposes an outcome into the metrics that drive it, so product measures can be linked to business results. Links here are hypotheses to test, not established causes.', '',
      '```', 'Potential business outcomes (not measured): retained trips, rider time saved, platform revenue',
      '|-- Fewer pickup-related cancellations  <-- (hypothesis) meeting success',
      '`-- Shorter coordination time           <-- meeting success, fewer calls/messages, less extra walking', '```', '',
      '**Guardrail metrics:** rider and driver safety, accessibility, driver distraction, privacy, added pickup complexity. The TAM/SAM/SOM model (illustrative, unvalidated assumptions, not a forecast) is not used to set any of these metrics.', '',
      '## 6. Assumptions', '',
      '- Framework scores, weights and stage mapping are analyst judgements.',
      '- Primary and secondary counts have different denominators and are never combined.',
      f'- Secondary reviews: Apple App Store India only, {M} reviews, {DATES} (about five weeks of the requested six months); {drivers} driver review; no per-review URL.',
      '- Driver job and driver-side metrics are hypotheses; the data contain almost no driver evidence.',
      '- No feature is preselected; "structured meeting-point guidance" is a test condition.', '',
      '## 7. References', '',
      '- Christensen, C. M., Hall, T., Dillon, K., & Duncan, D. S. (2016). *Competing Against Luck*. Harper Business.',
      '- Ulwick, A. W. (2016). *Jobs to Be Done: Theory to Practice*. Idea Bite Press.',
      '- Ries, E. (2011). *The Lean Startup*. Crown Business.',
      '- Gibbons, S. (2018). Journey Mapping 101. Nielsen Norman Group (nngroup.com).',
      '- Weighted scoring and metric trees are standard product-management practices; no specific source is cited for them.',
      '- AGMP course materials were not supplied to this analysis, so no course page citations are included. Add them from the course documents if required.', '']
(OUT / 'Uber_FindMyRide_Frameworks_Appendix.md').write_text('\n'.join(A), encoding='utf-8')
print('saved', path, '| slides', len(prs.slides), '| words', tot_w, '| ~sec', round(tot_t))
print({n: (len(NOTES[n].split()), round(len(NOTES[n].split()) / WPS), ALLOC.get(n)) for n in range(1, 9)})
print({k: [f'{h}:{v:.2f}' for h, v in r.items()] for k, r in RESULT.items()})
