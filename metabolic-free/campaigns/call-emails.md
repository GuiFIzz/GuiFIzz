# Discovery-call emails (Cal.com → /api/calcom → Systeme.io tags)

Cal.com sends the booking confirmation, reminders and calendar invite itself. These three Systeme.io
automations cover what Cal.com doesn't. Each one starts when the tag is added (Automation rule:
"Tag added" → "Send email"). Booking link: https://cal.com/gfcxtreme-fitness-nmylwf/30min

| Tag | Starts | Also |
|---|---|---|
| `call_booked` | Email 1 right away | Remove the contact from the "book a call" nurture campaign |
| `call_cancelled` | Email 2 after 1 hour | |
| `call_no_show` | Subscribes to the "No-Show Recovery" campaign: Email 3 immediately, Email 3b 2 days later |  |

When someone rebooks, the webhook removes `call_cancelled` / `call_no_show` and adds `call_booked`.
The `call_booked` automation rule unsubscribes the contact from both the nurture campaign and the
No-Show Recovery campaign, so Email 3b never fires if they've already rebooked.

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
