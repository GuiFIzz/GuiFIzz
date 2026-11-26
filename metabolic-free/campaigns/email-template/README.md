# Mobile email template (v2)

`parts.py` builds the approved mobile-first email shell. `build_bc.py` renders the two
approved reference emails (`test-B.html`, `test-C.html`).

    cd metabolic-free/campaigns/email-template && python3 build_bc.py

## The structure, and why

- **Slim dark header**: 116px logo left, orange pill right. The pill points at the SAME
  destination as the main button below — one ask, available above the fold.
- **30px headline + grey deck line**: the idea lands without reading a paragraph.
- **One picture, clickable, chosen for the message** (not stock gym filler):
  - `hero_side()` = **B layout**, 150px thumbnail left + copy right. Use for TEACHING emails.
  - `hero()` = **C layout**, full width. Use for PROOF emails.
- **One CTA**, benefit + mechanic: "Keep your muscle — book free call →".
- **Labs card**: black rounded card, "Want results faster? / Add the medical side.",
  GLP-1 · Peptides · Hormone therapy in orange, its own button, Supplements under a rule.
  Appears on every email.

## Image rules (do not break)

- Email images live in `site/media/email/` as **600px JPG**. `.webp` does not render in
  Outlook or older Apple Mail — five emails shipped broken because of it.
- **Generated concept art is for ideas only.** Before/after photos, the Lumen device and
  the coach's own photos stay real. Never generate an image that depicts a client result
  or a product the client will actually receive.
- Concepts generated with Higgsfield `z_image` (0.15 credits each; a 150px thumbnail does
  not justify a 2k render): muscle, meal, strength40, accountability, longgame, bloodsugar,
  chairtest, breakfast.
