// Cloudflare Pages Function: POST /api/guide-lead
// Captures an email from a gated content download (e.g. the Peptide Guide) and tags the
// contact in Systeme.io. Separate from /api/lead (the Metabolic Score quiz) because this
// lead has no score/segment — just a name and email.
//
// Reuses the quiz_lead tag (not a dedicated one) so a guide download enters the same
// nurture sequence as a quiz-taker — same funnel, same "general lead" treatment, and no
// extra Systeme.io tag needed.
//
// Cloudflare Pages → Settings → Environment variables:
//   SYSTEME_API_KEY   (required) same key as /api/lead
//   SYSTEME_TAG_QUIZ  (required) same tag id as /api/lead's quiz_lead tag

const API = "https://api.systeme.io/api";

const json = (body, status = 200) =>
  new Response(JSON.stringify(body), { status, headers: { "Content-Type": "application/json" } });

export async function onRequestPost({ request, env }) {
  let lead;
  try { lead = await request.json(); } catch { return json({ ok: false, error: "bad_json" }, 400); }

  const email = String(lead.email || "").trim().toLowerCase();
  if (!/^[^@\s]+@[^@\s]+\.[a-z]{2,}$/i.test(email)) {
    return json({ ok: false, error: "invalid_email" }, 400);
  }
  if (!env.SYSTEME_API_KEY) return json({ ok: false, error: "not_configured" }, 503);

  const headers = { "X-API-Key": env.SYSTEME_API_KEY, "Content-Type": "application/json", Accept: "application/json" };
  const fields = [{ slug: "first_name", value: String(lead.first_name || "").slice(0, 60) }];

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

  if (env.SYSTEME_TAG_QUIZ) {
    await fetch(`${API}/contacts/${contactId}/tags`, { method: "POST", headers,
      body: JSON.stringify({ tagId: Number(env.SYSTEME_TAG_QUIZ) }) });
  }

  return json({ ok: true });
}

export const onRequest = () => json({ ok: false, error: "method_not_allowed" }, 405);
