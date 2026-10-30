import json, subprocess, copy, sys
base = json.load(open('founder/numbers.json'))
TOOL = '.claude/skills/founder-cfo/unit_economics.py'
SCRATCH = '/tmp/claude-0/-home-user-GuiFIzz/d81d7758-6d6d-5405-bb62-6483f433dc06/scratchpad/v.json'

def run(d):
    json.dump(d, open(SCRATCH,'w'))
    out = subprocess.run([sys.executable, TOOL, SCRATCH, '--json'], capture_output=True, text=True)
    return json.loads(out.stdout)

def coachhrs(d, hours, rate=22.0):
    d = copy.deepcopy(d)
    d['variable'][0] = {"label": f"Coach time ({hours}h @ ${rate}/h)", "cost": round(hours*rate,2)}
    return d

rows = []
for label, d in [
    ("BASELINE $149 / 2.5h coach time", base),
    ("price $199", {**copy.deepcopy(base), 'price':199.0}),
    ("price $249", {**copy.deepcopy(base), 'price':249.0}),
    ("price $299", {**copy.deepcopy(base), 'price':299.0}),
    ("coach time 1.5h (group model)", coachhrs(base,1.5)),
    ("coach time 1.0h (app-led)", coachhrs(base,1.0)),
    ("coach time 0.5h (app + async)", coachhrs(base,0.5)),
    ("$199 + 1.5h coach time", {**coachhrs(base,1.5), 'price':199.0}),
    ("$249 + 1.5h coach time", {**coachhrs(base,1.5), 'price':249.0}),
    ("$99 app-only, 0.25h", {**coachhrs(base,0.25), 'price':99.0}),
]:
    r = run(d)
    be_day = r['breakeven_per_day']
    rows.append((label, r['contribution'], r['margin_at_plan'], be_day*30, r['year1_profit'], r['cash_needed']))

print(f"{'scenario':<34}{'contrib':>9}{'margin@plan':>12}{'B/E clients':>13}{'yr1 profit':>13}{'cash need':>12}")
print("-"*93)
for l,c,m,be,y,cash in rows:
    print(f"{l:<34}{c:>9.2f}{m*100:>11.0f}%{be:>13.0f}{y:>13,.0f}{cash:>12,.0f}")
print()
print(f"Plan volume = {base['plan_per_day']*30:.0f} clients/mo   Capacity = {base['capacity_per_day']*30:.0f} clients/mo")
