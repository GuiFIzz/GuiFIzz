"""How many clients must you SELL to end year 1 holding 30?

A roster target is a net number. Churn means gross sales are always higher.
Nobody budgets for this, and it is usually where the ad spend dies.

gross new in month m = (growth that month) + (clients lost that month)
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
base = json.load(open(os.path.join(HERE, 'numbers.json')))
PRICE = base['price']
CONTRIB = PRICE - sum(v['cost'] for v in base['variable'])
ADS = next(f['cost'] for f in base['fixed_monthly'] if 'ad spend' in f['label'])
ROSTER = [round(r*30) for r in base['ramp_per_day']]

print(f"Target roster: {ROSTER[-1]} clients by month 12")
print(f"Price ${PRICE:,.0f}  contribution ${CONTRIB:,.2f}  ad budget ${ADS:,.0f}/mo\n")

print(f"{'churn':>7}{'gross sales yr1':>17}{'lost yr1':>10}{'avg new/mo':>12}"
      f"{'CAC $150':>11}{'CAC $300':>11}{'CAC $500':>11}")
print("-" * 79)
rows = {}
for churn in (0.03, 0.05, 0.08, 0.12, 0.20):
    gross = lost = 0.0
    held = 0.0
    for target in ROSTER:
        leavers = held * churn
        new = (target - held) + leavers
        gross += new; lost += leavers; held = target
    rows[churn] = gross
    print(f"{churn:>6.0%}{gross:>17.0f}{lost:>10.0f}{gross/12:>12.1f}"
          + "".join(f"{gross*c:>11,.0f}" for c in (150, 300, 500)))

print(f"\nYear 1 ad budget at ${ADS:,.0f}/mo = ${ADS*12:,.0f}.")
print("Any CAC column above that number is a hole you fund out of pocket.\n")

print("WHAT CHURN COSTS YOU IN YEAR 1 REVENUE")
print(f"{'churn':>7}{'client-months lost':>21}{'revenue lost':>15}{'contribution lost':>20}")
print("-" * 63)
for churn in (0.03, 0.05, 0.08, 0.12, 0.20):
    # months of billing forgone vs a zero-churn roster holding the same targets
    held = 0.0; cm_lost = 0.0
    for target in ROSTER:
        leavers = held * churn
        cm_lost += leavers      # each leaver stops billing from here on
        held = target
    print(f"{churn:>6.0%}{cm_lost:>21.0f}{cm_lost*PRICE:>15,.0f}{cm_lost*CONTRIB:>20,.0f}")

print(f"\nBreak-even is 21 clients. At 30, you carry {30-21} clients of cushion.")
for churn in (0.05, 0.08, 0.12, 0.20):
    months = (30 - 21) / (30 * churn) if churn else 99
    print(f"  At {churn:.0%} churn with zero new sales you fall below "
          f"break-even in {months:.1f} months.")
