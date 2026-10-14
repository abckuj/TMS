/**
 * Ride Pickup Experience Study — Google Form builder.
 *
 * Usage: script.google.com → New project → paste this file → Run createRidePickupForm()
 * → authorise. The form's edit and live URLs are printed in the execution log.
 */
function createRidePickupForm() {
  var form = FormApp.create('Ride Pickup Experience Study')
    .setDescription(
      'This is an independent product research study on how riders experience pickups on ride-hailing ' +
      'apps (Uber, Ola and Rapido). The study is not affiliated with, sponsored by, or conducted on behalf ' +
      'of any ride-hailing company.\n\n' +
      'It takes about 8–10 minutes. There are no right or wrong answers — please describe your actual experience.')
    .setProgressBar(true)
    .setCollectEmail(false)
    .setAllowResponseEdits(false)
    .setConfirmationMessage('Thank you for your time. Your responses will help identify how ride pickups can be made easier for riders.');

  var SUBMIT = FormApp.PageNavigationType.SUBMIT;
  var SCALE5 = ['Very poor', 'Poor', 'Average', 'Good', 'Excellent'];

  // ---------- Page 0: Consent ----------
  form.addSectionHeaderItem().setTitle('Participant information & consent').setHelpText(
    '• Participation is voluntary; you may stop at any time.\n' +
    '• No personally identifying information is required. Contact details are requested only if you opt in to a follow-up conversation.\n' +
    '• Responses are analysed in aggregate and anonymised before any findings are shared.\n' +
    '• Data is used only for this research and is not sold or shared with ride-hailing companies.\n' +
    '• You must be 18 years or older to take part.\n' +
    '• You may request deletion of your response by contacting the researcher via the follow-up details provided.');
  var consent = form.addMultipleChoiceItem()
    .setTitle('Have you read the information above, and do you agree to take part?').setRequired(true);

  // ---------- Page 1: Eligibility ----------
  var pEligibility = form.addPageBreakItem().setTitle('Eligibility');
  var age = form.addMultipleChoiceItem().setTitle('What is your age group?').setRequired(true);
  var recentUse = form.addMultipleChoiceItem()
    .setTitle('Have you booked a ride on Uber, Ola or Rapido in the last 3 months?').setRequired(true);

  // ---------- Page 2: Usage profile ----------
  var pProfile = form.addPageBreakItem().setTitle('About your ride usage');
  form.addTextItem().setTitle('Which city do you take rides in most often?').setRequired(true);
  form.addMultipleChoiceItem().setTitle('How often do you book rides?').setRequired(true)
    .setChoiceValues(['Daily', '3–5 times a week', '1–2 times a week', '2–3 times a month', 'Once a month or less']);
  form.addCheckboxItem().setTitle('What do you usually book rides for? (Select all that apply)').setRequired(true)
    .setChoiceValues(['Commute to work / college', 'Airport / railway / bus station', 'Social outings', 'Errands / shopping',
      'Medical visits', 'Late-night travel'])
    .showOtherOption(true);
  form.addCheckboxItem().setTitle('Which ride types do you use? (Select all that apply)').setRequired(true)
    .setChoiceValues(['Bike taxi', 'Auto-rickshaw', 'Cab — economy', 'Cab — premium / sedan / SUV', 'Shared / pool']);
  form.addCheckboxItem().setTitle('Which apps have you used in the last 3 months? (Select all that apply)').setRequired(true)
    .setChoiceValues(['Uber', 'Ola', 'Rapido']).showOtherOption(true);
  var primary = form.addMultipleChoiceItem()
    .setTitle('Which app do you use most often?').setRequired(true);

  // ---------- Pages 3–5: Platform-specific ----------
  function platformSection(name) {
    var pb = form.addPageBreakItem().setTitle('Your experience with ' + name);
    form.addCheckboxItem().setTitle('Why do you use ' + name + ' most often? (Select up to 3)').setRequired(true)
      .setChoiceValues(['Lower fares', 'Shorter wait / faster driver assignment', 'More accurate pickup location',
        'Fewer cancellations', 'Better driver behaviour', 'Vehicle type availability', 'Safety features',
        'Offers / discounts / subscriptions', 'Habit / familiarity'])
      .showOtherOption(true)
      .setValidation(FormApp.createCheckboxValidation().requireSelectAtMost(3).build());
    form.addScaleItem().setTitle('How easy is it to meet your driver at the pickup point on ' + name + '?')
      .setBounds(1, 5).setLabels('Very difficult', 'Very easy').setRequired(true);
    form.addParagraphTextItem().setTitle('Is there anything about pickups on ' + name + ' that consistently frustrates you? (Optional)');
    return pb;
  }
  var pUber = platformSection('Uber');
  var pOla = platformSection('Ola');
  var pRapido = platformSection('Rapido');

  // ---------- Page 6: Pickup experience (all) ----------
  var pPickup = form.addPageBreakItem().setTitle('Setting and reaching the pickup point');
  form.addMultipleChoiceItem().setTitle('How do you usually set your pickup location?').setRequired(true)
    .setChoiceValues(['Use my current GPS location as-is', 'Adjust the map pin manually', 'Search for an address or landmark',
      'Choose a suggested pickup point from the app', 'Use a saved place (home, work, etc.)']);
  form.addMultipleChoiceItem().setTitle('How often does the driver arrive at the exact pickup point you set?').setRequired(true)
    .setChoiceValues(['Always', 'Most of the time', 'About half the time', 'Rarely', 'Never']);
  form.addMultipleChoiceItem().setTitle('How often do you need to call or message the driver before pickup?').setRequired(true)
    .setChoiceValues(['Every ride', 'Most rides', 'Some rides', 'Rarely', 'Never']);
  var pickupIssue = form.addMultipleChoiceItem()
    .setTitle('In the last 3 months, have you had difficulty meeting your driver at the pickup point?').setRequired(true);

  // ---------- Page 7: Pickup issue deep-dive ----------
  var pIssue = form.addPageBreakItem().setTitle('Pickup difficulties')
    .setHelpText('Please think about the most recent time this happened.');
  form.addCheckboxItem().setTitle('Which difficulties have you experienced? (Select all that apply)').setRequired(true)
    .setChoiceValues(['GPS / map pin showed the wrong location', 'Driver went to a different spot or entrance',
      'Driver could not find me in a crowded area', 'Driver asked me to walk to them',
      'Pickup point was unsafe or not allowed for stopping', 'Driver could not enter the area (gated society, campus, mall, airport)',
      'Vehicle details (number plate, model) were hard to match', 'Language or communication difficulty with driver',
      'Driver did not answer calls or messages', 'Driver asked for destination or payment mode before arriving'])
    .showOtherOption(true);
  form.addMultipleChoiceItem().setTitle('Where were you being picked up?').setRequired(true)
    .setChoiceValues(['Residential society / apartment complex', 'Office / tech park', 'Airport', 'Railway / metro / bus station',
      'Mall / market', 'Hospital', 'Main road / street', 'Narrow lane / unmarked area'])
    .showOtherOption(true);
  form.addMultipleChoiceItem().setTitle('Which app was this on?').setRequired(true)
    .setChoiceValues(['Uber', 'Ola', 'Rapido']).showOtherOption(true);
  form.addCheckboxItem().setTitle('How did you and the driver coordinate? (Select all that apply)').setRequired(true)
    .setChoiceValues(['In-app call', 'Direct phone call', 'In-app chat', 'WhatsApp / SMS', 'Shared live location',
      'Tracked the driver on the map', 'No coordination happened']);
  form.addMultipleChoiceItem().setTitle('Roughly how much extra time did the pickup take?').setRequired(true)
    .setChoiceValues(['Under 2 minutes', '2–5 minutes', '5–10 minutes', '10–15 minutes', 'More than 15 minutes']);
  form.addMultipleChoiceItem().setTitle('How did it end?').setRequired(true)
    .setChoiceValues(['We met and the ride went ahead', 'I cancelled', 'The driver cancelled', 'Booked a different ride / app',
      'Took other transport']);
  form.addScaleItem().setTitle('How frustrating was this experience?')
    .setBounds(1, 5).setLabels('Not at all', 'Extremely').setRequired(true);
  form.addParagraphTextItem().setTitle('Briefly describe what happened, step by step.');

  // ---------- Page 8: Waiting & cancellations ----------
  var pWait = form.addPageBreakItem().setTitle('Waiting times and cancellations');
  form.addMultipleChoiceItem().setTitle('How accurate is the driver arrival time (ETA) shown in the app?').setRequired(true)
    .setChoiceValues(['Very accurate', 'Mostly accurate', 'Often underestimated', 'Often overestimated', 'Unpredictable']);
  form.addMultipleChoiceItem().setTitle('On a typical ride, how long do you wait beyond the ETA shown?').setRequired(true)
    .setChoiceValues(['No extra wait', 'Under 2 minutes', '2–5 minutes', '5–10 minutes', 'More than 10 minutes']);
  form.addMultipleChoiceItem().setTitle('What is the longest you are willing to wait after booking before you cancel?').setRequired(true)
    .setChoiceValues(['Under 3 minutes', '3–5 minutes', '5–10 minutes', '10–15 minutes', 'More than 15 minutes']);
  var cancelled = form.addMultipleChoiceItem()
    .setTitle('In the last 3 months, has a booked ride been cancelled (by you or the driver) before pickup?').setRequired(true);

  // ---------- Page 9: Cancellation details ----------
  var pCancel = form.addPageBreakItem().setTitle('Cancellations');
  form.addMultipleChoiceItem().setTitle('Who usually cancels?').setRequired(true)
    .setChoiceValues(['Mostly the driver', 'Mostly me', 'About equal']);
  form.addCheckboxItem().setTitle('What were the reasons? (Select all that apply)').setRequired(true)
    .setChoiceValues(['Driver was not moving / too far away', 'Driver asked me to cancel', 'Driver refused destination or payment mode',
      'Could not find each other at pickup', 'Wait was too long', 'Found a cheaper or faster option', 'Fare changed after booking',
      'My plans changed'])
    .showOtherOption(true);
  form.addMultipleChoiceItem().setTitle('Have you been charged a cancellation fee you felt was unfair?').setRequired(true)
    .setChoiceValues(['Yes, more than once', 'Yes, once', 'No', 'Not sure']);
  form.addMultipleChoiceItem().setTitle('After a cancellation, what do you usually do?').setRequired(true)
    .setChoiceValues(['Rebook on the same app', 'Switch to another app', 'Take other transport', 'Drop the trip']);

  // ---------- Page 10: Platform comparison ----------
  var pCompare = form.addPageBreakItem().setTitle('Comparing apps');
  form.addGridItem().setTitle('In your experience, which app performs best on each of these?')
    .setRows(['Pickup location accuracy', 'Driver arrives on time', 'Ease of contacting the driver', 'Fewest cancellations',
      'Fair cancellation policy', 'Clear vehicle / driver details', 'Feeling safe while waiting'])
    .setColumns(['Uber', 'Ola', 'Rapido', 'No difference', 'Not sure']);
  form.addScaleItem().setTitle('How likely are you to recommend your most-used app to a friend, based on pickup experience?')
    .setBounds(0, 10).setLabels('Not at all likely', 'Extremely likely').setRequired(true);
  form.addCheckboxItem().setTitle('Which of these would most improve your pickup experience? (Select up to 3)').setRequired(true)
    .setChoiceValues(['Exact entrance / gate-level pickup points', 'Photo or landmark-based pickup instructions',
      'Live location sharing between rider and driver', 'Auto-translated chat with driver', 'More reliable ETA',
      'Penalties for drivers who ask riders to cancel', 'Wait-time compensation', 'Clearer vehicle identification (e.g. colour flash)'])
    .showOtherOption(true)
    .setValidation(FormApp.createCheckboxValidation().requireSelectAtMost(3).build());
  form.addParagraphTextItem().setTitle('If you could change one thing about ride pickups, what would it be?');
  var followUp = form.addMultipleChoiceItem()
    .setTitle('Would you be open to a 20-minute follow-up conversation about your experience?').setRequired(true);

  // ---------- Page 11: Contact (opt-in) ----------
  var pContact = form.addPageBreakItem().setTitle('Follow-up contact (optional)')
    .setHelpText('Used only to schedule the conversation and deleted when the study ends.');
  form.addTextItem().setTitle('First name');
  form.addTextItem().setTitle('Email or phone number').setRequired(true);
  form.addMultipleChoiceItem().setTitle('Preferred format').setChoiceValues(['Phone call', 'Video call', 'Chat / text']);

  // ---------- Branching ----------
  consent.setChoices([consent.createChoice('Yes, I agree', pEligibility), consent.createChoice('No, I do not agree', SUBMIT)]);
  age.setChoices([age.createChoice('Under 18', SUBMIT), age.createChoice('18–24', FormApp.PageNavigationType.CONTINUE),
    age.createChoice('25–34', FormApp.PageNavigationType.CONTINUE), age.createChoice('35–44', FormApp.PageNavigationType.CONTINUE),
    age.createChoice('45–54', FormApp.PageNavigationType.CONTINUE), age.createChoice('55+', FormApp.PageNavigationType.CONTINUE)]);
  recentUse.setChoices([recentUse.createChoice('Yes', pProfile), recentUse.createChoice('No', SUBMIT)]);
  primary.setChoices([primary.createChoice('Uber', pUber), primary.createChoice('Ola', pOla),
    primary.createChoice('Rapido', pRapido), primary.createChoice('I use them about equally', pPickup)]);
  pOla.setGoToPage(pPickup);     // end of Uber section → pickup experience
  pRapido.setGoToPage(pPickup);  // end of Ola section → pickup experience
  pickupIssue.setChoices([pickupIssue.createChoice('Yes', pIssue), pickupIssue.createChoice('No', pWait)]);
  cancelled.setChoices([cancelled.createChoice('Yes', pCancel), cancelled.createChoice('No', pCompare)]);
  followUp.setChoices([followUp.createChoice('Yes', pContact), followUp.createChoice('No', SUBMIT)]);

  Logger.log('Edit URL: ' + form.getEditUrl());
  Logger.log('Live URL: ' + form.getPublishedUrl());
}
