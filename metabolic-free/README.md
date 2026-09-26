# Metabolic Free: client acquisition system

**Goal:** the coach only coaches. Everything upstream of the first session
(attention → lead → nurture → booking) and everything around retention
(reminders, check-ins, referrals, reporting) is run by a set of narrow agents
with a single decision layer on top.

> **Metabolic Free.** Use every tool humanity has built (GLP-1s, hormone
> therapy, the Lumen metabolic breath device, training, nutrition) to get
> metabolically healthy now, while building the habits that eventually let
> behavior replace the tools.

## The system on one page

```
 ATTENTION            CAPTURE              NURTURE               CONVERT             COACH (you)          RETAIN / EXPAND
 ───────────          ─────────            ─────────             ─────────           ───────────          ───────────────
 Organic social  ─┐                        Email (14-day)   ─┐
 Meta ads        ─┼─► Metabolic Score ───► SMS (opt-in)     ─┼─► Discovery call ───► Biweekly coaching ─► Check-ins, wins,
 Google search   ─┤   quiz + landing page  Retargeting ads  ─┘   (booked by agent)   session + Lumen      referrals, reviews,
 LinkedIn/B2B    ─┤   (lead + score +                            → enrollment +     data review          upgrades to
 Referrals       ─┘    consent in CRM)                            Lumen shipped                           telehealth (Rx)
                               │                                                             │
                               └──────────────── DECISION LAYER + EVIDENCE LOG ──────────────┘
                     every agent choice is logged: what it chose, why, and what happened after
```

The decision-layer idea comes from the "state → action → evidence" pattern
(the harness picks, validates against policy, executes, then records
evidence). Here it means: **no agent spends money, sends a message, or makes a
health claim without passing a policy check, and every action is scored
against the outcome it was supposed to produce (booked calls, enrolled
clients, retention).** That is how the system improves and how you know *why*
it improved.

## Folder map

| Path | What it is |
|---|---|
| [`docs/00-questions-for-coach.md`](docs/00-questions-for-coach.md) | **Start here.** The inputs I need from you to turn defaults into your real numbers. |
| [`docs/01-system-architecture.md`](docs/01-system-architecture.md) | Funnel stages, data flow, tool stack, decision layer. |
| [`docs/02-offer-and-messaging.md`](docs/02-offer-and-messaging.md) | Ideal clients, offer ladder, Lumen offer, brand voice, core messages. |
| [`docs/03-client-economics.md`](docs/03-client-economics.md) | What a client is worth to the business (LTV, CAC, capacity, Lumen payback). |
| [`docs/04-compliance-guardrails.md`](docs/04-compliance-guardrails.md) | Hard rules every agent enforces (health claims, GLP-1 ads, HIPAA, SMS, LinkedIn). |
| [`docs/05-launch-plan.md`](docs/05-launch-plan.md) | 90-day rollout, week by week. |
| [`agents/`](agents/) | One spec per agent: job, inputs, outputs, KPIs, guardrails, handoffs. |
| [`campaigns/hero-video.md`](campaigns/hero-video.md) | **Launch playbook:** one video, one offer, blasted to every channel (Higgsfield production brief). |
| [`campaigns/warm-list-launch.md`](campaigns/warm-list-launch.md) | **Day-one blast** to the ~600-contact warm list: emails, compliant texts, the math. |
| [`tools/prepare_list.py`](tools/prepare_list.py) | Cleans the contact file and splits it by email / SMS consent (output is git-ignored). |
| [`campaigns/`](campaigns/) | Ready-to-use copy: Meta, Google, email, SMS, social calendar, LinkedIn outreach. |
| [`site/`](site/) | Website: Home + Metabolic Score quiz, Program, **GFC Lab** (Altrohealth), founding-spots counter → waitlist. Settings in `site/config.js`. |
| [`site/app/`](site/app/) | **Client training platform:** daily check-in (Lumen, protein, walk, weight), 12-week program, progress, GFC Lab; coach roster with at-risk and renewal flags. Demo mode until Supabase is connected. |
| [`data/platform.sql`](data/platform.sql) | Platform database + security rules (Supabase). No medical data: that stays in Altrohealth. |
| [`campaigns/launch-emails.md`](campaigns/launch-emails.md) | **The 5 launch emails, ready to paste**, plus resend and waitlist emails. |
| [`data/schema.sql`](data/schema.sql) | Lead/client pipeline + evidence log (Postgres / Supabase). |
| [`tools/economics.py`](tools/economics.py) | Calculator: client value, allowable ad spend, coach capacity, Lumen payback. |

## What you do vs. what the system does

| You (coach) | The system |
|---|---|
| Biweekly coaching sessions | Content creation + posting |
| Record 1 short video/week (raw, phone is fine) | Ads: build, launch, test, pause losers, scale winners |
| Approve the weekly 1-page report (5 min) | Quiz, lead scoring, email + SMS nurture |
| Approve new health claims / new ad angles once | Booking, reminders, no-show recovery |
| Clinical decisions (or your licensed prescriber) | Onboarding, Lumen shipping trigger, check-ins, referrals, reviews |
