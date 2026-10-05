// Metabolic Flex: one settings file for every page (site + client platform).
// Fill these in before launch. Nothing here is secret: the Supabase "anon" key is
// designed to be public and is protected by row-level security (see data/platform.sql).
window.MF_CONFIG = {
  FOUNDING_SPOTS: 30,        // after this many enrollments, every CTA becomes "join the waitlist"
  SPOTS_TAKEN: 0,            // updated by hand, or live from Supabase once connected
  BOOKING_URL: "https://cal.com/gfcxtreme-fitness-nmylwf/30min", // discovery-call calendar link (Cal.com)
  LEAD_ENDPOINT: "/api/lead", // Cloudflare Pages Function → Systeme.io (functions/api/lead.js)
  ALTROHEALTH_URL: "https://altroapp.com/gfcxtremefit", // GFC Lab: Altrohealth storefront/intake link
  ALTROHEALTH_EMBED: false,  // altroapp.com blocks iframe embedding (confirmed "refused to connect") — opens in a new tab instead
  FORTIFY_URL: "",           // GFC Fortify: your supplement store link
  FORTIFY_EMBED: true,       // true = try showing the store inside the GFC Fortify tab (most e-commerce platforms, Shopify included, block this via X-Frame-Options — if the embed stays blank, set this to false to just link out instead)
  SUPABASE_URL: "",          // client platform backend; empty = demo mode
  SUPABASE_ANON_KEY: "",
  COACH_NAME: "Coach Gui",
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
