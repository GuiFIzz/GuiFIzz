#!/usr/bin/env python3
"""Put the mark on screen: the corner logo, and the photograph behind the sign-in.

Three edits that were left by hand until now because they are JSX rather than
one-line anchors. They are small, they are stable, and leaving them manual meant
a fresh checkout was never actually branded until somebody remembered.

  App.jsx            the mark, fixed in the upper-left of the app chrome
  Login.jsx          the gym photograph behind sign-in, the mark in the corner,
                     and the stock icon-plus-wordmark head removed
  MobileOnboarding   the same head replaced by the logo itself

Why the head goes: upstream centres a dumbbell icon above an <h1> of the product
name. After the rename that <h1> reads GFCXtreme in plain text, so with the corner
mark the brand would appear twice on one screen -- and the logo IS the wordmark.
On onboarding there is no app chrome to hold a corner mark, so there the logo
takes the head's place rather than being dropped.
"""
import re
import sys
from pathlib import Path

MARK = ('<img className="gfc-mark" src="/brand/gfc-logo-header.png" '
        'srcSet="/brand/gfc-logo-header@2x.png 2x, /brand/gfc-logo-header@3x.png 3x" '
        'alt="{alt}" />')

HEAD_OLD = """  const head = <>
    <div style={{ fontSize: 54, display: 'flex', justifyContent: 'center', color: 'var(--acc)' }}><Icon name="dumbbell" /></div>
    <h1 style={{ fontSize: 34, fontWeight: 700, letterSpacing: '-.028em', margin: '10px 0 4px' }}>{PRODUCT_NAME}</h1>
  </>"""

APP_ANCHOR = """      {/* Outside #app: the view's fade-in animates a transform, and a fixed element inside it"""


def edit(path: Path, old: str, new: str, what: str):
    src = path.read_text(encoding='utf-8')
    if new.strip() and new.split('\n')[0].strip() in src:
        return None
    if src.count(old) != 1:
        sys.exit(f"patch-chrome: expected 1 occurrence in {path.name} for {what}:\n  {old.splitlines()[0][:90]}")
    path.write_text(src.replace(old, new, 1), encoding='utf-8')
    return what


def drop_unused(path: Path, names):
    """Removing the stock head orphans the imports it used. Vite does not mind, but a
    dead import is a lie about what a file depends on, and the next person greps for it.

    A symbol's own module path mentions it too (`import Icon from './Icon.jsx'`), so the
    count is taken with the import line itself excluded rather than over the whole file."""
    src = path.read_text(encoding='utf-8')
    lines = src.splitlines(keepends=True)
    keep = []
    removed = False
    for i, line in enumerate(lines):
        stripped = line.strip()
        drop = False
        if stripped.startswith('import ') and "from '" in stripped:
            for n in names:
                if not re.search(rf"import\s+(\{{\s*)?{re.escape(n)}\b", stripped):
                    continue
                rest = ''.join(lines[:i] + lines[i + 1:])
                if not re.search(rf"\b{re.escape(n)}\b", rest):
                    drop = True
                    break
        if drop:
            removed = True
        else:
            keep.append(line)
    if removed:
        path.write_text(''.join(keep), encoding='utf-8')
    return removed


def main(src_root, alt):
    root = Path(src_root)
    done = []

    # 1. the mark, outside #app so a page transition's transform does not carry it along --
    #    the same reason upstream gives for everything else that sits out here.
    app = root / 'App.jsx'
    mark = MARK.format(alt=alt)
    r = edit(app, APP_ANCHOR,
             f"      {mark}\n{APP_ANCHOR}", 'the mark in the app chrome')
    if r:
        done.append(r)

    # 2. sign-in: photograph behind, mark in the corner, stock head gone.
    login = root / 'views' / 'Login.jsx'
    src = login.read_text(encoding='utf-8')
    if 'gfc-login-bg' not in src:
        if src.count(HEAD_OLD) != 1:
            sys.exit('patch-chrome: Login.jsx head anchor missing')
        head_new = ('  // The mark sits in the corner (gfc-brand.css), so the stock icon-and-wordmark\n'
                    '  // head would put the brand on the screen twice.\n'
                    '  const head = <>\n'
                    '    <div className="gfc-login-bg" aria-hidden="true" />\n'
                    f'    {MARK.format(alt=alt).replace("gfc-mark", "gfc-mark gfc-mark--login", 1)}\n'
                    '  </>')
        login.write_text(src.replace(HEAD_OLD, head_new, 1), encoding='utf-8')
        done.append('the photograph and mark on sign-in')

    # 3. onboarding has no chrome, so the logo takes the head's place.
    onb = root / 'views' / 'MobileOnboarding.jsx'
    src = onb.read_text(encoding='utf-8')
    if 'gfc-onboard-logo' not in src:
        if src.count(HEAD_OLD) != 1:
            sys.exit('patch-chrome: MobileOnboarding.jsx head anchor missing')
        head_new = ('  const head = <>\n'
                    '    <img className="gfc-onboard-logo" src="/brand/gfc-logo-header@2x.png"\n'
                    f'         alt="{alt}" />\n'
                    '  </>')
        onb.write_text(src.replace(HEAD_OLD, head_new, 1), encoding='utf-8')
        done.append('the logo on onboarding')

    dropped = sum(drop_unused(root / 'views' / f, ('Icon', 'PRODUCT_NAME'))
                  for f in ('Login.jsx', 'MobileOnboarding.jsx'))
    if dropped:
        done.append(f'{dropped} file(s) tidied of imports the old head used')
    print(f"  chrome: {len(done)} — {', '.join(done) if done else 'already in place'}")


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
