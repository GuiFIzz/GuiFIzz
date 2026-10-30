"""What makes a 30-client year 1 work?

Break-even is 21 clients. A ramp that ends at 30 crosses it in month 7, so
most of year 1 is spent below the line. These are the levers that change it.
"""
import json, subprocess, copy, sys, os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
TOOL = os.path.join(ROOT, '.claude/skills/founder-cfo/unit_economics.py')
SCRATCH = os.path.join(HERE, '.scn.tmp.json')
base = json.load(open(os.path.join(HERE, 'numbers.json')))

def run(d):
    json.dump(d, open(SCRATCH, 'w'))
    return json.loads(subprocess.run([sys.executable, TOOL, SCRATCH, '--json'],
                                     capture_output=True, text=True).stdout)

def build(price=None, roster=None, draw=None, ads=None):
    d = copy.deepcopy(base)
    if price:
        d['price'] = price
        d['variable'][1] = {"label": "Payment processing (2.9% + $0.30)",
                            "cost": round(price*0.029 + 0.30, 2)}
    if roster:
        d['plan_per_day'] = round(roster[-1]/30, 3)
        d['ramp_per_day'] = [round(r/30, 3) for r in roster]
    if draw is not None:
        d['fixed_monthly'][0] = {"label": "Founder draw", "cost": draw}
    if ads is not None:
        d['fixed_monthly'][3] = {"label": "Always-on ad spend", "cost": ads}
    return d

SLOW = [3, 6, 9, 12, 15, 18, 21, 23, 25, 27, 29, 30]      # as planned
FAST = [5, 10, 15, 19, 22, 25, 27, 28, 29, 30, 30, 30]    # 30 by month 10
LEAN = [4, 8, 12, 16, 20, 24, 27, 29, 30, 30, 30, 30]     # 30 by month 9

scenarios = [
    ("AS PLANNED  $300, 30 by mo 12",        build()),
    ("price $400",                            build(price=400)),
    ("price $500",                            build(price=500)),
    ("faster ramp (30 by mo 10)",             build(roster=FAST)),
    ("fastest ramp (30 by mo 9)",             build(roster=LEAN)),
    ("founder draw $2,500 in year 1",         build(draw=2500)),
    ("$400 + faster ramp",                    build(price=400, roster=FAST)),
    ("$400 + draw $2,500",                    build(price=400, draw=2500)),
    ("$500 + faster ramp",                    build(price=500, roster=FAST)),
]

print(f"{'scenario':<34}{'contrib':>9}{'B/E':>6}{'margin':>8}"
      f"{'yr1 profit':>13}{'cash need':>12}{'payback':>9}")
print("-" * 91)
for label, d in scenarios:
    r = run(d)
    pb = r['payback_month']
    print(f"{label:<34}{r['contribution']:>9.0f}{r['breakeven_per_day']*30:>6.0f}"
          f"{r['margin_at_plan']*100:>7.0f}%{r['year1_profit']:>13,.0f}"
          f"{r['cash_needed']:>12,.0f}{(f'mo {pb}' if pb else '>12 mo'):>9}")
os.remove(SCRATCH)

print("\nB/E = clients needed to break even. Plan ends at 30 in every row.")
print("'cash need' = the deepest the bank account goes before it climbs back.")
