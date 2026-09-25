# Client economics: what one client is worth

Same logic as valuing a cow on a farm: milk is only part of the value. You
also count what she eats, how long she produces, and the calves she brings.
Here:

| Farm | Coaching business |
|---|---|
| Milk per month | Coaching fee + telehealth margin per month |
| Feed cost | Lumen device, software, payment fees, your time |
| Productive years | Months retained |
| Calves | Referrals |
| Purchase price | Cost to acquire (ads + tools) |

Run `python3 tools/economics.py` (all inputs can be overridden, e.g.
`--price_per_month 397 --avg_months_retained 9`).

## Default output (placeholder numbers)

| Metric | Value | What it means |
|---|---|---|
| Lifetime gross profit per client | **~$1,840** (after Lumen) | What one client is worth |
| With referrals | ~$2,390 | Worth building a referral engine |
| Lumen payback | ~0.8 months | The free device is affordable **if** the client stays; hence the 6-month commitment |
| Lead → client | 2.5% (1 in 40) | 12% book × 70% show × 30% close |
| **Max cost to acquire a client** | **~$612** | At a 3:1 LTV:CAC safety ratio |
| **Max cost per lead** | **~$15** | The Ads agent's kill line |
| Coach capacity (20 h/wk, 30-min biweekly + 10 min admin) | **65 clients** | Your ceiling as a solo coach |
| Revenue at capacity | ~$20.5k/mo | |
| Intake to stay full | ~9 new clients/mo, ~370 leads/mo | |
| Ad budget to stay full | ~$5.7k/mo at max CPL | Lower CPL means more profit |

## Levers, ranked by impact

1. **Retention** (months retained). Going from 7 to 10 months raises LTV ~45% with no extra ad spend. Lumen
   adherence nudges + biweekly accountability are retention tools.
2. **Close rate** on discovery calls. A 30% → 40% close rate cuts CAC by 25%.
3. **Group coaching tier.** Breaks the 65-client ceiling.
4. **Telehealth attach.** GLP-1/hormone clients stay longer (medication supervision requires ongoing contact).
5. CPL. Matters, but it's the lever everyone over-focuses on.

## Rule for the Ads agent

```
kill an ad set     if CPL > 1.5 × max_cpl after 3 days AND ≥ $50 spent
scale an ad set    if cost per booked call < max_cac × show × close  for 3 days → +20% budget
optimize for       booked calls (Schedule event) once ≥ 50/week; until then, optimize for leads
```
