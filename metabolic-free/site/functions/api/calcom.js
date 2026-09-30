// Cloudflare Pages Function: POST /api/calcom
// Receives Cal.com webhooks for the discovery call and tags the person in Systeme.io, so the right
// email automation runs by itself:
//   booked / rescheduled  → "call booked" tag: stop the "book a call" nudges, send prep info
//   cancelled             → "call cancelled" tag: send a rebook email
//   no-show (7 min late)  → "call no-show" tag: send "sorry we missed you" + rebook link
// Cal.com already emails the coach when a call is booked, cancelled or rescheduled.
//
// Cal.com → Settings → Developer → Webhooks:
//   Subscriber URL  https://metabolicgfcxtremefit.com/api/calcom
//   Secret          same value as CALCOM_WEBHOOK_SECRET below
//   Triggers        Booking created, Booking canceled, Booking rescheduled,
//                   After guests didn't join cal video (7 min), Booking no-show updated
//
// Cloudflare Pages → Settings → Environment variables:
//   CALCOM_WEBHOOK_SECRET     (required) any long random string, also pasted into Cal.com
//   SYSTEME_API_KEY           (required) same key as /api/lead
//   SYSTEME_TAG_CALL_BOOKED   (optional) Systeme.io tag ids; a missing one is skipped
//   SYSTEME_TAG_CALL_CANCELLED
//   SYSTEME_TAG_CALL_NO_SHOW

const API = "https://api.systeme.io/api";

const json = (body, status = 200) =>
  new Response(JSON.stringify(body), { status, headers: { "Content-Type": "application/json" } });

async function validSignature(raw, signature, secret) {
  if (!signature || !/^[0-9a-f]+$/i.test(signature)) return false;
  const key = await crypto.subtle.importKey("raw", new TextEncoder().encode(secret),
    { name: "HMAC", hash: "SHA-256" }, false, ["verify"]);
  const bytes = new Uint8Array(signature.match(/../g).map((h) => parseInt(h, 16)));
  return crypto.subtle.verify("HMAC", key, bytes, new TextEncoder().encode(raw));
}

// Which tag to add and which to remove for each Cal.com event.
function plan(event, payload, env) {
  const booked = env.SYSTEME_TAG_CALL_BOOKED, cancelled = env.SYSTEME_TAG_CALL_CANCELLED,
    noShow = env.SYSTEME_TAG_CALL_NO_SHOW;
  switch (event) {
    case "BOOKING_CREATED":
    case "BOOKING_RESCHEDULED":
      return { add: [booked], remove: [cancelled, noShow] };
    case "BOOKING_CANCELLED":
      return { add: [cancelled], remove: [booked] };
    case "AFTER_GUESTS_CAL_VIDEO_NO_SHOW":
      return { add: [noShow], remove: [booked] };
    case "BOOKING_NO_SHOW_UPDATED":
      // Coach marked (or unmarked) the guest as a no-show in Cal.com.
      return (payload.attendees || []).some((a) => a.noShow)
        ? { add: [noShow], remove: [booked] } : { add: [], remove: [noShow] };
    default:
      return null;
  }
}

export async function onRequestPost({ request, env }) {
  if (!env.CALCOM_WEBHOOK_SECRET || !env.SYSTEME_API_KEY) return json({ ok: false, error: "not_configured" }, 503);

  const raw = await request.text();
  if (!(await validSignature(raw, request.headers.get("x-cal-signature-256"), env.CALCOM_WEBHOOK_SECRET))) {
    return json({ ok: false, error: "bad_signature" }, 401);
  }
  let body;
  try { body = JSON.parse(raw); } catch { return json({ ok: false, error: "bad_json" }, 400); }

  const payload = body.payload || {};
  const steps = plan(body.triggerEvent, payload, env);
  if (!steps) return json({ ok: true, ignored: body.triggerEvent });

  // Guests only: the coach (host) is never tagged.
  const hostEmail = String(payload.organizer?.email || payload.hostEmail || "").toLowerCase();
  const guests = (payload.attendees || [])
    .map((a) => ({ email: String(a.email || "").trim().toLowerCase(), name: String(a.name || "").split(" ")[0] }))
    .filter((g) => /^[^@\s]+@[^@\s]+\.[a-z]{2,}$/i.test(g.email) && g.email !== hostEmail);

  const headers = { "X-API-Key": env.SYSTEME_API_KEY, "Content-Type": "application/json", Accept: "application/json" };
  const add = steps.add.filter(Boolean), remove = steps.remove.filter(Boolean);

  for (const g of guests) {
    // Find the contact; people can book straight from the link without taking the quiz first.
    const found = await fetch(`${API}/contacts?email=${encodeURIComponent(g.email)}`, { headers });
    let contactId = found.ok ? ((await found.json()).items || [])[0]?.id : undefined;
    if (!contactId) {
      const created = await fetch(`${API}/contacts`, { method: "POST", headers,
        body: JSON.stringify({ email: g.email, fields: [{ slug: "first_name", value: g.name.slice(0, 60) }] }) });
      if (!created.ok) return json({ ok: false, error: "systeme_create_failed", status: created.status }, 502);
      contactId = (await created.json()).id;
    }
    await Promise.all([
      ...remove.map((tagId) => fetch(`${API}/contacts/${contactId}/tags/${Number(tagId)}`, { method: "DELETE", headers })),
      ...add.map((tagId) => fetch(`${API}/contacts/${contactId}/tags`, { method: "POST", headers,
        body: JSON.stringify({ tagId: Number(tagId) }) })),
    ]);
  }
  return json({ ok: true, event: body.triggerEvent, contacts: guests.length });
}

export const onRequest = () => json({ ok: false, error: "method_not_allowed" }, 405);
