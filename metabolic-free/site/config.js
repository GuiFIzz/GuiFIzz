// Metabolic Free: one settings file for every page (site + client platform).
// Fill these in before launch. Nothing here is secret: the Supabase "anon" key is
// designed to be public and is protected by row-level security (see data/platform.sql).
window.MF_CONFIG = {
  FOUNDING_SPOTS: 30,        // after this many enrollments, every CTA becomes "join the waitlist"
  SPOTS_TAKEN: 0,            // updated by hand, or live from Supabase once connected
  BOOKING_URL: "#book",      // discovery-call calendar link
  LEAD_ENDPOINT: "",         // CRM webhook that receives quiz leads
  ALTROHEALTH_URL: "",       // GFC Lab: your Altrohealth partner/intake link (ideally https://lab.metabolicgfcxtremefit.com)
  ALTROHEALTH_EMBED: true,   // true = show Altrohealth inside the GFC Lab tab (needs Altrohealth to allow embedding)
  SUPABASE_URL: "",          // client platform backend; empty = demo mode
  SUPABASE_ANON_KEY: "",
  COACH_NAME: "Coach",
};

window.MF = {
  spotsLeft() {
    const c = window.MF_CONFIG;
    return Math.max(0, c.FOUNDING_SPOTS - c.SPOTS_TAKEN);
  },
  renderSpots(el) {
    if (!el) return;
    const left = this.spotsLeft();
    el.textContent = left > 0
      ? `${left} of ${window.MF_CONFIG.FOUNDING_SPOTS} founding spots left`
      : "Founding spots full: join the waitlist";
    el.classList.toggle("full", left === 0);
  },
  esc(s) {
    return String(s).replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
  },
};
