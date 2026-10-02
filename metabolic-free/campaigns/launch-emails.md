# Launch emails: ready to paste

For the warm list (`email_wave_1..4.csv`), one wave per week. Merge fields: `{{first_name}}`,
`{{quiz_link}}` = site home + `?utm_source=email&utm_campaign=launch_wave{{N}}`, `{{video_link}}`,
`{{program_link}}` = program.html, `{{booking_link}}`, `{{spots_left}}`.
Every email ends with the footer below. Sender: **Coach's name, GFC Xtreme**, sent from the gym's own domain.

**Footer (all emails):**
> You're getting this because you've been part of the GFC Xtreme community. Not interested?
> [Unsubscribe]({{unsubscribe}}), no hard feelings. GFC Xtreme Fitness, {{address}}.
> *Educational content, not medical advice.*

**Want texts too?** Add this line above the footer in emails 1, 3 and 5. It's how phone contacts opt in to SMS:
> 📱 Want reminders and tips by text? [Tap here to opt in]({{sms_optin_link}}). Msg & data rates may apply; reply STOP anytime.

---

## Email 1 · Day 0 · the announcement
**Subject:** I built something for you, {{first_name}}
**Preview:** Every tool we have, plus a coach in your corner

> Hi {{first_name}},
>
> For years I've watched the same thing happen. People lose weight and lose their muscle with it. Their blood sugar
> creeps up without anyone noticing. And the plan falls apart the moment they're on their own.
>
> So I built **Metabolic Flex**. It uses every tool we have:
> - **Training that protects your muscle**, in an app built for you
> - A **free Lumen device** ($249 value) that shows from your breath whether you're burning fat or carbs
> - **GFC Lab:** licensed clinicians for GLP-1 medications, peptide therapy and hormone therapy, when they're right for you
> - **A 1:1 session with me every two weeks.** Discipline, accountability, consistency.
>
> Watch the 60-second video: {{video_link}}
>
> Then take the free 2-minute Metabolic Score to see where you stand: {{quiz_link}}
>
> I'm opening **30 founding spots** so every person gets my real attention. After that, it's a waitlist.
>
> *"From the first phone conversation I had with Gui I knew I wanted to work with him — he was so enthusiastic! Best decision I've made in a long time!"* — Melissa Rocher
>
> In your corner,
> {{coach_name}}

## Email 1b · Day 3 · resend to non-openers only
**Subject:** Did you see this, {{first_name}}?
Same body as Email 1.

## Email 2 · Day 2 · the muscle problem
**Subject:** Losing weight but losing muscle?
**Preview:** Why the scale can lie to you

> {{first_name}},
>
> Here's something most weight-loss plans ignore: when you lose weight fast, especially on GLP-1 medications, **a big
> share of it can be muscle.** In some studies it's up to around 40%.
>
> Why that matters: muscle is what burns energy all day. Lose it, and your metabolism slows down. Stop the medication,
> and the weight comes back, often as fat.
>
> The fix isn't complicated: **lift 3 times a week, eat protein at every meal, and walk after your biggest meal.**
> It's the base of everything we do in Metabolic Flex, and your Lumen tells us each morning whether it's working.
>
> Not sure where you stand? The Metabolic Score takes 2 minutes: {{quiz_link}}
>
> *"Gui is exceptional. Clearly educated on physical health and nutrition. I've been training with Gui for 4 weeks and am very pleased with my results."* — Thomas M.
>
> {{coach_name}}

## Email 3 · Day 4 · the hidden problem
**Subject:** 1 in 3 adults, and most don't know
**Preview:** The quiet one nobody tells you about

> {{first_name}},
>
> According to the CDC, **about 1 in 3 American adults has pre-diabetes, and more than 8 in 10 of them don't know it.**
>
> It usually doesn't hurt. It shows up as the 3pm crash, cravings, belly weight that won't move, and sleep that doesn't
> refresh you.
>
> The good news: pre-diabetes is the best window to act. Structured lifestyle programs have been shown to cut the
> risk of progressing substantially.
>
> The Metabolic Score checks the signs in 2 minutes. It's not a diagnosis, but it tells you whether it's time to
> look closer (and GFC Lab can order the labs if you want real numbers): {{quiz_link}}
>
> {{coach_name}}

## Email 4 · Day 6 · how it works and what it costs
**Subject:** How Metabolic Flex works (and what it costs)
**Preview:** No surprises

> {{first_name}}, here's the whole thing, straight:
>
> **Phase 1 · Foundation: $299/month, 3-month minimum**
> - 1:1 session with me every two weeks
> - Your training program and daily check-ins in the Metabolic Flex app
> - **Free Lumen device** ($249 value) + 12 months of Lumen membership
> - Access to GFC Lab (medical visits and medication are billed separately by our licensed partner)
>
> **Phase 2 · Momentum: $199/month for 6 months** after your first 3, if you want to keep going.
>
> Details and FAQ: {{program_link}}
>
> *"Gui is a great guy, great trainer and works on helping you reach your specific goals. I highly recommend him."* — Rodrigo Bravo
>
> If you're ready, grab a free 30-minute call and we'll map your first 30 days: {{booking_link}}
>
> **{{spots_left}} founding spots left.**
>
> {{coach_name}}

## Email 5 · Day 8 · last call
**Subject:** Founding spots are almost gone
**Preview:** Then it's a waitlist

> {{first_name}},
>
> Quick one: I'm keeping Metabolic Flex to 30 founding clients so I can coach each of you properly, and
> **{{spots_left}} spots are left.**
>
> If you've been thinking about it, this is the moment. Take the score or book directly:
> - Metabolic Score (2 min): {{quiz_link}}
> - Free 30-min call: {{booking_link}}
>
> *"I am very impressed by the professionalism and knowledge that Gui has shown from the very first training session. Gui is also very punctual and focused on results."* — Joseph Savarese
>
> If the timing isn't right, no problem. You'll still get my tips, and you'll be first to know when spots open again.
>
> {{coach_name}}

---

## Waitlist email · sent when someone takes the quiz after all 30 spots are full
**Subject:** You're on the list, {{first_name}}

> Thanks for taking the Metabolic Score. All 30 founding spots are full, so **you're on the waitlist.** You'll be the
> first to hear when a spot opens.
>
> In the meantime, you'll get the 7-Day Metabolic Reset by email: small daily actions you can start today.
>
> {{coach_name}}

## Send rules
- **Wave schedule:** wave 1 → week 1 (days 0–8). Start the next wave only if spots remain.
- **When spots hit 0:** stop the sequence, remove "{{spots_left}}" lines, switch all CTAs to the waitlist (the site does this automatically from `config.js`).
- **Tracking:** tag each wave (`launch_wave1`…) so the Reporting agent can compare open → quiz → call → enrolled by wave.
