# Warm-list launch: 2,188 contacts, in waves

**The real list (cleaned Sept 26, 2026):** 4,652 rows → **2,188 reachable people**
- **2,049 valid emails** (1,657 of them also have a mobile number)
- **139 phone-only** (no email)
- 138 rejected: 82 with no email or phone, 54 duplicates, 2 bad emails
- **0 with recorded SMS consent** (the export has no consent column)

**The capacity problem:** at the coach's 5% estimate, 2,188 people → **~109 clients, more than the 81-client
capacity.** Older, bigger lists usually convert at 1–3% (22–66 clients), but we shouldn't gamble on it. So
the list goes out in **4 waves of ~512**, one per week. Stop sending when the founding spots are full, and
everyone after that goes on a waitlist. Waves also protect email deliverability and let us fix the message after wave 1.

| Wave | Send | Cumulative clients at 1% / 3% / 5% |
|---|---|---|
| 1 | Week 1 | 5 / 15 / 26 |
| 2 | Week 2 | 10 / 31 / 51 |
| 3 | Week 3 (only if spots remain) | 15 / 46 / 77 |
| 4 | Week 4 (only if spots remain) | 20 / 61 / 102 → waitlist |

## What 30 founding clients means (the first milestone)

| | |
|---|---|
| Lumen cost (30 × $199) | $5,970, covered as each first payment clears |
| Month-1 coaching revenue | ~$8,970 |
| Guaranteed profit over the 3-month minimum | ~$21,000 |
| If half renew at $199 × 6 months | + ~$18,300 |
| Your time | ~9 h/week of your 25 (room for ~50 more clients) |
| Ad budget under the compounding rule | $500 + $100 × 30 = **$3,000 cap** (you approve going past $500) |

## Step 1: Clean the file (5 minutes, done by the system)

```
python3 tools/prepare_list.py path/to/your-file.csv
```
It splits the list into **email list** (plus `email_wave_1..4`), **SMS with recorded consent**, **phone without consent**, and **rejected**
(duplicates, bad emails). Files go to `data/private/`, which is **never committed**; this repo is public.
Then run the email list through a verifier (ZeroBounce / NeverBounce, ~$15–20 for 2,049) before sending. Old lists
bounce, and a high bounce rate can send all your email to spam.

## Step 2: Email everyone (the main blast)

From: your name, from your own authenticated domain (SPF/DKIM/DMARC). Every email includes an unsubscribe link and
the GFC Xtreme address. **Send in batches of ~150/day for the first 4 days** if the domain hasn't sent bulk email before.

| Day | Subject | Content | CTA |
|---|---|---|---|
| 0 | I built something for you, {{first_name}} | Personal note: why you built Metabolic Flex + **the hero video** | Watch → take the Metabolic Score |
| 3 | (to non-openers) Did you see this? | Same email, new subject | Same |
| 2 | Losing weight but losing muscle? | GLP-1 muscle problem + free Lumen ($249 value) | Take the score |
| 4 | 1 in 3 adults, and most don't know | Pre-diabetes stat (CDC) + what the score checks | Take the score |
| 6 | How it works (and what it costs) | Biweekly sessions, Lumen, medical partners, 3 months → $199 renewal | Book a call |
| 8 | Founding spots closing | "I'm taking 30 founding clients so I can give each one real attention." | Book a call |

After Day 8, anyone who took the quiz but didn't book moves into the regular 14-day nurture sequence
(`email-sequence.md`); everyone else goes to the monthly newsletter.

**Day 0 sample:**
> Subject: I built something for you, {{first_name}}
>
> Hi {{first_name}},
>
> For years I've watched the same thing happen: people lose weight and lose their muscle with it, their blood sugar
> creeps up without anyone noticing, and the plan falls apart the moment they're on their own.
>
> So I built **Metabolic Flex**. It uses every tool we have (GLP-1s and hormone therapy through licensed medical
> partners when they fit, training that protects your muscle, and a **free Lumen device** that reads your metabolism
> from your breath), with a coaching session with me every two weeks.
>
> Watch the 60-second video: {{video_link}}
> Then take the free 2-minute Metabolic Score: {{quiz_link}}
>
> I'm opening 30 founding spots first. If you're in, I'd love to have you.
>
> {{coach_name}}, GFC Xtreme
>
> *Educational, not medical advice. Unsubscribe anytime: {{unsubscribe}}. {{address}}*

## Step 3: Text messages (only where the law allows)

US texting law (TCPA, plus stricter state versions in e.g. Florida and Oklahoma) requires **prior written consent**
for marketing texts sent through a texting platform. Having someone's number isn't consent. Each group gets a different approach:

| Group | What we send |
|---|---|
| **SMS consent on record** | Platform texts: Day 0 (video + quiz link) and Day 7 (founding spots). Registered number (A2P 10DLC), "Reply STOP to opt out" |
| **Phone, no consent on record** (all 1,796 in this file) | No bulk texts. Many numbers look Southeast US (lots of bellsouth.net emails); if you're in **Florida**, its FTSA is stricter than federal law. Two safe options: (1) the emails invite them to opt in to texts; (2) **you** send short personal 1:1 texts from your own phone to people you actually know, typed individually. Check your state's rules first |
| **Email only** | Email only |

**Personal 1:1 text (for people you know):**
> Hey {{first_name}}, it's {{coach_name}} from GFC Xtreme. I just launched a metabolic coaching program and made a
> 60-sec video about it: {{video_link}}. Would love your honest opinion!

A platform text blast to numbers without consent can cost **$500–$1,500 per message** in damages. That's why this
step is split up.

## Step 4: Measure (Reporting agent)

Track opens, quiz completions, calls booked and enrollments for this list separately (tag `warm_list_launch`).
That turns the 5% guess into a real number for the calculator.
