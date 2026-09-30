# The hero video: one video, one offer, everywhere

**Strategy:** record **one** strong 60–75-second video that speaks to the whole population at once:
people on GLP-1s losing muscle, people on or curious about hormone therapy, and the many who are metabolically ill
(pre-diabetic or diabetic) without knowing it. Then push that same video, with the same offer, through every channel.

At a $500/month budget this is the right approach. One ad set with one video gets all the data, instead of splitting
$16/day across angles that never finish learning. Meta's broad targeting now works this way anyway: the video does
the targeting.

## What we cut from the one recording

Film the body **once**. Film **3 different opening lines** (5 seconds each). The Ads agent pairs each opening with
the same body, which gives 3 ads for the cost of one video.

| Opening (first 3–5 s) | Speaks to |
|---|---|
| A. "If you're losing weight fast, how much of it is muscle?" | GLP-1 users |
| B. "1 in 3 adults has pre-diabetes, and more than 8 in 10 of them don't know it." | Hidden metabolic illness |
| C. "Medication. Hormones. Devices. Use every tool, then make yourself not need them." | Hormones / the whole Metabolic Flex idea |

(Stat B source: CDC National Diabetes Statistics Report. Link it in the caption and on the landing page.)

## Body script (~60 s, same for all three)

> I'm Coach Gui from GFC Xtreme, and I coach people to become **metabolic dysfunction free**.
>
> Here's what I see every day. People on GLP-1s are losing weight, but up to around 40% of it can be muscle,
> and that muscle is what keeps your metabolism running. People who want hormone therapy but have no plan around it.
> And people whose blood sugar is quietly climbing, and nobody's told them.
>
> My program uses **every tool we have**: GLP-1s and hormone therapy through licensed medical partners when they fit,
> training that protects your muscle, and a **Lumen device, free**, that shows from your breath whether you're
> burning fat or carbs each morning.
>
> Then every two weeks, you and I meet. **Discipline, accountability, consistency.** The tools get you started,
> and the habits keep you there.
>
> Take my free 2-minute Metabolic Score at the link. If it's a fit, your Lumen is on me.

**On screen:** captions burned in · the Lumen in hand at the "free" line · end card with the quiz URL.
**Don't say:** "you have diabetes", "reverse diabetes", "get off your meds", or drug brand names (see guardrails).
**Price** stays off the video. It's covered on the call ($299/mo × 3 months, then $199/mo for 6 months).

## Where the same video goes ("the blast")

| Channel | How | Cost |
|---|---|---|
| Meta ads | 1 campaign → 1 ad set → openings A/B/C. The winner gets the budget after ~$100 spent | $500/mo |
| Instagram + Facebook | Reel + pinned post: "Comment SCORE" → auto-DM with the quiz link | Free |
| TikTok, YouTube Shorts | Same file | Free |
| WhatsApp | Your status + personal send to your contacts ("I launched this, would love your support") | Free |
| Email + SMS to **your own** list | GFC Xtreme members, past clients: send once, with the link | Free |
| Landing page | Top of `site/index.html`, above the quiz | Free |
| GFC Xtreme gym | QR code poster + the video on the gym screen | Print |
| Referral partners | Send to doctors, chiropractors and pharmacists to share | Free |
| LinkedIn | Native upload + employer pitch (see `linkedin-outreach.md`) | Free |

**What "blast" can't mean:** texting or emailing people who never gave you their number or email (bought lists,
scraped contacts). That breaks TCPA/CAN-SPAM, and a single SMS lawsuit costs more than a year of ads. Blast to
your own contacts, followers and ad audiences only.

## How long one video lasts

- At ~$16/day, one video can run for **2–3 months** before it wears out. The warning signs: frequency above 3 and
  cost per lead up 30% from its best week.
- When that happens, record **one new body** or **3 new openings**. That's about 15 minutes of filming a month.
- Organic posts can reuse the same video every few weeks with a new caption. Most followers won't have seen it.

## Production with Higgsfield

**Rule: the person talking is you.** Higgsfield makes it look professional; it doesn't replace you. People buy a
coach they trust, and Meta and the FTC both penalize misleading AI content in health ads.

| Piece | How | Higgsfield tool |
|---|---|---|
| The body + 3 openings | **Option 1 (best):** you on camera, 10 min of phone footage. **Option 2:** an avatar built from your own photos + a clone of your own voice, reading the script | Upscale / reframe · or avatar + `create_voice` from your recordings |
| B-roll (cutaways) | Lifting, protein meal, breathing into a Lumen, a morning walk, a coaching video call | Image → video generation |
| Formats | 9:16 (Reels/TikTok/Shorts), 4:5 (feed), 1:1 | Reframe |
| Captions + end card | Quiz URL, "Free Lumen ($249 value)" | Editor / CapCut |

