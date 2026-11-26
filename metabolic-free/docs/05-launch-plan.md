# 90-day launch plan

## Phase 0: Foundation (Weeks 1–2). Nothing runs until this is done.
- [x] Coach answered core numbers ($299/mo 3-mo min, free Lumen at $199 cost to GFC Xtreme, $500/mo ads, 25 h/wk); calculator updated
- [ ] Domain + landing page live (`site/index.html`), privacy policy, terms, enrollment agreement (3-month minimum owed on early cancel; free Lumen ships after first payment)
- [ ] CRM set up (GoHighLevel or similar): pipeline stages match `data/schema.sql`
- [ ] Booking calendar (discovery-call slots), reminders
- [ ] Meta Business Manager, Pixel + Conversions API; Google Ads + GA4; **no health data in events**
- [ ] SMS number registered (A2P 10DLC); email domain authenticated (SPF, DKIM, DMARC)
- [ ] Load email + SMS sequences from `campaigns/`
- [ ] Coach records **the hero video: 1 body + 3 openings, 20 minutes** (see `campaigns/hero-video.md`)
- [ ] Telehealth: pick Altrohealth or OpenLoop, get the referral/intake flow + payout terms in writing, confirm whether their LegitScript covers your ads (see guardrails §2)
- [ ] **Warm list (~600):** run `tools/prepare_list.py`, verify emails, then launch per `campaigns/warm-list-launch.md`. Original note: export GFC Xtreme members, past clients and phone contacts → personal "I'm launching" message + quiz link (the fastest first 5 clients)

## Phase 1: Prove the funnel (Weeks 3–6). Small budget, learn fast.
- Budget: **$500/month ≈ $16/day on Meta** only: 1 ad set, the hero video × 3 openings (GLP-1 muscle / hidden pre-diabetes / every tool)
- **Blast day:** the same video goes to every free channel on launch day (see the distribution table in `hero-video.md`)
- Organic: 5 posts/week + 1 coach video/week, all pointing to the quiz
- Google: turn on a Business Profile + ask every past client for a review
- Goal: **~65 paid leads + organic/warm leads → first 5–8 enrolled clients** (most from the warm list and organic). Gets real CPL, show and close rates.
- Weekly: Reporting agent sends a 1-page report; coach approves kills/scales

## Phase 2: Scale what works (Weeks 7–10)
- Kill the losing angle, put 70% of budget on the winner, 30% on new tests
- Ad budget grows by the compounding rule in `03-client-economics.md` ($500 + $100 × active clients)
- Launch Google Search once the budget is ≥ $1,000/month (see `campaigns/google-ads.md`)
- Launch retargeting (quiz starters who didn't finish, leads who didn't book)
- Start the referral program (client gets a free month for each enrolled referral)
- Start LinkedIn B2B outreach (corporate wellness pilot)

## Phase 3: Systemize (Weeks 11–13)
- Switch Meta optimization from Lead → Schedule (booked call) once volume allows
- Add the Power Warrior group tier (breaks the capacity ceiling)
- Consider a closer/setter if discovery calls take > 5 h/week of the coach's time
- Evidence review: which agent decisions paid off? Update the rules

## Targets by Day 90 (placeholder, recalibrated after Phase 1)
| Metric | Target |
|---|---|
| Active clients | 15–25 (≈ $4.5–7.5k/mo recurring) |
| CPL | < $11 (target ~$8) |
| LTV:CAC | ≥ 3:1 |
| Coach time spent on non-coaching work | < 2 h/week |
