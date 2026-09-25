# Agents

Seven narrow agents. Each has **one job, one KPI, and hard limits.** They share
the CRM/database and the `decision_log` (see `../docs/01-system-architecture.md`).
Every action goes through PROPOSE → VALIDATE → EXECUTE → EVIDENCE.

| Agent | Job | KPI | Runs |
|---|---|---|---|
| [Content](#1-content-agent) | Turn the message bank + coach videos into daily posts | Quiz starts from organic | Daily |
| [Ads](#2-ads-agent) | Build, test, kill, scale paid campaigns | Cost per enrolled client | Daily check, weekly plan |
| [Nurture](#3-nurture-agent) | Move leads to a booked call via email/SMS | Lead → booked % | Event-driven |
| [Booking](#4-booking-agent) | Book, remind, recover no-shows, prep the coach | Show rate | Event-driven |
| [Retention](#5-retention-agent) | Keep clients engaged between sessions | Monthly churn | Daily |
| [Outreach](#6-outreach-agent) | B2B partnerships (employers, doctors, gyms) | Partner meetings / month | Weekly |
| [Reporting](#7-reporting-agent) | Score decisions vs. outcomes, write the weekly report, update rules | Report accuracy | Weekly |

---

## 1. Content agent
- **Inputs:** message bank (`docs/02`), weekly coach video, last week's winning hooks (from Reporting), content calendar.
- **Outputs:** 5 feed posts + 5–7 stories + 2–3 short-form video cuts/week; captions with quiz CTA and UTM link.
- **Auto:** schedule posts that reuse approved claims. **Approve:** any new health claim or stat.
- **Guardrails:** claim filter, source required for every stat, no before/after without consent on file.
- **Handoff:** best-performing organic posts → Ads agent as creative candidates.

## 2. Ads agent
- **Inputs:** max CPL / max CAC from `tools/economics.py`, weekly budget cap, approved angles, conversion data by ad id.
- **Outputs:** campaign structure, creatives + copy variants, daily kill/scale actions.
- **Rules:** kill if CPL > 1.5× max after 3 days and ≥ $50 spent. Scale +20% if cost per booked call is under target 3 days running. Never exceed the monthly cap. Test ≤ 3 new creatives per ad set per week.
- **Auto:** pause, ≤ 20% scale, new variant of an approved angle. **Approve:** new angle, cap change, any medication mention.
- **Guardrails:** Meta special-category and personal-attribute rules, LegitScript gate, no health data in events.

## 3. Nurture agent
- **Inputs:** new lead + segment + score, sequences in `campaigns/email-sequence.md` and `sms-sequence.md`.
- **Outputs:** segmented sequences; replies answered with FAQ knowledge; hot leads (clicked booking link, replied "yes") flagged.
- **Rules:** exit the sequence when a call is booked; downgrade to the monthly newsletter after 30 days without engagement.
- **Guardrails:** consent check before every SMS, quiet hours, frequency caps, human handoff for medical questions.

## 4. Booking agent
- **Inputs:** coach calendar, lead record.
- **Outputs:** confirmations, reminders (24 h email, 2 h SMS, 10 min SMS), a **pre-call brief** for the coach
  (score, segment, goals, quiz answers, source), no-show recovery (re-book within 1 h), post-call enrollment link + agreement.
- **KPI:** show rate > 70%.
- **Guardrails:** red-flag leads go to the "see your physician first" path and are flagged to the coach.

## 5. Retention agent
- **Inputs:** sessions, Lumen log activity (if the Lumen/partner export is available, or client self-report), payments.
- **Outputs:** biweekly session reminders, mid-cycle check-in ("What's your Lumen score trend this week?"),
  win celebrations, a **churn-risk alert** to the coach (missed session, no logs 5+ days, failed payment),
  testimonial + review requests at milestones (day 45, 90), referral asks after a win.
- **KPI:** churn < 8%/month.

## 6. Outreach agent
- **Inputs:** manually built target lists (Sales Navigator, local employers, clinics, gyms). **No scraping.**
- **Outputs:** personalized drafts for the coach to send or approve (`campaigns/linkedin-outreach.md`), follow-up reminders.
- **Limits:** ≤ 20 new contacts/day; opt-outs honored forever.

## 7. Reporting agent
- **Inputs:** CRM, ad platforms (Supermetrics or native), `decision_log`.
- **Outputs:** Monday **1-page report**: leads, CPL, booked, show, close, enrolled, active, churn, CAC, LTV:CAC,
  top 3 decisions that helped or hurt, 3 recommended actions awaiting approval. It also fills `verdict` on decisions
  older than 7/30 days and updates the "winning rules" list used by Content and Ads.
