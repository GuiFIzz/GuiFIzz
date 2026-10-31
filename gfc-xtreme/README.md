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

Then the two hand edits and the `.env` line in `docs/PATCH_POINTS.md`, and openGym's
own `docker compose up`.

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

- Upstream's full frontend suite: **6,540 tests**. The overlay broke two, both
  legitimately; both are fixed, and `color-mix-fallback.test.js` caught a real Safari
  bug in our own CSS before it shipped.
- Total upstream diff: **six files, about fifteen lines.**

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
