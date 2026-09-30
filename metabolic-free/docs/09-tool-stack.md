# Tool stack decisions (Sept 30, 2026)

Research date: Sept 30, 2026. Prices change, so confirm at checkout.

## Email marketing: **Systeme.io Startup, $17/mo** (recommended)

| | Systeme.io Startup | Brevo Standard | MailerLite (Comfort) | GoHighLevel Starter |
|---|---|---|---|---|
| Price | **$17/mo flat** (2 months free yearly) | $18/mo base, scales with **emails sent** | ~$15/mo at 2,500 subs, scales with subscribers | ~$97/mo |
| Contacts | 5,000 | Unlimited | ~2,500 at that price | Unlimited |
| Email sends | **Unlimited** | 5k/mo at base, more costs more | Plan-based | Unlimited-ish |
| Automations (14-day nurture) | ✅ | ✅ (not on Free/Starter) | ✅ | ✅ |
| Forms / landing pages / tags | ✅ | ✅ | ✅ | ✅ |
| SMS | ❌ | ✅ pay-as-you-go | ❌ | ✅ |
| Booking calendar | ❌ (use Cal.com) | Basic | ❌ | ✅ |

**Why Systeme.io:** we have **2,049 emails** now (over Systeme's 2,000 free-plan cap), and month 1 sends roughly
**10,000–12,000 emails** (5 launch emails × 2,049 + nurture). Flat pricing with unlimited sends is the cheapest for
that volume. Brevo becomes the better pick later **if we add SMS in the same tool**. GoHighLevel is the all-in-one,
but at ~$97/mo it isn't worth it until the roster is ~20+ clients.

## Scheduling: **Cal.com Free, $0**
Unlimited event types (discovery call 15 min, coaching session 30 min, renewal session), Google Calendar sync,
video links, email reminders, **webhooks** (so a booking can tag the contact in Systeme.io), and embedding in the site.
Calendly's free plan allows only 1 event type.

## Website hosting: **Cloudflare Pages, $0**
The domain is already at Cloudflare. It deploys the `site/` folder, and HTTPS is automatic.

## Client platform database: **Supabase**, needed before the first client starts, not for launch
The website, quiz and emails run without it. Supabase only powers client logins, daily check-ins and the coach
roster, so turn it on before the first enrolled client's week 1.

## Monthly software cost at launch
| Tool | Cost |
|---|---|
| Systeme.io Startup | $17 |
| Cal.com | $0 |
| Cloudflare Pages + domain | ~$1/mo (domain ~$10–12/yr) |
| Supabase | $0 (free tier) |
| **Total** | **≈ $18/month** |

Sources: Brevo, MailerLite, Systeme.io and Cal.com pricing via 2026 reviews (emailtooltester.com, sendx.io,
capterra.com, koalendar.com), Sept 2026.
