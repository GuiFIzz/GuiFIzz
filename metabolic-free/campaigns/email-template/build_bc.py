from parts import *
CAL="https://cal.com/gfcxtreme-fitness-nmylwf/30min"

B = (head("Book free call", CAL)
 + title("Keep your muscle", "Lose weight fast and a big share of what comes off can be the tissue that runs your metabolism.")
 + hero_side("muscle-600.jpg", CAL, "Hi {first_name} &mdash; muscle burns energy all day, even at rest. Lose it and your metabolism slows, so the next pound gets <strong>harder</strong> to lose, not easier.")
 + para("The fix is simple, not easy: <strong>protein at every meal</strong>, and resistance training that signals your body to hold on to what it has. A rough target is 0.7&ndash;1g of protein per pound of your goal weight.")
 + cta("Keep your muscle &mdash; book free call &rarr;", CAL)
 + callout("Today's action", "Make protein the thing you plan your next meal around &mdash; and make tomorrow's breakfast the one you never skip it at again.")
 + sign("Educational content, not medical advice. Check with your doctor first if you have kidney disease.")
 + labs() + foot())

C = (head("Book free call", CAL)
 + title("Ninety days from now", "It arrives whether you start or not. The only question is what you did with it.")
 + hero("result-90-days-30-lb-anon-600.jpg", CAL, "A GFC Xtreme coaching client, 90 days. An individual result &mdash; results are not typical and vary from person to person.")
 + para("Hi {first_name} &mdash; most people who find their way here don't need more willpower. They need a system, the right tools, and <strong>someone checking in every two weeks.</strong>")
 + para("That's the whole job. Not clever exercises &mdash; noticing when you drift, and adjusting before it costs you a month.")
 + cta("Start your 90 days &mdash; book free call &rarr;", CAL)
 + sign()
 + labs() + foot())

open("test-B.html","w").write(B); open("test-C.html","w").write(C)
b=B.replace("{first_name}","Gui"); c=C.replace("{first_name}","Gui")
open("test-BC.html","w").write(f'''<!doctype html><meta charset="utf-8"><title>B and C, as a client sees them</title>
<body style="margin:0;background:#1c1c1e;font-family:-apple-system,Helvetica,Arial;">
<div style="max-width:900px;margin:0 auto;padding:18px 12px 40px;">
<p style="color:#f4f4f5;font:700 17px/1.3 Helvetica;margin:0 0 4px;">The two test emails, at iPhone width</p>
<p style="color:#a1a1aa;font:400 13px/1.5 Helvetica;margin:0 0 20px;">Images load from your live domain, so this is what a client's mail app would fetch.</p>
<div style="display:flex;gap:22px;flex-wrap:wrap;justify-content:center;">
<div><p style="color:#F26B2A;font:800 12px/1 Helvetica;letter-spacing:.1em;text-transform:uppercase;margin:0 0 8px;">B &mdash; teaching</p>
<div style="width:390px;height:820px;overflow:auto;border:10px solid #3a3a3c;border-radius:30px;background:#fff;">{b}</div></div>
<div><p style="color:#F26B2A;font:800 12px/1 Helvetica;letter-spacing:.1em;text-transform:uppercase;margin:0 0 8px;">C &mdash; proof</p>
<div style="width:390px;height:820px;overflow:auto;border:10px solid #3a3a3c;border-radius:30px;background:#fff;">{c}</div></div>
</div></div></body>''')
print("built")
