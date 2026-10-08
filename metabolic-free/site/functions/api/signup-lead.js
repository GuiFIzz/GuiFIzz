// Cloudflare Pages Function: POST /api/signup-lead
// Captures a "ready to enroll" lead — someone who already knows the program and wants to
// skip the quiz/call funnel. Tags the contact in Systeme.io (reuses quiz_lead, same as the
// Peptide Guide — no dedicated tag, the plan is capped at 10) and pings Slack immediately so
// Coach Gui can follow up fast, since this is a high-intent, time-sensitive lead.
//
// This is deliberately simple/temporary: once the white-labeled client platform is live,
// this button will route straight there instead of through a lead form.
//
// Cloudflare Pages → Settings → Environment variables:
//   SYSTEME_API_KEY          (required) same key as /api/lead
//   SYSTEME_TAG_QUIZ         (required) same tag id as /api/lead's quiz_lead tag
//   SLACK_HULK_WEBHOOK_URL   (optional) same Slack webhook Hulk uses — missing just skips the ping

const API = "https://api.systeme.io/api";

const json = (body, status = 200) =>
  new Response(JSON.stringify(body), { status, headers: { "Content-Type": "application/json" } });

export async function onRequestPost({ request, env, waitUntil }) {
  let lead;
  try { lead = await request.json(); } catch { return json({ ok: false, error: "bad_json" }, 400); }

  const email = String(lead.email || "").trim().toLowerCase();
  const first_name = String(lead.first_name || "").slice(0, 60);
  const phone = String(lead.phone || "").slice(0, 30);
  if (!/^[^@\s]+@[^@\s]+\.[a-z]{2,}$/i.test(email)) {
    return json({ ok: false, error: "invalid_email" }, 400);
  }
  if (!env.SYSTEME_API_KEY) return json({ ok: false, error: "not_configured" }, 503);

  const headers = { "X-API-Key": env.SYSTEME_API_KEY, "Content-Type": "application/json", Accept: "application/json" };
  const fields = [{ slug: "first_name", value: first_name }];
  if (phone) fields.push({ slug: "phone_number", value: phone });

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

  if (env.SLACK_HULK_WEBHOOK_URL) {
    const text = `:tada: *Ready-to-enroll lead* — wants to sign up directly, skipped the quiz/call.\n*Name:* ${first_name || "(none given)"}\n*Email:* ${email}${phone ? `\n*Phone:* ${phone}` : ""}\n\n_Follow up fast — this is a warm lead._`;
    waitUntil(fetch(env.SLACK_HULK_WEBHOOK_URL, {
      method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ text }),
    }).catch(() => {}));
  }

  return json({ ok: true });
}

export const onRequest = () => json({ ok: false, error: "method_not_allowed" }, 405);
