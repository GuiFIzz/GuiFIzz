# Compliance guardrails (enforced in the VALIDATE step)

Health marketing is the most regulated area in advertising. Getting an ad
account banned or receiving an FTC letter costs more than any campaign earns.
These rules are **hard blocks** for every agent. *This is operational guidance,
not legal advice; have a healthcare attorney review before launch.*

## 1. Health claims (FTC + platform policies)

| Blocked | Use instead |
|---|---|
| "Reverse / cure diabetes" | "Improve your blood sugar markers", "work alongside your doctor" |
| "Get off your medication" | "Many clients work with their doctor to reduce medication needs" (only with proof + approval) |
| "Lose 30 lbs in 30 days", specific guaranteed results | "Lose fat, keep muscle" + real, consented testimonials with a "results vary" note |
| Before/after images in **Meta ads** | Allowed organically with consent; in ads, use single "after" or lifestyle imagery |
| "Are you diabetic?", "You're overweight" (Meta personal-attribute rule) | "Tired of blood sugar swings?", "For people who want to…" |
| Unsourced statistics | Every stat in a post links a source (CDC, NIH, peer-reviewed study) |

## 2. GLP-1 and hormone therapy advertising

- **Partners: Altrohealth / OpenLoop** hold LegitScript. That certification covers *their* domain and ads. **Your** ads
  and landing page are a separate advertiser, so either (a) keep your ads coaching-first and send medication interest to the
  partner's certified intake page, or (b) ask the partner whether their certification can extend to your co-branded page.
  Confirm in writing before naming any drug in an ad.
- **Google and Meta require LegitScript certification** (or equivalent) to advertise prescription drugs or
  online pharmacy/telehealth prescribing. Until you or your telehealth partner are certified:
  **ads promote coaching and Lumen, not medication.** Medication is discussed on the discovery call and in
  organic content that's educational only.
- Never name a drug brand (Ozempic, Wegovy, Mounjaro, Zepbound) in paid ads without certification.
- Compounded GLP-1s: never claim they are "the same as" or "generic" brand drugs; the FDA has warned on this.
- Prescribing only after evaluation by a clinician **licensed in the client's state**. The coach never implies
  a prescription is guaranteed.

## 3. Health data (HIPAA / privacy)

- If you (or your telehealth arm) are a covered entity, quiz answers tied to a person can be PHI. Store them only in
  tools that sign a **BAA**.
- **Never send health answers to ad platforms.** The Meta Pixel and Google tag get the event name only
  (`Lead`, `Schedule`, `Purchase`), no URL parameters or custom data containing conditions. The quiz result
  page URL must not contain the segment (use `/thanks`, not `/thanks?type=diabetic`).
- Use the Conversions API with hashed email/phone only.
- The privacy policy states what is collected and why. The FTC Health Breach Notification Rule applies to
  health apps and sites even outside HIPAA.

## 4. SMS and email (TCPA / CAN-SPAM / 10DLC)

- SMS consent is a **separate, unchecked checkbox** with clear language, never bundled. Store timestamp + IP.
- Register the SMS number with **A2P 10DLC** before sending.
- Quiet hours: no texts before 8am or after 8pm in the lead's local time.
- Every SMS supports STOP; every email has an unsubscribe link + physical address.
- Max 1 marketing SMS/day, 4/week.

## 5. LinkedIn and "internet scraping"

**We don't scrape LinkedIn.** Automated scraping violates LinkedIn's User Agreement, gets accounts banned,
and cold-contacting scraped personal data creates GDPR/CAN-SPAM/state-privacy exposure. It's also a poor fit:
nobody lists "pre-diabetic" on their profile. What works better:

- **LinkedIn Sales Navigator** (allowed) to find **HR / benefits leaders** at 50–500-employee companies, then offer
  a **corporate metabolic health program**. That's B2B, where LinkedIn is strong, and one contract = many clients.
- A founder-voice LinkedIn content plan (see `campaigns/linkedin-outreach.md`), with manual, personalized
  connection requests (≤ 20/day).
- Public, permission-based lists: local employer wellness fairs, chambers of commerce, gym partnerships, doctor
  and chiropractor referral partners.

## 6. Scope of practice

- The coach coaches. Diagnosing, prescribing and dosing are for a licensed clinician.
- Every lead with red-flag answers (e.g. type 1 diabetes, insulin-dependent, pregnancy, eating-disorder history,
  chest pain) is routed to "see your physician first" and flagged for the coach, not auto-sold.
