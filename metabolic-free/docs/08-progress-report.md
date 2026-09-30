# Progress report: Metabolic Flex / GFC Xtreme (Sept 28, 2026)

**Overall: foundation, website, platform, emails and video are built. Nothing is live yet.** Launch is blocked on
five connections that only the coach can make (see "Blocking items").

## 1. Build status

| Area | Status | What exists | Where |
|---|---|---|---|
| Strategy & offer | ✅ Done | Offer ladder, messaging, segments, "metabolic dysfunction free" positioning | `docs/02` |
| Client economics | ✅ Done | Calculator with the coach's real numbers: $299×3 → $199×6, free Lumen ($199 cost), 25 h/wk | `docs/03`, `tools/economics.py` |
| Compliance rules | ✅ Done | Health claims, GLP-1/LegitScript, HIPAA, TCPA/SMS, no scraping | `docs/04` |
| Brand | ✅ Done | GFC orange #F26B2A + black, logo shirt rule | `docs/06` |
| Website | ✅ Built, not hosted | Home + Metabolic Score quiz, The Science (13 studies), Program, GFC Lab tab, 30 spots → waitlist | `site/` |
| GFC Lab (Altrohealth) | 🟡 Built, waiting on link | Tab embeds Altrohealth inside the site; subdomain plan `lab.metabolicgfcxtremefit.com` | `site/lab.html`, `docs/07` |
| Client training platform | 🟡 Built, demo mode | Daily check-in (Lumen, protein, walk, weight, sleep), 12-week program, progress, coach roster with at-risk + week-6 renewal flags | `site/app/`, `data/platform.sql` |
| Contact list | ✅ Cleaned | 2,188 reachable people (2,049 emails, 1,796 mobiles, 0 SMS consent), 4 send waves | `data/private/` (never in git) |
| Launch emails | ✅ Written | 5 emails + resend + waitlist + SMS opt-in | `campaigns/launch-emails.md` |
| Ads copy | ✅ Written | Meta (1 ad set, 3 openings), Google (at ≥ $1k/mo), LinkedIn B2B | `campaigns/` |
| Hero video: assets | ✅ Done | Digital twin, approved master still in GFC shirt, voice clone | Higgsfield |
| Hero video: 7 clips | ✅ **All approved** | 3 openings + 4 main-message clips, 1080p, coach's voice | `campaigns/hero-video.md` |
| Hero video: final edit | ⏳ Next | 3 ads (~65–70 s), captions, black/orange end card, 9:16 / 4:5 / 1:1 | — |

## 2. The agents

Each agent is **designed** (job, KPI, rules, approval tiers). None runs automatically yet: each needs the
accounts/tools below connected. Until then, Claude has been doing their launch work directly.

| Agent | Job | Built so far | Needs to go live |
|---|---|---|---|
| **Content** | Posts, reels, captions from the message bank | Message bank, weekly calendar, hero video + 3 openings | Instagram/Facebook/TikTok accounts + scheduler |
| **Ads** | Launch, test, kill/scale ads | Ad copy, kill line ($16 CPL), compounding budget rule, 3 video openings | Meta Business Manager + Pixel, payment method |
| **Nurture** | Email/SMS until a call is booked | 5 launch emails, 14-day sequence, SMS scripts, opt-in flow | Email platform (GoHighLevel or similar), verified sending domain, A2P 10DLC number |
| **Booking** | Book, remind, rescue no-shows, pre-call brief | Reminder + no-show scripts | Booking calendar link |
| **Retention** | Keep clients engaged, flag churn, renewal at week 6 | Client app check-ins, coach roster flags | Supabase live (restore "GFCxtreme app") |
| **Outreach** | Employers, doctors, gyms (no scraping) | LinkedIn templates, employer pilot offer | Coach's LinkedIn / Sales Navigator |
| **Reporting** | Weekly 1-page report, scores every decision | Evidence log schema, weekly funnel view | Supabase live + ad/email accounts connected |

## 3. Blocking items (coach)
1. **Domain:** nameservers at lookup.icann.org (GoDaddy or Cloudflare) → publish `metabolicgfcxtremefit.com`.
2. **Altrohealth:** send the message in `docs/07` (subdomain, branding, embedding) → get the GFC Lab link.
3. **Supabase:** OK to restore the paused "GFCxtreme app" project → client logins go live.
4. **Email/CRM platform + booking calendar** → launch emails and booking can run.
5. **Meta Business Manager** → ads can run.

## 4. Spend so far (Higgsfield)
Started with ~2,587 credits; now ~1,290 left. Spent: twin training, 2 test stills, 1 test clip, 7 clips (~984), clip 4 redo (~204), voice tracks.

## 5. Next 3 steps
1. Final edit of the 3 ads (Claude).
2. Coach clears blocking items 1–4.
3. Wave 1 email (~512 people) goes out the day the site is live.
