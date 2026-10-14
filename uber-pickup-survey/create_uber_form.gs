/**
 * Uber Ride & Pickup Experience Survey — Google Form + Sheet builder.
 *
 * 1. script.google.com → New project → paste this file → Save.
 * 2. Select createUberPickupSurvey → Run → authorise.
 * 3. View → Logs (or Execution log) shows the edit link, respondent link and Sheet link.
 */
var RESPONSES_TAB = 'Form Responses 1';

function createUberPickupSurvey() {
  var form = FormApp.create('Uber Ride & Pickup Experience Survey');
  form.setDescription(
    "We are conducting independent customer research to understand people's experiences with Uber, especially when " +
    'booking rides from crowded places such as shopping malls, office complexes, airports, railway stations, and busy streets.\n\n' +
    'We would like to understand what works well, what difficulties you have faced, and what improvements could make ride ' +
    'pickups easier and more reliable.\n\n' +
    'This is independent research and is not affiliated with Uber.\n\n' +
    '• Participation is completely voluntary.\n' +
    '• You may respond anonymously.\n' +
    '• Your name, phone number, and email address are not required.\n' +
    '• Please do not include personally identifying information in written answers.\n' +
    '• Responses will be used for independent product research and reported in anonymized or aggregated form.\n' +
    '• Estimated completion time: 4–5 minutes.\n\n' +
    'By submitting, you are happy for your answers to be used for this research. Thank you for sharing your experience! 🙏');

  // Anonymity & privacy settings
  form.setCollectEmail(false);
  form.setLimitOneResponsePerUser(false); // true would force Google sign-in
  try { form.setRequireLogin(false); } catch (e) { /* only exists on Workspace accounts */ }
  form.setAllowResponseEdits(false);
  form.setPublishingSummary(false);
  form.setShowLinkToRespondAgain(false);
  form.setProgressBar(true);
  form.setAcceptingResponses(true);
  form.setConfirmationMessage('Thank you! Your response has been recorded.');

  function mc(title, choices, required) {
    return form.addMultipleChoiceItem().setTitle(title).setChoiceValues(choices).setRequired(required);
  }
  function cb(title, choices, required, other) {
    var item = form.addCheckboxItem().setTitle(title).setChoiceValues(choices).setRequired(required);
    if (other) item.showOtherOption(true);
    return item;
  }
  function note(title, help) {
    var item = form.addParagraphTextItem().setTitle(title).setRequired(false);
    if (help) item.setHelpText(help);
    return item;
  }

  // ---------- Page 1: Q1 ----------
  var q1 = form.addMultipleChoiceItem().setTitle('Q1. Have you used Uber for booking a ride?').setRequired(true);

  // ---------- Page 2: Uber users (Q2–Q15) ----------
  var pUber = form.addPageBreakItem().setTitle('Your Uber experience')
    .setHelpText('If a question does not match your experience, choose "Not applicable" or "No difficulties". Written answers are optional.');

  form.addScaleItem().setTitle('Q2. How would you rate your overall experience with Uber?')
    .setBounds(1, 5).setLabels('Very poor', 'Excellent').setRequired(true);
  note('Q2a. What is the main reason for your rating?', 'Please share any positive or negative experience.');

  mc('Q3. Have you booked an Uber from a crowded or complex location?',
    ['Yes, several times', 'Yes, once or twice', 'No', 'Cannot remember'], true);

  cb('Q4. Where have you experienced difficulty finding or meeting your Uber driver?',
    ['Shopping mall', 'Office complex / IT park', 'Airport', 'Railway station / Bus stand', 'Crowded market',
      'Busy street / Main road', 'Event venue', 'Residential complex', 'I have not experienced such difficulty'], true, true);
  form.addTextItem().setTitle('Q4a. If you remember, mention the location type or entrance where the difficulty occurred.')
    .setHelpText('Please do not share an exact address.').setRequired(false);

  mc("Q5. How helpful is Uber's app in showing your pickup location and helping you find the driver?",
    ['Very helpful and accurate', 'Mostly helpful', 'Sometimes confusing or inaccurate', 'Often confusing or inaccurate',
      'I have not used these features / Not sure'], true);
  note('Q5a. What worked well, or what information was missing or confusing?');

  cb('Q6. What difficulties have you experienced when meeting your driver in crowded places?',
    ['Driver could not find my exact location', 'Pickup pin showed an incorrect or inconvenient location',
      'Confusion about which entrance or gate to use', 'Driver could not access the pickup point',
      'Driver asked me to walk to another location', 'Repeated phone calls or messages', 'Long waiting time',
      "Difficulty identifying the driver's vehicle", 'No difficulties'], true, true);
  note('Q6a. Please describe what happened during your most memorable difficult pickup.');

  cb('Q7. How did the driver coordinate with you when finding your location was difficult?',
    ['Called and politely asked for directions', 'Sent messages through the app', 'Helped identify a suitable meeting point',
      'Asked me to move to another location', 'Appeared confused about the location', 'Did not communicate clearly',
      'Cancelled the booking', 'Not applicable'], true, true);
  note('Q7a. What did the driver say or do that helped or made the situation more difficult?');

  mc("Q8. How would you describe the driver's behavior during a difficult pickup?",
    ['Very polite and helpful', 'Cooperative and patient', 'Neutral', 'Frustrated or impatient', 'Rude or unhelpful',
      'Behavior varied across rides', 'Not applicable'], true);
  note('Q8a. If you experienced frustration or particularly good service, what happened?');

  cb('Q9. How did you feel when you had difficulty finding your driver?',
    ['Frustrated', 'Anxious or stressed', 'Unsafe or uncomfortable', 'Worried about being late', 'Confused',
      'Calm because the driver helped', 'No significant inconvenience', 'Not applicable'], true, true);
  note('Q9a. What was the biggest impact on you?');

  mc('Q10. What was the outcome of your difficult pickup experience?',
    ['Successfully met the driver without much delay', 'Successfully met the driver after a delay', 'I cancelled the booking',
      'Driver cancelled the booking', 'Booking ended for another reason', 'Not applicable'], true);
  note('Q10a. If the ride was cancelled or delayed, what was the main reason?');

  mc('Q11. Has an Uber driver ever requested extra money beyond the fare shown in the app?',
    ['Yes', 'No', 'Cannot remember', 'Prefer not to answer'], true);
  note('Q11a. If yes, what reason did the driver give?',
    'Was this related to pickup location, traffic, waiting, or another issue?');

  note('Q12. What has been your most positive experience with Uber?',
    'Please describe anything you appreciate, such as helpful drivers, accurate pickup locations, quick coordination, safety, convenience, or reliable service.');
  note('Q13. What improvements would you suggest to make Uber pickups easier, especially in crowded places?',
    'Please share your suggestions in your own words.');

  mc('Q14. Is there another ride-booking app you prefer over Uber?',
    ['Rapido', 'Ola', 'Namma Yatri', 'Other', 'I prefer Uber', 'No particular preference'], true);
  note('Q14a. Why do you prefer that app?',
    'Does your preference relate to price, driver availability, pickup coordination, cancellations, driver behavior, or another reason?');
  note('Q15. Would you like to provide any additional feedback about Uber?',
    'Please share any other positive or negative experience that you feel is important.');

  // ---------- Page 2 (alternative): never used Uber ----------
  var pNever = form.addPageBreakItem().setTitle('Your ride-booking preference')
    .setGoToPage(FormApp.PageNavigationType.SUBMIT); // Uber users submit after Q15, never reach this page
  mc('Q14 (non-Uber users). Which ride-booking app do you prefer?',
    ['Rapido', 'Ola', 'Namma Yatri', 'Other', 'No particular preference', 'I do not use ride-booking apps'], true);
  note('Q14a (non-Uber users). Why do you prefer that app?',
    'Does your preference relate to price, driver availability, pickup coordination, cancellations, driver behavior, or another reason?');

  q1.setChoices([
    q1.createChoice('Yes, frequently', pUber),
    q1.createChoice('Yes, occasionally', pUber),
    q1.createChoice('Yes, but not in the last 3 months', pUber),
    q1.createChoice('No, I have never used Uber', pNever)
  ]);

  // ---------- Linked Google Sheet + summary ----------
  var ss = SpreadsheetApp.create('Uber Ride & Pickup Experience Survey (Responses)');
  form.setDestination(FormApp.DestinationType.SPREADSHEET, ss.getId());
  SpreadsheetApp.flush();
  ss = SpreadsheetApp.openById(ss.getId());
  ss.getSheets().forEach(function (s) { if (s.getFormUrl()) s.setName(RESPONSES_TAB); });
  var blank = ss.getSheetByName('Sheet1');
  buildSummary_(ss, form);
  if (blank) ss.deleteSheet(blank);

  Logger.log('Edit link:       ' + form.getEditUrl());
  Logger.log('Respondent link: ' + form.getPublishedUrl());
  Logger.log('Short link:      ' + form.shortenFormUrl(form.getPublishedUrl()));
  Logger.log('Responses Sheet: ' + ss.getUrl());
}

