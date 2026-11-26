# Discovery-call emails (Cal.com → /api/calcom → Systeme.io tags)

Cal.com sends the booking confirmation, reminders and calendar invite itself. These Systeme.io
automations cover what Cal.com doesn't. Each one starts when the tag is added (Automation rule:
"Tag added" → "Send email"). Booking link: https://cal.com/gfcxtreme-fitness-nmylwf/30min

**Calls must use Cal Video (Cal.com's own video), not Google Meet or Zoom.** No-show detection and
the "Meeting ended" event only work inside Cal.com's own video — Cal.com has no visibility into who
joined a separate Google Meet/Zoom session, so the whole flow below silently does nothing on
Google Meet.

| Tag | Starts | Also |
|---|---|---|
| `call_booked` | Email 1 right away | Remove the contact from the "book a call" nurture campaign |
| `call_cancelled` | Email 2 after 1 hour | |
| `call_no_show` | Subscribes to the "No-Show Recovery" campaign: Email 3 immediately, Email 3b 2 days later |  |
| `call_attended` | Subscribes to the "Attended Follow-up" campaign: Email 4 immediately, Email 5 2 days later | Fires on Cal.com's "Meeting ended" event, skipped if the contact is already tagged `call_no_show` (that trigger fires first, at the 7-minute mark) |

When someone rebooks, the webhook removes `call_cancelled` / `call_no_show` and adds `call_booked`.
The `call_booked` and `call_attended` automation rules both unsubscribe the contact from the nurture
campaign and the No-Show Recovery campaign, so later no-show emails never fire once someone has
rebooked or attended.

Note: `call_attended` reuses the tag originally named `segment_weight_energy` (renamed 2026-10-08) —
Systeme.io's 10-tag plan limit was already maxed out, and that segment tag had zero contacts and no
automation rule attached to it.

---

**Email 1: call_booked**
> Subject: You're booked, {{first_name}}. 2 things before our call
>
> Hi {{first_name}},
>
> Our call is set. To make the most of our time:
>
> 1. Have your Metabolic Score handy (it's in your inbox), plus any recent labs like A1c or fasting glucose if you have them.
> 2. Think about the one thing you'd most like to change in the next 90 days.
>
> The call is on video. The link is in your calendar invite from Cal.com.
>
> See you soon,
> Coach Gui, GFC Xtreme Fitness

**Email 2: call_cancelled**
> Subject: No problem, let's find a better time
>
> Hi {{first_name}},
>
> I saw you had to cancel. Life happens. When you're ready, pick a time that works here:
> https://cal.com/gfcxtreme-fitness-nmylwf/30min
>
> Coach Gui

**Email 3: call_no_show**
> Subject: Sorry we missed you, {{first_name}}
>
> Hi {{first_name}},
>
> I was on our video call and didn't see you come in. No worries, it happens.
> Grab another time that works better for you here:
> https://cal.com/gfcxtreme-fitness-nmylwf/30min
>
> Coach Gui

**Email 3b: call_no_show, 2 days later, only if not rebooked**
> Subject: Still want your plan?
>
> Hi {{first_name}},
>
> Your spot for a free strategy call is still open. It takes 15–30 minutes and you'll leave with
> your next three steps, whether or not you join.
> https://cal.com/gfcxtreme-fitness-nmylwf/30min
>
> Coach Gui

**Email 4: call_attended**
> Subject: Good talking with you, {{first_name}} — here's what's next
>
> Hi {{first_name}},
>
> Thanks for jumping on the call today. I hope it was useful, whichever way you decide to go.
>
> If you're ready to lock in your spot in Metabolic Flex Foundations, just reply to this email and
> I'll get you set up right away.
>
> Still weighing it? Totally fine. Grab a quick follow-up time and we'll iron out whatever's left:
> https://cal.com/gfcxtreme-fitness-nmylwf/30min
>
> Coach Gui

**Email 5: call_attended, 2 days later, only if not re-tagged**
> Subject: Still deciding, {{first_name}}?
>
> Hi {{first_name}},
>
> Wanted to check back in after our call. Founding spots are capped at 30, and they're going.
>
> If you're ready, just reply and I'll get your spot locked in. Still have questions? Grab a
> follow-up time here: https://cal.com/gfcxtreme-fitness-nmylwf/30min
>
> Coach Gui