**Never generate:** fake clients, fake testimonials, AI before/after bodies, anyone in a white coat or presented as a
doctor, or a real brand's medication packaging. If the talking person is an AI avatar, turn on Meta's "AI info"
disclosure. Real-looking AI people who don't exist, presented as clients, are deceptive advertising.

**Production status (Sept 26, 2026):** Option 2 chosen. Digital twin **"Coach GFC Xtreme"** (Higgsfield Soul V2,
soul_id `16ccf338-368f-4d70-8bcf-dc434815a406`) trained from 19 of the coach's photos. Voice clone: **"Gui-Filizzola-Cury"** (Higgsfield element voice `c8ce33af-fd22-4af8-aaae-9663923ee34e`), recorded by the coach.
Talking-video pipeline: script line → `seed_audio` in the coach's voice → `seedance_2_5` (omni_reference: approved
still as start image + that audio as reference) → lip-synced clip. Test clip: opening A, 5 s, 720p (35 credits);
the final uses 1080p (~60 credits per 5 s).
Shirt reference: Higgsfield media `ed95d66f-02e1-4ce3-bbe3-e8ff10a015a8` (navy performance shirt, full logo centered on chest).
Test stills: `af833a84…` (Soul V2 likeness test) → `83c7dcb6…` (GPT Image 2.5 edit with the real shirt, 2.75 credits). **APPROVED by the coach (Sept 28): logo, likeness and shirt all correct. This is the master still for all video.**
Pipeline: Soul V2 stills of the coach (gym / office settings) → talking video driven by the coach's cloned voice →
b-roll → edit in 9:16, 4:5 and 1:1. Every script is approved by the coach before generation.

**What I need from you to produce it:** 10–20 clear photos of you (face, gym, different angles), 1–2 minutes of
your voice reading anything (for the voice clone, only if you choose Option 2), and your OK on the final script above.
Or just the phone footage for Option 1.

## Production log: full set (Sept 28, 2026, approved by the coach after the test clip)

All clips: `seedance_2_5` omni_reference, 1080p, 9:16, start image = approved still `83c7dcb6…`, voice = coach's clone.

| # | Piece | Line | Voice job | Video job | Length |
|---|---|---|---|---|---|
| 1 | Opening A (GLP-1 muscle) | "If you're losing weight fast… how much of it is muscle?" | `92d808e5…` | `cc248a99-e2aa-442d-a90e-3eae64b9c63d` | 5 s |
| 2 | Opening B (hidden pre-diabetes) | "One in three adults has pre-diabetes… more than eight in ten don't know it." | `7ba9c362…` | `074635ea-6402-4ed4-958c-da0c85156d2d` | 7 s |
| 3 | Opening C (every tool) | "Medication. Hormones. Devices. Use every tool… then make yourself not need them." | `9aba14bc…` | `56cd869d-b932-4c02-aaff-ca67efeb7ace` | 7 s |
| 4 | Body 1 (intro + muscle) | "I'm Coach Gui from GFC Xtreme, and I coach people to become metabolic dysfunction free… keeps your metabolism running." | `b5890af4…` (v2) | `9b9dcc80-2f96-4fe5-bd45-37fb6794c868` (v2, **approved Sept 28**; v1 `8b6bf48f…` said "metabolically free", replaced at the coach's request) | 17 s |
| 5 | Body 2 (hormones + blood sugar) | "People who want hormone therapy… nobody's told them." | `f73e94f5…` | `c5cba913-1789-463b-944a-7e5221b1452a` | 10 s |
| 6 | Body 3 (every tool + free Lumen) | "My program uses every tool we have… fat or carbs each morning." | `40cf3268…` | `afa1a979-be04-47a8-81dc-24106b9730b1` | 18 s |
| 7 | Body 4 (accountability + CTA) | "Then every two weeks, you and I meet… your Lumen is on me." | `18e8bfa1…` | `3954f37d-84e4-4f36-b0ea-e7ac72a96444` | 19 s |

Cost: ~984 credits of video (12 credits/s at 1080p) + voice tracks.
Final edits: each opening (1, 2 or 3) + body 4–7 → three ~60–70 s ads; captions burned in, black/orange end card with the quiz URL; 9:16 master, then 4:5 and 1:1.
