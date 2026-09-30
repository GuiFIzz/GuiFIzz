// Cloudflare Pages Function: POST /api/lead
// Receives a Metabolic Score quiz submission and adds the person to Systeme.io.
// The Systeme.io API key stays here on the server (Cloudflare environment variable),
// never in the browser.
//
// Cloudflare Pages → Settings → Environment variables:
//   SYSTEME_API_KEY       (required) Systeme.io → Profile → Settings → Public API keys
//   SYSTEME_TAG_QUIZ      (optional) tag id added to every quiz lead, e.g. "quiz_lead"; starts the nurture sequence
//   SYSTEME_TAG_WAITLIST  (optional) tag id for people who signed up after the founding spots filled
//   SYSTEME_TAG_SEGMENTS  (optional) JSON map of segment → tag id, e.g. {"prediabetic":"123","glp1":"456"}
//
// Privacy: only name, email, phone (if SMS consent), score and a segment tag are sent. Individual
// quiz answers and red-flag details are NOT sent to Systeme.io (see docs/04-compliance-guardrails.md).

const API = "https://api.systeme.io/api";

const json = (body, status = 200) =>
  new Response(JSON.stringify(body), { status, headers: { "Content-Type": "application/json" } });

export async function onRequestPost({ request, env }) {
  let lead;
  try { lead = await request.json(); } catch { return json({ ok: false, error: "bad_json" }, 400); }

  const email = String(lead.email || "").trim().toLowerCase();
  if (!/^[^@\s]+@[^@\s]+\.[a-z]{2,}$/i.test(email) || !lead.email_consent) {
    return json({ ok: false, error: "invalid_email_or_consent" }, 400);
  }
  if (!env.SYSTEME_API_KEY) return json({ ok: false, error: "not_configured" }, 503);

  const headers = { "X-API-Key": env.SYSTEME_API_KEY, "Content-Type": "application/json", Accept: "application/json" };
  const fields = [{ slug: "first_name", value: String(lead.first_name || "").slice(0, 60) }];
  if (lead.sms_consent && lead.phone) fields.push({ slug: "phone_number", value: String(lead.phone).slice(0, 30) });

  // 1. Create the contact, or find the existing one.
  let contactId;
  const created = await fetch(`${API}/contacts`, { method: "POST", headers, body: JSON.stringify({ email, fields }) });
  if (created.ok) {
    contactId = (await created.json()).id;
  } else {
    const found = await fetch(`${API}/contacts?email=${encodeURIComponent(email)}`, { headers });
    const items = found.ok ? (await found.json()).items || [] : [];
    contactId = items[0]?.id;
    if (!contactId) return json({ ok: false, error: "systeme_create_failed", status: created.status }, 502);
  }

  // 2. Tag it: every quiz lead, the waitlist when spots are full, and the segment.
  let segmentTags = {};
  try { segmentTags = JSON.parse(env.SYSTEME_TAG_SEGMENTS || "{}"); } catch {}
  const tags = [env.SYSTEME_TAG_QUIZ, lead.waitlist ? env.SYSTEME_TAG_WAITLIST : null, segmentTags[lead.segment]]
    .filter(Boolean);
  await Promise.all(tags.map((tagId) =>
    fetch(`${API}/contacts/${contactId}/tags`, { method: "POST", headers, body: JSON.stringify({ tagId: Number(tagId) }) })));

  return json({ ok: true });
}

export const onRequest = () => json({ ok: false, error: "method_not_allowed" }, 405);
