# Domains

> **Decision (Sept 30, 2026):** the program gets its own domain, **metabolicgfcxtremefit.com**, registered at
> **Cloudflare** (active within 1 business day). The site is hosted free on **Cloudflare Pages** in the same account,
> so there's no separate DNS step. GFC Lab lives at **lab.metabolicgfcxtremefit.com** (Altrohealth) and shows inside the
> GFC Lab tab. The notes below from the earlier subdomain plan still apply, with the new domain in place of gfcxtreme.com.
>
> **Email sending on a brand-new domain:** new domains have no sending reputation. Authenticate it (SPF, DKIM, DMARC:
> the email platform gives the records, and they're added in Cloudflare DNS) and warm it up: ~50/day for 2–3 days,
> then ~150/day, then the 512-contact waves. Or send the launch from the existing gfcxtreme.com mailbox domain if
> its DNS is reachable.

## Original plan: how the website, client app and GFC Lab fit together

A subdomain is a free prefix on a domain you already own (`gfcxtreme.com`). Each one is created with a single DNS
record at your domain registrar and can point to a **different service**. The visitor sees one GFC Xtreme brand,
and each part runs where it belongs.

```
gfcxtreme.com               → current GFC Xtreme website (unchanged)
metabolicgfcxtremefit.com     → Metabolic Free site: Home, The Science, Program, quiz, client login   (site/)
lab.metabolicgfcxtremefit.com           → GFC Lab: Altrohealth's platform (intake, clinicians, prescriptions, pharmacy)
```

## Why GFC Lab should be a subdomain, not a page we build
- **HIPAA and prescriptions stay with Altrohealth.** Intake forms, medical records, clinician visits and payments run on
  their certified, HIPAA-compliant systems. We never touch medical data.
- **Their LegitScript certification stays valid**, because the medical pages are still served by them.
- **It still feels like your site:** your address (`lab.metabolicgfcxtremefit.com`), your GFC Lab tab in the menu, and (if they
  offer white-label) your logo and colors.
- Embedding their intake inside our page with an iframe is the fallback. It often breaks logins, payments and
  cookies, so it's used only if they can't do a custom domain.

## GFC Lab as a tab inside the site (built)
The **GFC Lab** tab can show Altrohealth *inside* our page: the menu stays on top and their platform appears
below it, with an "Open full screen ↗" link as a backup. Set in `site/config.js`:

```
ALTROHEALTH_URL:   "https://lab.metabolicgfcxtremefit.com"   // or whatever link Altrohealth gives you
ALTROHEALTH_EMBED: true                          // false = the tab opens GFC Lab in a new window instead
```

Their pages are still served by Altrohealth's servers, so medical data goes straight to them. This only works if
Altrohealth **allows embedding** (the technical terms are `X-Frame-Options` / `frame-ancestors`), so ask them. On iPhone
Safari, logins inside embedded pages can be blocked, so the full-screen link stays visible.

## Where is gfcxtreme.com's DNS?
Look it up at **lookup.icann.org** (type `gfcxtreme.com` and check "Nameservers"):
- `ns…domaincontrol.com` → **GoDaddy**
- `…ns.cloudflare.com` → **Cloudflare**
Whichever it shows is where the CNAME records get added.

## Setup steps
1. **Ask Altrohealth** (copy/paste):
   > "We'd like GFC Lab to run on our own subdomain, `lab.metabolicgfcxtremefit.com`. Do you support custom domains / white-label
   > for partners? If so, what DNS record (CNAME) should we add, and can the pages use our logo and colors
   > (orange #F26B2A / black)? Can your patient pages be embedded (iframe) on metabolicgfcxtremefit.com
   > (frame-ancestors allowed)? If not, do you provide a partner referral link with tracking?"
2. **Find where your DNS lives:** the company where you bought gfcxtreme.com, or where its DNS is managed
   (GoDaddy, Namecheap, Cloudflare, Wix, Squarespace, Google/Squarespace Domains…).
3. **Host the Metabolic Free site** on a free static host (Netlify, Vercel or Cloudflare Pages) and connect
   `metabolicgfcxtremefit.com` to it. The host tells you the exact CNAME to add, and it issues HTTPS automatically.
4. **Add the DNS records** (about 5 minutes each):

   | Type | Name | Value | For |
   |---|---|---|---|
   | CNAME | `metabolic` | *(given by Netlify / Vercel / Cloudflare)* | Metabolic Free site + client app |
   | CNAME | `lab` | *(given by Altrohealth)* | GFC Lab |

5. **Update `site/config.js`:** set `ALTROHEALTH_URL` to `https://lab.metabolicgfcxtremefit.com`, and Supabase's allowed
   redirect URL to `https://metabolicgfcxtremefit.com/app/`.

## Subdomain vs. new domain
| | Subdomain (`metabolicgfcxtremefit.com`) | New domain (e.g. a Metabolic Free .com) |
|---|---|---|
| Cost | Free | ~$12–20/year |
| Trust | Borrows GFC Xtreme's name and history | Starts from zero |
| Email | Launch emails come from the gym's domain, which your 2,049 contacts already know | Needs a new, warmed-up sending domain |
| Brand | "Part of GFC Xtreme" | Standalone brand, easier to grow beyond one gym |

**Recommendation:** launch on subdomains now. If Metabolic Free grows into its own brand, buy the new domain later
and point it at the same site. Nothing gets rebuilt.
