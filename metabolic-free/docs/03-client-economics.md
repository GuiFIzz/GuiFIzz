# Client economics: what one client is worth

Same logic as valuing a cow on a farm: milk is only part of the value. You
also count what she eats, how long she produces, and the calves she brings.

| Farm | Coaching business |
|---|---|
| Milk per month | $299/mo (months 1–3), then $199/mo (6-month renewal) + telehealth margin |
| Feed cost | Software, payment fees, your time (Lumen membership: first 12 months included) |
| Productive years | 3-month minimum + 6-month renewal (if they renew) |
| Calves | Referrals |
| Purchase price | Cost to acquire (ads) |
| Equipment given to each cow | Free Lumen: $199 cost to GFC Xtreme ($249 value to the client) |

Run `python3 tools/economics.py` (override anything, e.g. `--renewal_rate 0.6`).

## Your numbers (Sept 2026)

| Input | Value | Source |
|---|---|---|
| Coaching | $299/mo, 3-month minimum | Coach |
| Renewal | 6 months at $199/mo | Coach |
| Lumen membership | First 12 months included (no cost during the program) | Coach / Lumen |
| Lumen | Free to client, $199 cost to GFC Xtreme | Coach |
| Telehealth | Altrohealth / OpenLoop (LegitScript) | Coach |
| Ad budget | $500/mo at launch | Coach |
| Coaching hours | 25 h/week | Coach |
| Renewal rate | **50% (estimate)** → 6 months average per client | Replace after the first 20 clients |
| Telehealth attach / margin | 30% × $60/mo (estimate) | Confirm your partner payout |
| Funnel rates | 12% book, 70% show, 30% close (industry estimate) | Replaced by real data in Week 6 |

## Output

| Metric | Value | What it means |
|---|---|---|
| Day-one cash after device | **~$85** ($299 − $199 − fees) | The device is paid off in month 1 |
| Guaranteed gross profit (3-month minimum) | **~$700** | Floor value of every client, after the Lumen |
| Each 6-month renewal adds | **~$1,220** | Worth more than the whole first phase |
| Lifetime gross profit (50% renew) | **~$1,310** | What one client is worth |
| With referrals | ~$1,700 | |
| Max cost to acquire a client (3:1) | **~$437** | |
| Max cost per lead | **~$11** | Ads agent kill line |
| Target cost per lead | ~$8 | Healthy running level |
| Coach capacity (25 h/wk, 30-min biweekly + 10 min admin) | **81 clients** | Solo ceiling |
| Revenue at capacity (half the roster on $199) | **~$21.6k/mo** | |
| New clients/month to stay full | ~13.5 | |

## The honest math on $500/month

$500 ÷ ~$8 per lead ≈ **65 leads/month ≈ 1–2 paid clients/month.**
Filling 81 spots that way would take years. So **$500 in ads is the test budget, not the growth engine.**
Early growth comes from free channels and compounding:

| Channel | Target clients/month by Month 3 | Cost |
|---|---|---|
| Meta ads ($500) | 1–2 | $500 |
| Organic content + "comment SCORE" DMs | 2–4 | Your weekly video |
| Referrals (1 free month per enrolled referral) | 1–3 | $299 per referral |
| Existing network / GFC Xtreme members / past clients | 2–4 | Free |
| B2B employer pilot (LinkedIn, local) | 0–10 (lumpy) | Time |

## Compounding rule: how the ad budget grows by itself

A client costs ~$310 to acquire (at ~$8 CPL, ~40 leads) plus $199 for the Lumen, about $510 in total. The 3-month
minimum brings in ~$870 after fees, so **every client is profitable by month 2 even if they quit at the minimum.**
That means the budget can safely grow with the client count:

```
monthly ad budget = $500 + $100 × active clients
   cap: the coach's monthly limit (default $3,000)
   only if: last 30 days' cost per enrolled client < $434 (max CAC)
```

| Active clients | Ad budget | Expected paid clients/month |
|---|---|---|
| 0 | $500 | ~1.6 |
| 10 | $1,500 | ~5 (Google turns on at ≥ $1,000) |
| 20 | $2,500 | ~8 |
| 25+ | $3,000 (cap) | ~10 |

The Reporting agent recalculates this every Monday. Increases up to the cap are a **Notify** action and anything
above the cap needs your approval.

## Levers, ranked by impact

1. **Renewal rate.** Each renewal is worth ~$1,220, more than the first 3 months. Going from 30% → 70% renewal
   raises LTV from ~$1,070 to ~$1,550. Present the renewal in the **week-6 session** with the client's own Lumen and
   progress data. The Retention agent prepares that progress summary for you.
2. **Close rate** on discovery calls (30% → 40% cuts CAC 25%).
3. **Referrals.** The cheapest client you'll ever get.
4. **Telehealth attach.** Medication clients need ongoing supervision, so they stay longer.
5. Cost per lead.

## Rule for the Ads agent

```
kill an ad set     if CPL > $16 (1.5 × $11) after 3 days AND ≥ $30 spent
scale              per the compounding rule above
optimize for       leads now; switch to booked calls (Schedule) once ≥ 50 bookings/week
```
