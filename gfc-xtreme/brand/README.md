# Brand assets

Everything here is referenced from `brand.config.json`. Replace a file, keep the
name, run `node gfc-xtreme/scripts/build-tokens.mjs`.

| File | What it is |
|------|------------|
| `gfc-logo.png` | the full mark, black keyed to transparent so it sits on any dark surface |
| `gfc-logo-header.png` (+`@2x`, `@3x`) | the mark at header height, 44 / 88 / 132 px tall |
| `gym-bg.jpg` | the sign-in photograph, 896×1200, darkened to 62% |
| `gym-bg-480.jpg` | the same, 480px wide, served below a 520px viewport |

## The logo

Supplied as a PNG on a black field. The black was keyed to transparency by luminance
(fully clear below 10, fully opaque above 60, ramped between), which keeps the soft
edges of the grunge texture on "GFC" and the rope graphic rather than hard-cutting them.

**Supply the vector when you can find it.** A PNG is fine at header size and fine on the
App Store icon, but an SVG would sharpen the mark at every size and shrink the bundle.
The slot and the filenames stay the same, so it is a drop-in.

## The photography

Darkened at build time rather than in CSS, so the bytes sent to a phone are already the
bytes shown — a full-brightness photo dimmed by an overlay costs the same download and
gains nothing. The CSS lays a gradient scrim on top of that, heaviest where the sign-in
form sits.

Swap in your own gym's photography freely. Two things to keep: a **dark frame** (the
scrim assumes it) and **empty space in the upper third**, where the logo sits.
