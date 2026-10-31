#!/usr/bin/env bash
# Applies the GFC Xtreme brand overlay to a checkout of upstream openGym.
#
#   ./gfc-xtreme/scripts/apply-overlay.sh ../openGym
#
# Every edit is anchored to an exact line of upstream source. If upstream has changed
# that line the script stops and names the anchor rather than half-applying — a loud
# failure on a known file beats a silent miss discovered in production. Re-running is
# safe: each step checks whether it has already been applied.
set -euo pipefail

UP="${1:-}"
[ -n "$UP" ] || { echo "usage: $0 <path-to-openGym-checkout>" >&2; exit 2; }
[ -d "$UP/frontend/src" ] || { echo "not an openGym checkout: $UP" >&2; exit 2; }

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ok=0; skip=0

anchor() { # file, literal string that must exist
  grep -qF "$2" "$1" || { echo "ANCHOR LOST in $1:"; echo "   $2"; echo "upstream changed — re-check this patch point before continuing."; exit 1; }
}
done_already() { grep -qF "$2" "$1"; }

# 1 ── register "gfc" as an accent preset -------------------------------------
F="$UP/frontend/src/lib/format.js"
if done_already "$F" "gfc:"; then skip=$((skip+1)); else
  anchor "$F" "export const ACCENTS = {"
  anchor "$F" "export const ACCENT_INK = {"
  sed -i "s/export const ACCENTS = { lime:/export const ACCENTS = { gfc: '#FC6228', lime:/" "$F"
  sed -i "s/export const ACCENT_INK = { lime:/export const ACCENT_INK = { gfc: '#000000', lime:/" "$F"
  ok=$((ok+1))
fi

# 2 ── make it the default ----------------------------------------------------
F="$UP/frontend/src/lib/accent.js"
if done_already "$F" "DEFAULT_ACCENT = 'gfc'"; then skip=$((skip+1)); else
  anchor "$F" "export const DEFAULT_ACCENT = 'lime'"
  sed -i "s/export const DEFAULT_ACCENT = 'lime'/export const DEFAULT_ACCENT = 'gfc'/" "$F"
  ok=$((ok+1))
fi

# 3 ── brand sheet after the design system, so it can override tokens ---------
F="$UP/frontend/src/main.jsx"
if done_already "$F" "gfc-brand.css"; then skip=$((skip+1)); else
  anchor "$F" "index.css"
  sed -i "0,/import '.\/index.css'/s//import '.\/index.css'\nimport '.\/gfc-brand.css'/" "$F"
  grep -qF "gfc-brand.css" "$F" || { echo "could not add the brand import to main.jsx" >&2; exit 1; }
  ok=$((ok+1))
fi

# 4 ── the generated sheet and the assets -------------------------------------
cp "$HERE/overlay/frontend/src/gfc-brand.css" "$UP/frontend/src/gfc-brand.css"
mkdir -p "$UP/frontend/public/brand"
cp "$HERE/brand/assets/gfc-logo-header.png"    "$UP/frontend/public/brand/"
cp "$HERE/brand/assets/gfc-logo-header@2x.png" "$UP/frontend/public/brand/"
cp "$HERE/brand/assets/gfc-logo-header@3x.png" "$UP/frontend/public/brand/"
cp "$HERE/brand/assets/gfc-logo.png"           "$UP/frontend/public/brand/"
cp "$HERE/brand/assets/gym-bg.jpg"             "$UP/frontend/public/brand/"
cp "$HERE/brand/assets/gym-bg-480.jpg"         "$UP/frontend/public/brand/"

# 5 ── brand attribute on <html> so the surface overrides apply ---------------
F="$UP/frontend/index.html"
if done_already "$F" 'data-brand="gfc"'; then skip=$((skip+1)); else
  anchor "$F" "<html"
  sed -i '0,/<html/s//<html data-brand="gfc"/' "$F"
  ok=$((ok+1))
fi

# 6 ── upstream's accent tests assert the default as the literal 'lime' -------
#      Rather than swap one literal for another, the assertions are pointed at the
#      DEFAULT_ACCENT constant, so this is the last time a rebrand touches a test.
#      Only the assertions that mean "the default" are changed; 'lime' as an ordinary
#      preset value elsewhere in the file is left exactly as it is. Each replacement
#      must match exactly once or the script stops.
F="$UP/frontend/src/lib/accent.test.js"
if done_already "$F" "DEFAULT_ACCENT"; then skip=$((skip+1)); else
  python3 "$HERE/scripts/patch-accent-test.py" "$F"
  ok=$((ok+1))
fi

# 7 ── the new accent needs an accessible name, in every language ------------
F="$UP/frontend/src/lib/format.js"
if grep -qF "GFC Orange" "$F"; then skip=$((skip+1)); else
  python3 "$HERE/scripts/patch-accent-name.py" "$UP/frontend/src"
  ok=$((ok+1))
fi

echo "overlay applied: $ok change(s), $skip already in place"
echo
echo "Still to do by hand (they are component edits, not one-line anchors):"
echo "  frontend/src/App.jsx        render <img class=\"gfc-mark\"> — see docs/PATCH_POINTS.md"
echo "  frontend/src/views/Login.jsx add <div class=\"gfc-login-bg\"> and the login mark"
echo "  .env                        RP_NAME=\"GFC Xtreme\""
