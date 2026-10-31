#!/usr/bin/env python3
"""Point upstream's accent.test.js default-accent assertions at DEFAULT_ACCENT.

The file asserts the fallback accent as the bare string 'lime' in eight places. A
rebrand changes that fallback, so those assertions would fail. Swapping in 'gfc'
would only move the problem, so the constant is imported and asserted instead.

Every edit must match exactly once; anything else means upstream has moved and the
script stops without writing, so a silent partial patch is impossible. The other
occurrences of 'lime' in the file are an ordinary preset value and a comment about
an older app's behaviour -- both correct as they stand, both left alone.
"""
import sys

IMPORT_OLD = ("  customAccentVars, accentPair, applyAccent, applyTintFallback, THEMES, "
              "isGrey, inkOnBoth, mix, GREY_TEXT, GREY_GAP,")
IMPORT_NEW = IMPORT_OLD + " DEFAULT_ACCENT,"

ASSERTIONS = [
    "expect(sanitizeAccent({ accent: '\"><script>' }).accent).toBe('lime')",
    "expect(sanitizeAccent({ accent: 42 }).accent).toBe('lime')",
    "expect(accentKey({})).toBe('lime')",
    "expect(accentKey({ accent: 'mint' })).toBe('lime')",
    "expect(accentKey({ accent: 'toString' })).toBe('lime')",
    "expect(accentKey({ accent: 'custom' })).toBe('lime')",
    "expect(accentKey({ accent: 'custom', accentCustom: 'nope' })).toBe('lime')",
    "expect(el.dataset.accent).toBe('lime')",
    # The merge drops a malformed own colour, so this falls back to the default too.
    "expect(accentValue(out)).toBe('lime')",
]

# These read the default's *hex* through ACCENTS rather than its key, so the swap differs.
PAIR_ASSERTIONS = [
    "expect(accentPair('nonsense')).toEqual({ accent: ACCENTS.lime, ink: '#000000' })",
    "expect(accentPair(undefined)).toEqual({ accent: ACCENTS.lime, ink: '#000000' })",
]

def main(path):
    src = open(path, encoding='utf-8').read()
    edits = [(IMPORT_OLD, IMPORT_NEW)]
    edits += [(a, a.replace(".toBe('lime')", ".toBe(DEFAULT_ACCENT)")) for a in ASSERTIONS]
    # ink stays '#000000' only because the GFC accent measures black-on-accent; a brand whose
    # accent wanted white ink would have to change these two with it, which is why they are
    # listed separately rather than folded into a blanket replace.
    edits += [(a, a.replace("ACCENTS.lime", "ACCENTS[DEFAULT_ACCENT]")) for a in PAIR_ASSERTIONS]

    for old, _ in edits:
        n = src.count(old)
        if n != 1:
            sys.exit(f"patch-accent-test: expected 1 occurrence, found {n}:\n  {old}\n"
                     f"upstream changed -- re-check this patch point.")
    for old, new in edits:
        src = src.replace(old, new, 1)

    open(path, 'w', encoding='utf-8').write(src)
    print(f"  accent.test.js: {len(ASSERTIONS) + len(PAIR_ASSERTIONS)} assertions now read DEFAULT_ACCENT")

if __name__ == '__main__':
    main(sys.argv[1])
