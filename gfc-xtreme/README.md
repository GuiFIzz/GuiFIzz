# GFC Xtreme — brand overlay for openGym

The GFC Xtreme Fitness training app, built on [openGym](https://github.com/DuarteSantos8/openGym).

This directory is **not a fork**. It holds only what is ours — the brand, and
eventually the member gateway — and applies it to a clean checkout of upstream. The
21,000 files of openGym stay upstream, where they get maintained by someone else.

```
brand/
  brand.config.json     the single source of truth: colours, names, logo slots
  assets/               the logo (black keyed to transparent) and gym photography
overlay/
  frontend/src/gfc-brand.css      GENERATED — do not edit
  frontend/manifest.partial.json  GENERATED — do not edit
scripts/
  build-tokens.mjs      brand.config.json  ->  the generated files
  check-contrast.mjs    fails if a colour pair drops below WCAG
  apply-overlay.sh      applies everything to an openGym checkout
  patch-accent-test.py  }  called by apply-overlay.sh
  patch-accent-name.py  }
docs/
  PATCH_POINTS.md       every upstream line we touch, and why
```

## Changing the brand

Edit `brand/brand.config.json`. Nothing else.

```bash
node gfc-xtreme/scripts/check-contrast.mjs    # does it still pass WCAG?
node gfc-xtreme/scripts/build-tokens.mjs      # regenerate the CSS and manifest
```

New logo or new photography: drop the files into `brand/assets/` under the existing
names and rebuild. No code changes.

## Building the app

```bash
git clone https://github.com/DuarteSantos8/openGym.git
./gfc-xtreme/scripts/apply-overlay.sh ./openGym
```

That applies everything. The only step left is one line of configuration:

```bash
echo 'RP_NAME="GFCXtreme"' >> openGym/.env
```

Then openGym's own `docker compose up`.

## Taking upstream updates

```bash
cd openGym && git pull && cd ..
./gfc-xtreme/scripts/apply-overlay.sh ./openGym
cd openGym/frontend && npx vitest run
```

The script re-applies cleanly, skips what is already there, and **stops with the exact
anchor text if upstream has moved a line it patches**. A loud failure on a known file is
the point — the alternative is a half-applied brand discovered by a member.

## Verified

Applied to a clean upstream checkout, then both suites run in full:

```
frontend   Test Files  543 passed (543)
                Tests  6540 passed (6540)
api             tests  696   pass 693   fail 0   (3 skipped: root, midnight UTC)
```

Upstream's tests earned their keep. They caught, among others, a `color-mix()` with no
fallback that would have broken the sign-in card on Safari before 16.2; a stale CSP hash
that would have stopped the app's boot script running at all; and a backup-filename
pattern that had drifted out of step between the JavaScript and the Android plugin.

## Naming

`openGym` appears about 1,470 times in the frontend. The brand is swapped at the one
point every translated string passes through — `t()` and `tn()` in `lib/i18n-core.js` —
so one constant renames the app in all nineteen languages and keeps renaming strings
upstream adds later. The locale keys are untouched, so the packs still match.

Roughly a hundred of those occurrences are **not** the brand: cache names, state files,
event names, Health Connect record ids, the Android package. They keep upstream's
spelling, because renaming them orphans members' data and buys nothing. The exceptions
are the things members actually read — the backup folder and the files in it, the FIT
export's product string, the printed footer — which move with the brand.

`docs/PATCH_POINTS.md` lists every one of those decisions.

## Licence, and one thing to settle

openGym is **AGPL-3.0**. A rebranded fork is squarely allowed, provided it stays AGPL and
its source is offered to the people who use it over the network. That last clause is not
optional once members are signing in.

**The exercise animations are a separate matter.** `catalogue/media/` is licensed to
openGym by gymvisual.com and is *not* covered by the AGPL. Upstream's `NOTICE.md`:

> A non-commercial fork of openGym may keep the unmodified 180px media together with this
> notice. A commercial fork, or any other use, needs its own licence from gymvisual.com.

A paid membership makes this commercial. Either license the media from
[gymvisual.com](https://gymvisual.com/) or ship without those animations — the catalogue
text itself is openGym's own and is AGPL. The overlay does not vendor the media, which
keeps the decision open rather than making it by accident.
