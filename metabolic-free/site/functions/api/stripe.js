// Cloudflare Pages Function: POST /api/stripe
// Receives Stripe webhooks for PT Distinction package signups and tags the person
// "client_signed_up" in Systeme.io. That tag unsubscribes them from every campaign
// (Nurture, Launch, No-Show, Attended Follow-up, Long-Term Nurture), so a paying client
// never receives another sales email.
//
// Without this, the only thing that stops those emails is the coach remembering to tag by
// hand — which is how a new client ends up getting "Still deciding?" two days after paying.
//
// PT Distinction subscriptions are charged through the coach's own Stripe account, so the
// events land in that account's dashboard like any other.
//
// Stripe → Developers → Webhooks → Add endpoint:
//   Endpoint URL  https://metabolicgfcxtremefit.com/api/stripe
//   Events        checkout.session.completed
//                 customer.subscription.created
//                 invoice.payment_succeeded
//   Then copy the signing secret (whsec_...) into STRIPE_WEBHOOK_SECRET below.
//
// Cloudflare Pages → Settings → Environment variables:
//   STRIPE_WEBHOOK_SECRET        (required) the endpoint's signing secret, "whsec_..."
//   SYSTEME_API_KEY              (required) same key as /api/lead
//   SYSTEME_TAG_CLIENT_SIGNED_UP (required) Systeme.io tag id for "client_signed_up"
//   STRIPE_SECRET_KEY            (optional) "sk_live_..."; only used to look up a customer's
//                                email when the event itself doesn't carry one
//
// Environment changes need a new deployment before they take effect.

const API = "https://api.systeme.io/api";
const STRIPE_API = "https://api.stripe.com/v1";

const json = (body, status = 200) =>
  new Response(JSON.stringify(body), { status, headers: { "Content-Type": "application/json" } });

const toHex = (buf) =>
  [...new Uint8Array(buf)].map((b) => b.toString(16).padStart(2, "0")).join("");

async function hmacHex(secret, data) {
  const key = await crypto.subtle.importKey("raw", new TextEncoder().encode(secret),
    { name: "HMAC", hash: "SHA-256" }, false, ["sign"]);
  return toHex(await crypto.subtle.sign("HMAC", key, new TextEncoder().encode(data)));
}

function safeEqual(a, b) {
  if (a.length !== b.length) return false;
  let diff = 0;
  for (let i = 0; i < a.length; i++) diff |= a.charCodeAt(i) ^ b.charCodeAt(i);
  return diff === 0;
}

// Stripe-Signature looks like: t=1492774577,v1=5257a869e7...,v1=<older secret>
// The signed payload is "<t>.<raw body>". The timestamp check blocks replays.
async function validSignature(raw, header, secret, toleranceSec = 300) {
  const parts = String(header || "").split(",").map((p) => p.trim().split("="));
  const t = parts.find(([k]) => k === "t")?.[1];
  const sigs = parts.filter(([k]) => k === "v1").map(([, v]) => v);
  if (!t || !/^\d+$/.test(t) || !sigs.length) return false;
  if (Math.abs(Math.floor(Date.now() / 1000) - Number(t)) > toleranceSec) return false;
  const expected = await hmacHex(secret, `${t}.${raw}`);
  return sigs.some((s) => safeEqual(s, expected));
}

const isEmail = (e) => /^[^@\s]+@[^@\s]+\.[a-z]{2,}$/i.test(e);

// Stripe puts the buyer's email in a different place depending on how they paid.
function emailFrom(obj) {
  return String(obj.customer_details?.email || obj.customer_email || obj.receipt_email ||
    obj.billing_details?.email || "").trim().toLowerCase();
}

function nameFrom(obj) {
  return String(obj.customer_details?.name || obj.customer_name || "").split(" ")[0];
}

// customer.subscription.created carries only a customer id, so fetch the customer when we can.
async function emailFromCustomer(customerId, secretKey) {
  if (!customerId || !secretKey) return { email: "", name: "" };
  const res = await fetch(`${STRIPE_API}/customers/${encodeURIComponent(customerId)}`, {
    headers: { Authorization: `Bearer ${secretKey}` },
  });
  if (!res.ok) return { email: "", name: "" };
  const c = await res.json();
  return { email: String(c.email || "").trim().toLowerCase(), name: String(c.name || "").split(" ")[0] };
}

export async function onRequestPost({ request, env }) {
  if (!env.STRIPE_WEBHOOK_SECRET || !env.SYSTEME_API_KEY || !env.SYSTEME_TAG_CLIENT_SIGNED_UP) {
    return json({ ok: false, error: "not_configured" }, 503);
  }

  const raw = await request.text();
  if (!(await validSignature(raw, request.headers.get("stripe-signature"), env.STRIPE_WEBHOOK_SECRET))) {
    return json({ ok: false, error: "bad_signature" }, 401);
  }
  let event;
  try { event = JSON.parse(raw); } catch { return json({ ok: false, error: "bad_json" }, 400); }

  const PAID = ["checkout.session.completed", "customer.subscription.created", "invoice.payment_succeeded"];
  if (!PAID.includes(event.type)) return json({ ok: true, ignored: event.type });

  const obj = event.data?.object || {};

  // A checkout session that hasn't actually been paid is not a signup.
  if (event.type === "checkout.session.completed" && obj.payment_status === "unpaid") {
    return json({ ok: true, ignored: "unpaid" });
  }

  let email = emailFrom(obj), name = nameFrom(obj);
  if (!isEmail(email)) {
    const customerId = typeof obj.customer === "string" ? obj.customer : obj.customer?.id;
    ({ email, name } = await emailFromCustomer(customerId, env.STRIPE_SECRET_KEY));
  }
  // Nothing to match on. 200 so Stripe doesn't retry an event we can never resolve.
  if (!isEmail(email)) return json({ ok: true, skipped: "no_email", event: event.type });

  const headers = { "X-API-Key": env.SYSTEME_API_KEY, "Content-Type": "application/json", Accept: "application/json" };

  // Find the contact. They normally exist already (quiz lead, or a Cal.com booking), but
  // someone can buy straight from the pricing page without ever being a lead.
  const found = await fetch(`${API}/contacts?email=${encodeURIComponent(email)}`, { headers });
  let contactId = found.ok ? ((await found.json()).items || [])[0]?.id : undefined;
  if (!contactId) {
    const created = await fetch(`${API}/contacts`, { method: "POST", headers,
      body: JSON.stringify({ email, fields: [{ slug: "first_name", value: name.slice(0, 60) }] }) });
    if (!created.ok) return json({ ok: false, error: "systeme_create_failed", status: created.status }, 502);
    contactId = (await created.json()).id;
  }

  const tagged = await fetch(`${API}/contacts/${contactId}/tags`, { method: "POST", headers,
    body: JSON.stringify({ tagId: Number(env.SYSTEME_TAG_CLIENT_SIGNED_UP) }) });
  if (!tagged.ok) return json({ ok: false, error: "systeme_tag_failed", status: tagged.status }, 502);

  return json({ ok: true, event: event.type });
}

export const onRequest = () => json({ ok: false, error: "method_not_allowed" }, 405);
