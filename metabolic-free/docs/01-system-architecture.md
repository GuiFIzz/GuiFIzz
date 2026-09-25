# System architecture

## 1. Funnel stages and the one number each stage owns

| Stage | Definition | Owner agent | Stage KPI | Starting target |
|---|---|---|---|---|
| Attention | Someone sees content or an ad | Content, Ads | Cost per 1,000 impressions, hook rate (3-sec views / impressions) | hook rate > 25% |
| Capture | Completes the Metabolic Score quiz and leaves email + phone | Ads, Landing | Cost per lead (CPL), quiz completion rate | CPL < $15, completion > 45% |
| Nurture | Lead gets education + proof until ready | Nurture | Lead → booked call % | > 12% in 14 days |
| Convert | Discovery call (15–20 min) | Booking (+ you, or a closer later) | Show rate, close rate | show > 70%, close > 30% |
| Coach | Biweekly session, Lumen data review | **You** | Adherence (sessions attended, Lumen logs/week) | > 85% sessions kept |
| Retain | Stays, gets results, refers | Retention | Monthly churn, referrals/client | churn < 8%/mo |

**Master metric: cost per enrolled client (CAC) vs. client value (LTV).**
Everything else is a diagnostic for that ratio. Target LTV:CAC ≥ 3:1. See `03-client-economics.md`.

## 2. Data flow

```
 Ad / post ──UTM──► Landing + quiz ──► CRM contact
                                       ├─ score (0–100) + segment (weight | pre-diabetic | diabetic | hormones | performance)
                                       ├─ consent flags (email, SMS; captured separately, with timestamps)
                                       └─ source (utm_source / campaign / ad id)
                                              │
                           ┌──────────────────┼──────────────────┐
                           ▼                  ▼                  ▼
                     Nurture sequence    Retargeting audience  Booking link
                           │                                     │
                           └─────────► Discovery call ◄──────────┘
                                             │
                                  enrolled? ─┴─ yes ─► onboarding + Lumen shipped + session cadence
                                             └─ no ──► long-term nurture (monthly), re-scored at 90 days
```

**Key rule:** the ad id travels with the lead all the way to "enrolled" and
"month 6 retained". That lets the Ads agent optimize for **clients**, not for
cheap leads. (Send `Lead`, `Schedule`, and `Purchase` events back to Meta via the
Conversions API and to Google via offline conversion import. Send only event
names and hashed contact data, **never health answers**; see guardrails.)

## 3. Tool stack (recommended, swappable)

| Job | Recommended | Why | Alternative |
|---|---|---|---|
| CRM + email + SMS + booking + pipeline | **GoHighLevel** (or HubSpot Starter) | One place for everything; built for coaching funnels | Kajabi, ActiveCampaign + Calendly |
| Landing page + quiz | `site/index.html` here, hosted on Netlify/Vercel/WordPress | We own the code and the tracking | ScoreApp, Typeform |
| Database + evidence log | Supabase (Postgres), schema in `data/schema.sql` | Agents read and write here; the reporting source of truth | Airtable |
| Ads | Meta Ads Manager, Google Ads | Main paid channels | TikTok Ads, YouTube |
| Creative | Phone video (you) + Canva + AI image/video for b-roll | Real face + fast volume | CapCut |
| Social scheduling | Meta Business Suite / Buffer / GHL Social Planner | Auto-posting | Later, Metricool |
| Reporting | Supermetrics → dashboard, or GHL reports | Weekly 1-page report | Looker Studio |
| Telehealth (Rx) | Partner platform with licensed clinicians | Needed for GLP-1s and hormones | Your own licensed clinician |
| HIPAA storage | A platform that signs a BAA with you | Required for health data when you're a covered entity | — |

## 4. The decision layer (how agents stay safe and improve)

Every agent action goes through the same four steps:

```
 1. PROPOSE   agent picks an action + states the expected outcome
              e.g. "Pause ad set B: CPL $31 over 3 days vs $14 target; expect blended CPL -18%"
 2. VALIDATE  policy check (code, not vibes):
              - budget within daily/weekly caps?
              - copy passes claim filter (04-compliance-guardrails.md)?
              - SMS has consent + quiet hours respected?
              - action type allowed without human approval?
 3. EXECUTE   only if validated; otherwise queue for the coach's approval
 4. EVIDENCE  write to `decision_log`: what, why, expected, then 7/14/30-day actual
```

**Approval tiers**

| Tier | Examples | Who approves |
|---|---|---|
| Auto | Post scheduled content, pause an ad under its kill rule, send a sequence email, book or reschedule | System |
| Notify | Increase an ad set budget ≤ 20% within the monthly cap, launch a new variant of an approved angle | System, listed in weekly report |
| Approve | New ad angle, new health claim, new offer or price, spend above cap, anything mentioning medication | **Coach** |

**Self-improvement loop (weekly):** the Reporting agent compares expected and
actual outcomes in `decision_log`, promotes rules that worked (e.g. "hooks
about energy crashes beat weight-loss hooks 2:1 for women 40–55"), and retires
those that didn't. Those rules become the inputs for next week's Content and
Ads decisions. An extra model call or automation has to earn its place: if it
doesn't move a stage KPI, it gets cut.
