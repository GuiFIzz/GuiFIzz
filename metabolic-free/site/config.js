// Metabolic Flex: one settings file for every page (site + client platform).
// Fill these in before launch. Nothing here is secret: the Supabase "anon" key is
// designed to be public and is protected by row-level security (see data/platform.sql).
window.MF_CONFIG = {
  FOUNDING_SPOTS: 30,        // after this many enrollments, every CTA becomes "join the waitlist"
  SPOTS_TAKEN: 0,            // updated by hand, or live from Supabase once connected
  BOOKING_URL: "https://cal.com/gfcxtreme-fitness-nmylwf/30min", // discovery-call calendar link (Cal.com)
  LEAD_ENDPOINT: "/api/lead", // Cloudflare Pages Function → Systeme.io (functions/api/lead.js)
  GUIDE_LEAD_ENDPOINT: "/api/guide-lead", // Gated-content lead capture (functions/api/guide-lead.js)
  HULK_ENDPOINT: "/api/hulk", // Hulk AI chat widget (functions/api/hulk.js)
  ALTROHEALTH_URL: "https://altroapp.com/gfcxtremefit", // GFC Lab: Altrohealth storefront/intake link
  ALTROHEALTH_EMBED: false,  // altroapp.com blocks iframe embedding (confirmed "refused to connect") — opens in a new tab instead
  FORTIFY_URL: "https://us.fullscript.com/s/gfcxtremefit/shop", // GFC Fortify: Fullscript storefront
  FORTIFY_EMBED: false,      // Fullscript sends X-Frame-Options: DENY (confirmed) — opens in a new tab instead
  SUPABASE_URL: "",          // client platform backend; empty = demo mode
  SUPABASE_ANON_KEY: "",
  COACH_NAME: "Coach Gui",
  // The training app's public package list, which also carries the reason the program
  // has a three-month minimum. The app is the source of truth for that copy, so the
  // pricing page reads it rather than keeping a second version that drifts.
  // Empty until app.metabolicgfcxtremefit.com is live — the page falls back to the
  // copy written into the HTML, which is the same text.
  PACKAGES_ENDPOINT: "",     // e.g. "https://app.metabolicgfcxtremefit.com/api/gfc/packages"
};

window.MF = {
  spotsLeft() {
    const c = window.MF_CONFIG;
    return Math.max(0, c.FOUNDING_SPOTS - c.SPOTS_TAKEN);
  },
  // Never print a running count: a hard number goes stale the moment someone joins,
  // and a wrong number on a live page is worse than no number. Scarcity is stated,
  // not counted. FOUNDING_SPOTS/SPOTS_TAKEN still drive the waitlist switch below.
  renderSpots(el) {
    if (!el) return;
    const left = this.spotsLeft();
    el.textContent = left > 0
      ? "Founding spots are limited"
      : "Founding spots full: join the waitlist";
    el.classList.toggle("full", left === 0);
  },
  esc(s) {
    return String(s).replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
  },

  // Replace the "Why three months?" copy with whatever the training app is serving.
  //
  // THE PAGE ALREADY READS CORRECTLY WITHOUT THIS. The same words are written into the
  // HTML, so the section works with no JavaScript, with the app down, before the app
  // exists at all, and for a crawler. This only keeps the two from drifting once the
  // coach edits the copy in one place — which is the whole reason the app serves it.
  //
  // Everything below writes with textContent, never innerHTML. The text arrives over the
  // network, and a page that injected it as markup would be one compromised response away
  // from running someone else's script on the checkout page.
  async renderWhy(root) {
    const url = window.MF_CONFIG.PACKAGES_ENDPOINT;
    if (!root || !url) return;

    let why;
    try {
      // 4s: past that the visitor has read the static copy and a swap would only make
      // the page jump under them. No credentials — this endpoint is public by design.
      const ctl = new AbortController();
      const timer = setTimeout(() => ctl.abort(), 4000);
      const res = await fetch(url, { signal: ctl.signal, credentials: "omit" });
      clearTimeout(timer);
      if (!res.ok) return;
      why = (await res.json()).why;
    } catch { return; }          // offline, blocked, slow, not deployed — keep the HTML

    if (!why || !why.short) return;

    const set = (sel, text) => {
      const el = root.querySelector(sel);
      if (el && text) el.textContent = text;
    };
    set("[data-why=heading]", why.heading);
    set("[data-why=short]", why.short);
    set("[data-why=closing]", why.closing);
    set("[data-why=disclaimer]", why.disclaimer);

    const list = root.querySelector("[data-why=points]");
    if (list && Array.isArray(why.points) && why.points.length) {
      list.replaceChildren(...why.points.map((p) => {
        const li = document.createElement("li");
        li.textContent = p;
        return li;
      }));
    }
    root.dataset.source = "app";  // so you can tell in devtools which copy you are reading
  },
};
