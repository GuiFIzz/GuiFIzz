// Metabolic Score quiz engine — shared by index.html (quiz in context) and
// score.html (quiz on its own, the destination every email CTA points at).
//
// It lives in one file on purpose. Both pages POST the same payload shape to
// /api/lead, so a scoring or field change made in only one of them would send
// Systeme two different contracts and the drift would be invisible until a
// lead came in wrong.
//
// Call MF_QUIZ.init() once the page has #progress and #stage in the DOM.
// Options:
//   prefillQ1 — index of an answer to question 1, already chosen elsewhere
//               (an email CTA). Records it and opens on question 2.
(function () {
  // ---- Config -------------------------------------------------------------
  // POST target for leads (CRM webhook, e.g. GoHighLevel inbound webhook or a Supabase edge function).
  // All settings live in config.js (shared by every page).
  const { LEAD_ENDPOINT, BOOKING_URL } = window.MF_CONFIG;
  const FULL = MF.spotsLeft() <= 0;
  
  // Each answer adds "risk points" (higher = more dysfunction) and can tag a segment or red flag.
  const QUESTIONS = [
    { q: "How is your energy in the afternoon?", a: [
      ["Steady all day", 0], ["A small dip", 4], ["I crash most days", 10] ] },
    { q: "Where do you carry extra weight?", a: [
      ["I'm at a weight I'm happy with", 0], ["Mostly hips/legs", 4], ["Mostly belly/waist", 12] ] },
    { q: "Has a doctor ever mentioned your blood sugar or A1c?", a: [
      ["No / normal", 0], ["Told it's borderline or pre-diabetic", 14, "prediabetic"],
      ["Diagnosed type 2 diabetes", 18, "type2"], ["I have type 1 diabetes or use insulin", 18, "type2", true] ] },
    { q: "How often do you get strong cravings for sugar or carbs?", a: [
      ["Rarely", 0], ["A few times a week", 5], ["Daily", 10] ] },
    { q: "Strength training in a typical week?", a: [
      ["2+ sessions", 0], ["Once, or on and off", 5], ["None", 10] ] },
    { q: "Are you using or considering a GLP-1 medication?", a: [
      ["No", 0], ["Considering it", 4, "glp1"], ["Currently using one", 6, "glp1"] ] },
    { q: "Do you notice hormone-related changes (sleep, mood, libido, hot flashes)?", a: [
      ["No", 0], ["Some", 5, "hormones"], ["A lot", 8, "hormones"] ] },
    { q: "How is your sleep?", a: [
      ["7+ hours, rested", 0], ["Often short or broken", 6], ["Poor most nights", 10] ] },
    { q: "Any of these apply: pregnant, eating-disorder history, heart condition?", a: [
      ["None of these", 0], ["Yes, one or more", 0, null, true] ] },
  ];
  const MAX = QUESTIONS.reduce((s, x) => s + Math.max(...x.a.map(o => o[1])), 0);
  
  const SEGMENT_LINES = {
    type2:        "You're in our Power Warrior track: coaching that works alongside your doctor's care.",
    prediabetic:  "You're in our Power Warrior track. Borderline is the best window to act.",
    glp1:         "Your focus: keep your muscle while you lose fat, and build the plan for after medication.",
    hormones:     "Your focus: energy, body composition, and whether a hormone evaluation makes sense.",
    weight_energy:"Your focus: steady energy, fat loss, and keeping your muscle.",
  };
  const SEGMENT_PRIORITY = ["type2", "prediabetic", "glp1", "hormones"];
  
  let i = 0, points = 0, tags = new Set(), redFlag = false;
  const answers = [];
  const stage = document.getElementById("stage");
  const progress = document.getElementById("progress");
  const el = (h) => { const d = document.createElement("div"); d.innerHTML = h; return d; };
  
  function renderQuestion() {
    progress.style.width = (i / (QUESTIONS.length + 1) * 100) + "%";
    const item = QUESTIONS[i];
    stage.replaceChildren(el(`<h2 style="margin-top:0">${item.q}</h2>`));
    item.a.forEach(([label, pts, tag, flag]) => {
      const b = document.createElement("button");
      b.className = "opt"; b.type = "button"; b.textContent = label;
      b.onclick = () => {
        points += pts; if (tag) tags.add(tag); if (flag) redFlag = true;
        answers.push({ question: item.q, answer: label });
        i++; i < QUESTIONS.length ? renderQuestion() : renderCapture();
      };
      stage.appendChild(b);
    });
  }
  
  function scoreAndSegment() {
    // Higher score = healthier (100 = metabolic dysfunction free).
    const score = Math.max(0, Math.round(100 - points / MAX * 100));
    const segment = SEGMENT_PRIORITY.find(s => tags.has(s)) || "weight_energy";
    return { score, segment };
  }
  
  function renderCapture() {
    progress.style.width = (QUESTIONS.length / (QUESTIONS.length + 1) * 100) + "%";
    stage.replaceChildren(el(`
      <h2 style="margin-top:0">Your score is ready.</h2>
      <p class="sub">Where should we send your personalized breakdown and 7-Day Metabolic Reset?</p>
      <form id="lead" novalidate>
        <label for="fn">First name</label><input id="fn" type="text" autocomplete="given-name" required>
        <label for="em">Email</label><input id="em" type="email" autocomplete="email" required>
        <label for="ph">Mobile (optional)</label><input id="ph" type="tel" autocomplete="tel">
        <div class="consent"><input id="c_email" type="checkbox" required>
          <label for="c_email" style="margin:0">Email me my results and the 7-Day Metabolic Reset. I can unsubscribe anytime. <a href="privacy.html" target="_blank">Privacy policy</a></label></div>
        <div class="consent"><input id="c_sms" type="checkbox">
          <label for="c_sms" style="margin:0">Optional: I agree to receive text messages from Metabolic Flex about my results and coaching, including automated messages. Up to 4 msgs/week. Msg &amp; data rates may apply. Reply STOP to opt out. Consent is not a condition of purchase.</label></div>
        <button class="btn" id="go" type="submit" disabled>See my score</button>
      </form>`));
    const f = document.getElementById("lead");
    const check = () => document.getElementById("go").disabled =
      !(f.fn.value.trim() && /\S+@\S+\.\S+/.test(f.em.value) && f.c_email.checked);
    f.addEventListener("input", check);
    f.addEventListener("submit", async (e) => {
      e.preventDefault();
      const { score, segment } = scoreAndSegment();
      const params = new URLSearchParams(location.search);
      const payload = {
        first_name: f.fn.value.trim(), email: f.em.value.trim(),
        phone: f.ph.value.trim() || null,
        email_consent: true, sms_consent: f.c_sms.checked && !!f.ph.value.trim(),
        metabolic_score: score, segment, red_flag: redFlag, answers,
        utm_source: params.get("utm_source"), utm_campaign: params.get("utm_campaign"),
        utm_content: params.get("utm_content"),
        timezone: Intl.DateTimeFormat().resolvedOptions().timeZone,
        waitlist: FULL,
      };
      if (LEAD_ENDPOINT) {
        try { await fetch(LEAD_ENDPOINT, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(payload) }); }
        catch (err) { console.warn("Lead submit failed", err); }
      }
      // Ad-platform event: name only, never health data (see docs/04-compliance-guardrails.md).
      if (window.fbq) fbq("track", "Lead");
      if (window.gtag) gtag("event", "generate_lead");
      renderResult(score, segment, f.fn.value.trim());
    });
  }
  
  function renderResult(score, segment, name) {
    progress.style.width = "100%";
    const cta = redFlag
      ? `<p>Based on your answers, please talk with your physician before starting a new nutrition or training program. We've sent your results by email, and the coach will reach out personally.</p>`
      : FULL
      ? `<p><b>All founding spots are taken, and you're on the waitlist.</b> You'll be first to hear when a spot opens.</p>`
      : `<p><a class="btn" href="${BOOKING_URL}">Book a free 30-minute strategy call</a></p>`;
    stage.replaceChildren(el(`
      <p class="eyebrow">${name ? MF.esc(name) + ", your" : "Your"} Metabolic Score</p>
      <div class="score">${score}<span style="font-size:24px;color:var(--muted)">/100</span></div>
      <p class="sub">${SEGMENT_LINES[segment]}</p>
      <p>Your 7-Day Metabolic Reset is ready — <a href="7-day-reset.html">read it here</a>, and a copy is on its way to your inbox. On a free call we'll map your first 30 days: training, meal timing, and whether tools like a Lumen device, GLP-1s, peptides or hormone therapy belong in your plan.</p>
      ${cta}
      <p class="note">The Metabolic Score is an educational self-assessment, not a diagnosis.</p>`));
    stage.scrollIntoView({ behavior: "smooth", block: "start" });
  }
  

  window.MF_QUIZ = {
    init(opts) {
      opts = opts || {};
      // Apply a first answer chosen in an email, but only if it really is one
      // of question 1's options. Test the raw string first: a missing param is
      // null, and Number(null) is 0, which would quietly record answer 0 and
      // skip the question for every ordinary visitor.
      const raw = opts.prefillQ1;
      const n = /^[0-9]+$/.test(String(raw ?? "")) ? Number(raw) : -1;
      if (n >= 0 && n < QUESTIONS[0].a.length) {
        const [label, pts, tag, flag] = QUESTIONS[0].a[n];
        points += pts; if (tag) tags.add(tag); if (flag) redFlag = true;
        answers.push({ question: QUESTIONS[0].q, answer: label });
        i = 1;
      }
      renderQuestion();
    },
  };
})();
