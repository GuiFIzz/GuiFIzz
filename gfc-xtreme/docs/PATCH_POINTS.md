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

## The mark on screen (`patch-chrome.py`)

| File | Change |
|---|---|
| `App.jsx` | the mark, fixed upper-left, rendered **outside `#app`** — a fixed element inside it rides along with the page transition's transform, which is upstream's own reason for everything else that sits out there |
| `views/Login.jsx` | the photograph behind sign-in, the mark in the corner, and the stock head removed |
| `views/MobileOnboarding.jsx` | the logo in place of the stock head |

These were manual until they were not. Leaving them by hand meant a fresh checkout was
never actually branded until somebody remembered to finish it.

**Why the stock head goes.** Upstream centres a dumbbell icon above an `<h1>` of the
product name. After the rename that `<h1>` reads "GFCXtreme" in plain text, so alongside
the corner mark the brand would appear twice on one screen — and the logo *is* the
wordmark. Onboarding has no app chrome to hold a corner mark, so there the logo takes the
head's place rather than being dropped. Removing the head orphans the `Icon` and
`PRODUCT_NAME` imports it used, and those are removed with it.

## The one thing still done by hand

```
.env
RP_NAME="GFCXtreme"
```

The name shown in the Face ID / Touch ID prompt when a member signs in. It is the only
piece of branding that lives outside the build, because it is the API's configuration
rather than the app's code.

## What was deliberately left alone

- **The other eight accents.** Members keep the choice.
- **Light mode.** The brand orange measures 3.04 on white — fine for large text and the
  button fills it already has, not for body text. openGym's light theme handles this with
  its own `--on-acc`; we inherit that rather than fight it.
- **Status colours.** A PR stays green, a warning amber, an error red. If achievement and
  brand share a colour, neither reads.
- **The 1,469 "openGym" strings** in the UI copy. Renaming those is the next piece of work
  and belongs at the `t()` chokepoint in `lib/i18n-core.js`, not in a find-and-replace.

---

# The product name

The name itself lives in `brand/brand.config.json` (`identity.productName`, currently
**GFCXtreme**, with `fileSlug` as its lowercase form). Changing it is one edit there plus
a re-run of `apply-overlay.sh` — the examples below use the current value, but nothing in
the code does.

`openGym` appears about 1,470 times in the frontend. Almost none of them were replaced
one by one, because most are not what they look like.

## The chokepoint

1,224 of those occurrences are in the nineteen locale packs — and they are in strings
whose **keys are the English source text**. Rewriting a key stops the pack matching;
rewriting only the value leaves every string upstream adds next month saying `openGym`
again.

So the swap happens at the one point every translated string passes through:

```js
// lib/i18n-core.js
const UPSTREAM_NAME = 'openGym'
const brandName = v =>
  typeof v === 'string' && v.includes(UPSTREAM_NAME) ? v.replaceAll(UPSTREAM_NAME, PRODUCT_NAME) : v
```

applied inside `t()` and inside `tn()`'s fast path (which returns without calling `t()`).
One constant rebrands every string in every language, and keeps doing it for strings
that do not exist yet.

Two details that matter:

- **The key is never touched**, only the resolved value — so a pack still matches after
  an upstream update.
- **The swap runs before `{0}` interpolation**, so a member's own routine called
  "openGym leg day" is not quietly renamed in a message about it.

## What is NOT renamed, and why

About a hundred occurrences are not the brand at all:

| Kept as upstream wrote it | Why |
|---|---|
| `opengym-state.json`, `opengym-remote.json`, `opengym-stash.json` | the phone's state files — invisible, and renaming orphans them |
| `opengym-media-v1`, `opengym-device` | cache names |
| `opengym:back-preview` | an internal event name |
| `opengym-bw-…` | **Health Connect record ids** — rename these and the app loses track of every body-weight record it has already written, and re-writes them all |
| `ch.duartesantos.opengym` | the Android package. Renaming it is a new signing identity and a new Play listing, not a brand edit |
| `openGymSheet` | a history-state key |
| "Media licensed for use in openGym only" | a **quotation of the media licence** (agreement §8c, which is why upstream marks it as untranslated). It describes the agreement *openGym* holds with gymvisual.com; rewriting it would misstate a licence we do not have |

## What IS renamed beyond the UI copy

| Renamed | Why it is not just an identifier |
|---|---|
| `Documents/openGym` → `Documents/GFCXtreme` | members browse to it, and the UI names it in its own copy — leaving it would have made the app lie about where it put their data |
| `opengym-backup-*.json` → `gfcxtreme-backup-*.json` | members see these files in that folder |
| the FIT export's product string | it identifies us in files members send to Garmin or Strava |
| the CSV source label | shown in "Import from another app"; both sides moved together so a round trip still recognises itself |
| the Nominatim `User-Agent` | the service asks callers to identify themselves; it must be us, not upstream |
| `opengym.ch` in the printed-plan footer | it is printed on a member's plan |

## Three consequences that were not string swaps

- **The update check** asked GitHub for openGym's latest release. Left alone, a member
  tapping "check for updates" in a rebranded app would have been offered openGym's APK.
  It now reads `links.updateRepo` from the brand config.
- **The source-code link.** The AGPL obliges us to offer members the source of the version
  they are running, and that link is how. It reads `links.repo`. **That repository does not
  exist yet** — creating it is not optional once members are signing in.
- **The CSP hash.** `index.html`'s inline boot script is allowed by a sha256 pinned in
  `web/Dockerfile`. Editing the script's text changes the hash, and a stale one means the
  browser refuses the script: the app would load without its first-paint language and
  direction. The hash is recomputed from the patched file. Upstream's own test caught this.

## A note on the tests

Renaming user-visible copy makes tests that assert that copy wrong, so they move with it —
98 expectations across 41 files, rewritten by `patch-test-copy.py` with the same
distinction: the brand standing on its own is replaced, `opengym-state.json` and
`DuarteSantos8/openGym` are not.

One test needed care rather than a rule. `api.test.js` keeps a locale key as the English
source string *and* compares it against rendered output. The key has to stay; the
comparison has to be branded. Both, explicitly.
