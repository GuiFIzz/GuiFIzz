#!/usr/bin/env python3
"""Give the GFC accent a name, in ACCENT_NAMES and in every language pack.

openGym's format-names test requires two things of any new accent: a key in
ACCENT_NAMES, and a translation of that name in every locale pack -- the swatches
are read out by screen readers, and the keys ("gfc") are not words.

Rather than invent nineteen translations, each pack's name is built from the word
that pack already uses for 'Orange': German keeps 'GFC Orange', Portuguese becomes
'GFC Laranja', Arabic 'GFC <its own word>'. The brand itself is not translated.
A pack that somehow has no 'Orange' entry falls back to the English word, so the
test's "every pack names every accent" still holds.
"""
import re
import sys
from pathlib import Path

NAME_EN = 'GFC Orange'

def patch_format(path: Path):
    src = path.read_text(encoding='utf-8')
    # Match the entry itself, not a window after the declaration: ACCENTS is declared
    # right below ACCENT_NAMES and already carries a `gfc:` key, which a loose check reads
    # as "done" and silently skips the name. (It did exactly that once.)
    if f"gfc: '{NAME_EN}'" in src:
        return False
    old = "export const ACCENT_NAMES = { lime:"
    if src.count(old) != 1:
        sys.exit(f"patch-accent-name: ACCENT_NAMES anchor not found once in {path}")
    src = src.replace(old, f"export const ACCENT_NAMES = {{ gfc: '{NAME_EN}', lime:", 1)
    path.write_text(src, encoding='utf-8')
    return True

def patch_pack(path: Path):
    src = path.read_text(encoding='utf-8')
    if f"'{NAME_EN}'" in src:
        return None
    m = re.search(r"^(\s*)'Orange':\s*'((?:[^'\\]|\\.)*)',", src, re.M)
    if not m:
        # No 'Orange' entry: name it in English so the pack still answers for the accent.
        m_any = re.search(r"^(\s*)'[^']+':", src, re.M)
        if not m_any:
            sys.exit(f"patch-accent-name: {path.name} has no entries to anchor to")
        indent, word = m_any.group(1), 'Orange'
        line = f"{indent}'{NAME_EN}': 'GFC {word}',\n"
        src = src[:m_any.start()] + line + src[m_any.start():]
    else:
        indent, word = m.group(1), m.group(2)
        line = f"\n{indent}'{NAME_EN}': 'GFC {word}',"
        src = src[:m.end()] + line + src[m.end():]
    path.write_text(src, encoding='utf-8')
    return word

def main(frontend_src):
    root = Path(frontend_src)
    changed = patch_format(root / 'lib' / 'format.js')
    print(f"  format.js: ACCENT_NAMES {'gained gfc' if changed else 'already had gfc'}")
    done = []
    for pack in sorted((root / 'locales').glob('*.js')):
        word = patch_pack(pack)
        if word is not None:
            done.append(f"{pack.stem}={word}")
    print(f"  locales: {len(done)} pack(s) named the accent")
    if done:
        print("    " + ', '.join(done))

if __name__ == '__main__':
    main(sys.argv[1])