/** Summary tab: live counts per answer option, grouped by analysis theme. No data is pre-filled. */
function buildSummary_(ss, form) {
  var themes = [
    ['Overall Uber satisfaction', ['Q1.', 'Q2.']],
    ['Pickup problems by location type', ['Q3.', 'Q4.']],
    ['Perceived pickup-location accuracy', ['Q5.', 'Q6.']],
    ['Driver coordination & communication', ['Q7.']],
    ['Driver behavior & customer emotions', ['Q8.', 'Q9.']],
    ['Delays & cancellations', ['Q10.']],
    ['Requests for additional money', ['Q11.']],
    ['Competitor preference', ['Q14.', 'Q14 (non-Uber users).']]
  ];
  var openText = [
    ['Positive experiences', 'Q12'], ['Improvement suggestions', 'Q13'], ['Reasons for rating', 'Q2a'],
    ['Difficult-pickup stories', 'Q6a, Q7a, Q8a, Q9a, Q10a'], ['Extra-money reasons', 'Q11a'],
    ['Competitor-preference reasons', 'Q14a'], ['Additional feedback', 'Q15']
  ];

  var items = {};
  form.getItems().forEach(function (it) { items[it.getTitle().split(' ')[0] + (it.getTitle().indexOf('(non-Uber') > -1 ? ' (non-Uber users).' : '')] = it; });

  var sh = ss.insertSheet('Summary');
  var R = "'" + RESPONSES_TAB + "'!";
  var rows = [['Theme / Question', 'Answer option', 'Count', '% of answers to this question']];
  var styles = [];

  themes.forEach(function (t) {
    rows.push([t[0], '', '', '']); styles.push(rows.length);
    t[1].forEach(function (key) {
      var it = items[key];
      if (!it) return;
      var title = it.getTitle(), type = it.getType(), opts = [], multi = false;
      if (type === FormApp.ItemType.MULTIPLE_CHOICE) {
        opts = it.asMultipleChoiceItem().getChoices().map(function (c) { return c.getValue(); });
      } else if (type === FormApp.ItemType.CHECKBOX) {
        opts = it.asCheckboxItem().getChoices().map(function (c) { return c.getValue(); }); multi = true;
      } else if (type === FormApp.ItemType.SCALE) {
        opts = ['1', '2', '3', '4', '5'];
      }
      var col = 'INDEX(' + R + 'A:BZ,0,MATCH("' + title.replace(/"/g, '""') + '",' + R + '$1:$1,0))';
      var answered = '(COUNTA(' + col + ')-1)';
      opts.forEach(function (o, i) {
        var crit = multi ? '"*' + o.replace(/"/g, '""') + '*"' : (type === FormApp.ItemType.SCALE ? o : '"' + o.replace(/"/g, '""') + '"');
        rows.push([i === 0 ? title : '', o,
          '=IFERROR(COUNTIF(' + col + ',' + crit + '),0)',
          '=IFERROR(C' + (rows.length + 1) + '/' + answered + ',0)']);
      });
      if (type === FormApp.ItemType.SCALE) rows.push(['', 'Average rating', '=IFERROR(AVERAGE(' + col + '),"—")', '']);
      if (multi) rows.push(['', 'Other (written in)', '', 'See ' + RESPONSES_TAB]);
    });
  });

  rows.push(['', '', '', '']);
  rows.push(['Open-text themes (read & tag in the responses tab)', 'Questions', '', '']); styles.push(rows.length);
  openText.forEach(function (o) { rows.push([o[0], o[1], '', '']); });
  rows.push(['Total responses', '', '=MAX(0,COUNTA(' + R + 'A:A)-1)', '']); styles.push(rows.length);

  sh.getRange(1, 1, rows.length, 4).setValues(rows);
  sh.getRange('D:D').setNumberFormat('0%');
  sh.getRange(1, 1, 1, 4).setFontWeight('bold').setBackground('#000000').setFontColor('#ffffff');
  styles.forEach(function (r) { sh.getRange(r, 1, 1, 4).setFontWeight('bold').setBackground('#eeeeee'); });
  sh.setColumnWidth(1, 380); sh.setColumnWidth(2, 340); sh.setColumnWidths(3, 2, 110);
  sh.getRange('A:B').setWrap(true);
  sh.setFrozenRows(1);
  ss.setActiveSheet(sh);
}
