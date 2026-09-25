# Email nurture: "7-Day Metabolic Reset" + booking push (14 days)

Trigger: quiz submitted with email consent. Exit: call booked. Personalize `{{segment_line}}` per segment.
From: Coach first name. Plain-text style (no heavy design). One link per email.

| Day | Subject | Body (summary + CTA) |
|---|---|---|
| 0 | Your Metabolic Score: {{score}}/100 | Score explained in plain words, top 3 levers for their segment. Day-1 action: 10-min walk after the biggest meal. CTA: book a free call. |
| 1 | The muscle mistake | Why losing muscle slows metabolism; protein target = ~0.7–1 g/lb goal weight (tell them to check with their doctor if they have kidney disease). Action: protein at breakfast. |
| 2 | Why you crash at 3pm | Blood sugar swings + meal order (veg/protein first, carbs last). Action: try meal order today. |
| 3 | A story: {{client_story}} | Consented client story from the same segment. CTA: "Want the same plan? Book 15 min." |
| 4 | Medication, hormones, apps: my honest take | Tools are bridges, not destinations. How we combine GLP-1s/HRT (via licensed providers) with habits. |
| 5 | Know when to eat | Lumen explained; the free-device offer + commitment. CTA: see if you qualify. |
| 6 | 2 lifts that matter most after 40 | Strength basics, 2×/week. Action: do one session. |
| 7 | Your reset recap + next step | Recap 6 habits. Strong CTA to book. |
| 9 | "Is this for me?" | FAQ: cost range, time per week, remote, what if I'm on medication. CTA book. |
| 11 | What happens on the call | 15 min, no pressure, what they'll leave with. CTA book. |
| 14 | Closing the door (for now) | Last push; then moves to monthly newsletter. |

**Sample, Day 0:**
> Subject: Your Metabolic Score: {{score}}/100
>
> Hi {{first_name}},
>
> Thanks for taking the Metabolic Score. Yours is **{{score}}**. {{segment_line}}
>
> Here's the truth: most people with a score like yours don't need more willpower. They need a system, the right
> tools, and someone checking in every two weeks.
>
> Your first move (today): a 10-minute walk after your biggest meal. It's one of the simplest ways to blunt a blood
> sugar spike.
>
> If you'd like me to look at your answers with you and map your first 30 days, grab a free 15-minute call here:
> {{booking_link}}
>
> In your corner,
> {{coach_name}}
>
> *This is educational and not medical advice. Talk to your doctor before changing medication.*
