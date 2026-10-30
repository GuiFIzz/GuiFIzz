"""Capacity-bound model for a founder-delivered 1:1 coaching agency.

The constraint is not cash, it is founder hours. This sweeps hours-per-client
against price and reports the ceiling: the most the business can earn before
the founder runs out of week.
"""
import json, subprocess, copy, sys, os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
TOOL = os.path.join(ROOT, '.claude/skills/founder-cfo/unit_economics.py')
SCRATCH = os.path.join(HERE, '.sweep.tmp.json')
base = json.load(open(os.path.join(HERE, 'numbers.json')))

DELIVERY_HOURS_PER_WEEK = 25   # hours left for coaching after sales + admin
WEEKS = 4.33

def run(d):
    json.dump(d, open(SCRATCH, 'w'))
    out = subprocess.run([sys.executable, TOOL, SCRATCH, '--json'],
                         capture_output=True, text=True)
    return json.loads(out.stdout)

def variant(price, hours_per_client):
    """Capacity and plan both follow from founder hours, not from a wish."""
    d = copy.deepcopy(base)
    d['price'] = price
    d['variable'][1] = {"label": "Payment processing (2.9% + $0.30)",
                        "cost": round(price * 0.029 + 0.30, 2)}
    ceiling = (DELIVERY_HOURS_PER_WEEK * WEEKS) / hours_per_client
    d['capacity_per_day'] = round(ceiling / 30, 3)
    d['plan_per_day'] = round(ceiling * 0.75 / 30, 3)   # plan at 75% of full
    d['ramp_per_day'] = [round(d['plan_per_day'] * f / 30 * 30, 3)
                         for f in (.1,.2,.32,.45,.57,.68,.76,.83,.88,.93,.97,1.0)]
    return d, ceiling

print(f"Founder delivery capacity: {DELIVERY_HOURS_PER_WEEK} h/week = "
      f"{DELIVERY_HOURS_PER_WEEK*WEEKS:.0f} h/month\n")
print(f"{'price':>7}{'h/client':>10}{'max clients':>13}{'plan':>7}"
      f"{'contrib':>10}{'B/E':>6}{'yr1 profit':>13}{'at full capacity':>18}")
print("-" * 84)
for hours in (1.0, 0.75, 0.5, 0.25):
    for price in (300, 400, 500):
        d, ceiling = variant(price, hours)
        r = run(d)
        full = (r['contribution'] * ceiling - r['fixed_monthly']) * 12
        print(f"{price:>7}{hours:>10}{ceiling:>13.0f}{d['plan_per_day']*30:>7.0f}"
              f"{r['contribution']:>10.2f}{r['breakeven_per_day']*30:>6.0f}"
              f"{r['year1_profit']:>13,.0f}{full:>18,.0f}")
    print()
os.remove(SCRATCH)
print("'at full capacity' = annual profit ON TOP of the $4,000/mo founder draw,")
print("if every founder hour is sold. That is the ceiling of this model.")
