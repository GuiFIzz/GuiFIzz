# Email nurture: "7-Day Metabolic Reset" + booking push (14 days)

Trigger: quiz submitted with email consent. Exit: call booked. Personalize `{{segment_line}}` per segment.
From: Coach first name. Plain-text style (no heavy design). One link per email.

**Lead magnet delivery (the promise this whole sequence is named after):** the 7-Day Metabolic
Reset lives at `/7-day-reset` and is delivered twice — on screen the instant the quiz finishes,
and again as the first thing in the Day-0 email. Keep both. The Peptide Guide download
(`/api/guide-lead`) reuses the same `quiz_lead` tag and so enters this same sequence, which is
why Day 0 must stay neutral about how the person arrived — do not reintroduce
"thanks for taking the Metabolic Score" into Day 0.

**Send timing (corrected 2026-10-12).** The Systeme account timezone is now
**America/New_York**, so send times are set literally: every delayed step across all five
campaigns is pinned to **`09:00`**. Four steps stay immediate and must never be given a
`sendAtLocalTime` — nurture Day 0 (carries the lead magnet; delaying it breaks the promise),
the no-show "Sorry we missed you", and the post-call "Good talking with you".

*History worth keeping:* the account used to be Europe/Paris, which forced a 14:00 setting to
land at 8am ET and created a one-week DST hole every October. Changing the account timezone
removed both problems. **If the timezone is ever changed again, every `sendAtLocalTime` in all
five campaigns has to be re-checked** — a silent 6-hour shift is the failure mode.

Weekday skipping is off on the nurture (it would desynchronise the "Day N" labels from the
guide's days, and habit coaching reads fine at weekends). Consider turning it on for the
**Launch Sequence** only, since weekend sales emails convert poorly.

**Testing the funnel:** a contact who already carries `quiz_lead` cannot re-enter — `tag_added`
does not re-fire for a tag already present, and Systeme will not restart a campaign the
contact is already in. Always test with a fresh address (plus-addressing works).

| Day | Subject | Body (summary + CTA) |
|---|---|---|
| 0 | Your 7-Day Metabolic Reset is here | **Delivers the guide** (link to `/7-day-reset`) as the first thing in the email. What's in it, the honest "seven days won't transform you" framing, then Day-1 action: 10-min walk after the biggest meal. CTA: book a free call. |
| 1 | The muscle mistake | Why losing muscle slows metabolism; protein target = ~0.7–1 g/lb goal weight (tell them to check with their doctor if they have kidney disease). Action: protein at breakfast. |
| 2 | Why you crash at 3pm | Blood sugar swings + meal order (veg/protein first, carbs last). Action: try meal order today. |
| 3 | What actually makes the difference | Social proof. "Almost nobody quits because the plan was wrong — they quit because nobody noticed." Two consented testimonials (Melissa Rocher, Thomas M. — deliberately *not* the two used on Day 6). Action: name the habit that slipped first. CTA book. |
| 4 | Medication, peptides, hormones, apps: my honest take | Tools are bridges, not destinations. How we combine GLP-1s/peptides/HRT (via licensed providers) with habits. |
| 5 | Know when to eat | Lumen explained; **free device ($249 value)** for every client. CTA: see if you qualify / book a call. |
| 6 | 2 lifts that matter most after 40 | Strength basics, 2×/week. Action: do one session. |
| 7 | Your reset recap + next step | Recap the guide's **seven** days in order (must match `/7-day-reset` exactly), re-link the guide to keep, then: which stuck without effort, which needed willpower? Strong CTA to book. |
| 9 | "Is this for me?" | FAQ: cost range, time per week, remote, what if I'm on medication. CTA book. |
| 11 | What happens on the call | 30 min, no pressure, what they'll leave with. CTA book. |
| 14 | Closing the door (for now) | Last push; then moves to monthly newsletter. |

**Day 6, full copy:**
> Subject: 2 lifts that matter most after 40
>
> Hi {{first_name}},
>
> After 40, you lose muscle a little faster every year if you don't push against it — but you don't need to live in
> the gym to stop that.
>
> Two lifts do most of the work: a squat pattern (protects your legs and hips) and a hinge or row pattern (protects
> your back and posture). Twice a week, 30-40 minutes, is enough to hold the line.
>
> Here's what that's looked like for two of our members:
>
> *"I have been into fitness all my life. Today, at 46, I find myself in great shape... after working with Gui Cury
> for the past year, I can truly say, I found MY PERSONAL TRAINER."* — Arlyn Haas, 46
>
> *"At 45 my body changed and I wanted to get back in shape. I started working with Gui and — wow — I saw a total
> difference. Truly excellent."* — Zulema Lopez, 45
>
> Today's action: if you have a strength session scheduled this week, do it. If you don't, that's exactly what we
> build together.
>
> Book a free call and we'll design yours: {{booking_link}}
>
> {{coach_name}}

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
> If you'd like me to look at your answers with you and map your first 30 days, grab a free 30-minute call here:
> {{booking_link}}
>
> In your corner,
> {{coach_name}}
>
> *This is educational and not medical advice. Talk to your doctor before changing medication.*

---

# Long-Term Nurture (campaign 1210493) — the recapture net

Built 2026-10-12. Catches everyone who finished another sequence without converting, so
nobody dead-ends into silence. **Costs zero tags** — the whole chain runs on
`campaign_completed` triggers, which matters because all 10 tag slots are spent.

## The chain

```
quiz_lead ──► Nurture (14d) ──────────────┐
                                           ├──► LONG-TERM NURTURE (~100d)
call_attended ──► Attended F/U (2d) ──────┘

launch_list ──► Launch Sequence (8d) ──► Nurture (14d) ──► Long-Term Nurture
```

Rules: `2458742` (Nurture done → LT), `2458743` (Attended done → LT),
`2458744` (Launch done → Nurture). Existing `2454042` (No-Show done → Nurture).

Total runway for an imported contact: **8 + 14 + ~100 = ~122 days** of automatic contact,
versus 8 days before.

## The five emails

| # | Gap | Subject | Job |
|---|---|---|---|
| 1 | +14d | The part nobody posts about | Reframe to the long game. Twelve weeks is a photo. Arlyn Haas (1-year client). No ask. |
| 2 | +14d | A 30-second test you can do right now | Pure value, zero pitch: the 30-second chair stand. Rebuilds goodwill after a sales sequence. |
| 3 | +21d | What's changed since we last spoke | Real reason to re-open: human-filmed exercise library, free Lumen, GFC Lab live. First CTA of the sequence. |
| 4 | +21d | Was it the money or the timing? | The objection email. Asks for a **one-word reply**, not a booking — surfaces the real blocker and feeds product decisions. |
| 5 | +30d | Still here when you're ready | Soft re-offer with no deadline, plus an explicit invitation to unsubscribe. Protects list quality. |

**Note on testimonials:** all six consented quotes are now in use across the sequences
(Arlyn, Zulema, Melissa, Thomas, Rodrigo, Joseph). LT1 reuses Arlyn deliberately — the
"after a year with Gui" line is the only one that supports a long-game message. New
testimonials are the constraint on writing more social proof.

## Still outstanding before launch

- [ ] `client_signed_up` tag + rule to unsubscribe from **all four** campaigns (1203488,
      1203500, 1206790, 1208671, 1210493) — needs a tag slot freed
- [ ] `launch_list` tag + rule → subscribe to 1203500 — needs a tag slot freed
- [ ] Optional: `skipWeekdays` on the Launch Sequence so no sales email lands on a weekend
