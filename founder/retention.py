"""Churn + CAC layer for a client-month business.

founder-cfo's unit_economics.py models a TRANSACTION business: each sale is
independent. A coaching retainer is not that. Two numbers it has no input for
decide the whole business:

  churn  - the share of clients who leave each month
  CAC    - what it costs to acquire one client

Together they set the real ceiling. A roster is a leaky bucket: at steady
state you hold (new clients per month / churn) clients, no matter how many
hours you have free. This models that.

Run:  python3 founder/retention.py
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
base = json.load(open(os.path.join(HERE, 'numbers.json')))

PRICE = base['price']
VARIABLE = sum(v['cost'] for v in base['variable'])
CONTRIB = PRICE - VARIABLE
FIXED = sum(f['cost'] for f in base['fixed_monthly'])
AD_SPEND = next(f['cost'] for f in base['fixed_monthly'] if 'ad spend' in f['label'])

def ltv(churn):
    """Lifetime value: contribution x expected months retained."""
    return CONTRIB / churn

def steady_state(new_per_month, churn):
    """The roster size where joiners and leavers cancel out."""
    return new_per_month / churn

print(f"Price ${PRICE:,.0f}/client-month   contribution ${CONTRIB:,.2f} "
      f"({CONTRIB/PRICE:.0%})   fixed ${FIXED:,.0f}/mo\n")

print("LIFETIME VALUE — how long a client stays is worth more than what they pay")
print(f"{'monthly churn':>15}{'avg months':>13}{'LTV':>12}{'max CAC @ 3:1':>16}")
print("-" * 56)
for churn in (0.03, 0.05, 0.08, 0.12, 0.20):
    v = ltv(churn)
    print(f"{churn:>14.0%}{1/churn:>13.1f}{v:>12,.0f}{v/3:>16,.0f}")

print("\n\nTHE LEAKY BUCKET — the roster you can actually hold")
print("Steady-state clients = new clients per month / churn rate")
print(f"{'new/mo':>8}" + "".join(f"{c:>12.0%}" for c in (0.03,0.05,0.08,0.12,0.20)))
print("-" * 68)
for new in (2, 4, 6, 8, 12):
    row = "".join(f"{steady_state(new,c):>12.0f}" for c in (0.03,0.05,0.08,0.12,0.20))
    print(f"{new:>8}{row}")

print("\n\nWHAT STANDING STILL COSTS — replacing churn before you grow at all")
print(f"{'roster':>8}{'churn':>8}{'lost/mo':>9}{'CAC $150':>11}{'CAC $300':>11}"
      f"{'CAC $500':>11}{'vs ad budget':>16}")
print("-" * 72)
for roster in (40, 80, 108):
    for churn in (0.05, 0.08, 0.12):
        lost = roster * churn
        costs = [lost * c for c in (150, 300, 500)]
        verdict = "OK" if costs[1] <= AD_SPEND else f"over by ${costs[1]-AD_SPEND:,.0f}"
        print(f"{roster:>8}{churn:>8.0%}{lost:>9.1f}"
              + "".join(f"{c:>11,.0f}" for c in costs) + f"{verdict:>16}")
    print()

print(f"Ad budget in numbers.json: ${AD_SPEND:,.0f}/mo. 'vs ad budget' tests the")
print("$300 CAC column — what it costs to merely REPLACE churn, before growth.")
