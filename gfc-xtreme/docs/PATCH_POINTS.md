# Patch points

Everything the brand changes in upstream openGym, and why. The whole surface is six
files and about fifteen lines — small on purpose, because openGym ships releases
regularly and every line we add here is a line that can conflict later.

`scripts/apply-overlay.sh` does the first five automatically and refuses to run if an
anchor has moved. The last two are component edits and are done by hand.

## Applied by the script

| # | File | Change |
|---|------|--------|
| 1 | `frontend/src/lib/format.js` | `gfc: '#FC6228'` added to `ACCENTS`, `gfc: '#000000'` to `ACCENT_INK` |
| 2 | `frontend/src/lib/accent.js` | `DEFAULT_ACCENT` becomes `'gfc'` |
| 3 | `frontend/src/main.jsx` | imports `./gfc-brand.css` after `index.css` |
| 4 | — | `gfc-brand.css` and `public/brand/*` copied in |
| 5 | `frontend/index.html` | `data-brand="gfc"` on `<html>` |
| 6 | `frontend/src/lib/accent.test.js` | eleven assertions read `DEFAULT_ACCENT` instead of the literal `'lime'` |
| 7 | `frontend/src/lib/format.js` + 19 locale packs | the accent gets an accessible name |
| 8 | `frontend/src/views/Settings.accent.test.jsx` | the shown default name reads `ACCENT_NAMES[DEFAULT_ACCENT]` |

### Why the accent is a preset and not a custom colour

openGym already has an accent system: named presets in `ACCENTS`, a user-chosen hex
under `'custom'`, and `--acc` / `--acc-2` / `--on-acc` set from whichever is active.
Registering `gfc` as one more preset means Settings, the swatch picker, the Android
native theme colour and the per-account sync all keep working with no special cases —
and a member who would rather train against blue can still pick it.

Forcing the colour in as `custom` would have taken the own-colour slot away from
members, and overriding `--acc` globally would have broken the picker silently.

### Why upstream's tests were edited

Three of them asserted things our change legitimately makes untrue. In each case the
literal was replaced by the constant it stands for, so the next brand change touches
none of them:

- **`accent.test.js`** asserted the fallback accent as the bare string `'lime'`, eleven
  times. Swapping in `'gfc'` would only move the problem to the next rebrand, so the
  assertions now read the `DEFAULT_ACCENT` constant. This is the last time a rebrand
  touches that file.
- **`format-names.test.js`** requires every accent to have a name in `ACCENT_NAMES` *and*
  a translation of that name in all nineteen locale packs — the swatches are read aloud
  by screen readers and `"gfc"` is not a word. Each pack's name is built from the word
  that pack already uses for `'Orange'` (`GFC Laranja`, `GFC Orange`, `GFC 橙色`), so
  nothing is machine-translated. Have a native speaker check these if it matters to you.
- **`Settings.accent.test.jsx`** asserted the *displayed name* of the default accent as
  `'Green'`; it now reads `ACCENT_NAMES[DEFAULT_ACCENT]`. This one only surfaced on a
  full-suite run — the three obvious accent files passed without it, which is the argument
  for running all 543 files rather than the ones that look related.

A third test, **`color-mix-fallback.test.js`**, was not edited — it caught a real bug in
our own CSS. It requires a plain declaration before any `color-mix()`, because Safari
before 16.2 has neither. Members are on iPhones, so the generator now emits the `rgba()`
fallback ahead of every mix.

## Done by hand

These are JSX edits inside components, with no stable one-line anchor to patch against.

### `frontend/src/App.jsx` — the mark in the corner

Render it once, inside the app shell, above the routed content:

```jsx
<img className="gfc-mark" src="/brand/gfc-logo-header.png"
     srcSet="/brand/gfc-logo-header@2x.png 2x, /brand/gfc-logo-header@3x.png 3x"
     alt="GFC Xtreme Fitness" />
```

`.gfc-mark` is `position: fixed`, offset by openGym's own `--sat` (the status bar) and
`--conn` (the connection banner), so it never collides with either and never scrolls away.
It is `pointer-events: none` — it is a mark, not a button. If you later want it to go Home
on tap, wrap it in a `<Link>` and drop that line.

### `frontend/src/views/Login.jsx` — photography behind the sign-in

```jsx
<div className="gfc-login-bg" aria-hidden="true" />
<img className="gfc-mark gfc-mark--login" src="/brand/gfc-logo-header.png"
     srcSet="/brand/gfc-logo-header@2x.png 2x, /brand/gfc-logo-header@3x.png 3x"
     alt="GFC Xtreme Fitness" />
```

and put `gfc-login-card` on the class list of the sheet holding the sign-in buttons.

The photo is decorative, so it is a CSS background and is hidden from assistive tech.
It is served at 480px wide below a 520px viewport, and replaced by the flat brand black
for anyone who has asked for reduced motion or more contrast — a photograph behind a
form is a legibility risk, and that preference is how people say so.

### `.env`

```
RP_NAME="GFC Xtreme"
```

This is the name the phone shows in the Face ID / Touch ID prompt when a member signs in.
It is the one piece of branding that lives outside the frontend.

## What was deliberately left alone

- **The other eight accents.** Members keep the choice.
- **Light mode.** The brand orange measures 3.04 on white — fine for large text and the
  button fills it already has, not for body text. openGym's light theme handles this with
  its own `--on-acc`; we inherit that rather than fight it.
- **Status colours.** A PR stays green, a warning amber, an error red. If achievement and
  brand share a colour, neither reads.
- **The 1,469 "openGym" strings** in the UI copy. Renaming those is the next piece of work
  and belongs at the `t()` chokepoint in `lib/i18n-core.js`, not in a find-and-replace.
