#!/usr/bin/env python3
"""Point test expectations at the new product name, without touching identifiers.

Thirty-six assertions across nineteen files check UI copy that spells the product
"openGym". The copy legitimately changed, so the expectations are wrong, not the app --
but a blanket replace over the test files would also rewrite `opengym-state.json`,
`opengym-media-v1` and `opengym:back-preview`, which are not the brand.

The brand is always the camel-case token `openGym` standing on its own. The identifiers
are either all-lowercase (`opengym-...`) or have the name glued to a path or a word
(`Documents/openGym`, `openGymSheet`, `openGym-server`). The pattern below matches the
first and never the second -- except `Documents/openGym`, which IS renamed, because the
app now really does write there (see patch-product-name.py).

Run after patch-product-name.py. Idempotent: the name it writes contains no `openGym`.
"""
import re
import sys
from pathlib import Path

# The brand standing on its own: not glued to a word, not part of a path or a package
# (`DuarteSantos8/openGym`, `openGymSheet`, `openGym-server`), and not a hostname
# (`openGym.ch`). A trailing full stop at the end of a sentence IS allowed through, which
# is the distinction `\.[A-Za-z]` draws -- getting that wrong left half of one message
# renamed and half not.
TOKEN = re.compile(r'(?<![\w.:_/-])openGym(?![\w-])(?!\.[A-Za-z])')
# The one path that does move with the brand: the app really writes there now.
# Tests spell it both ways (`Documents/openGym` as the app shows it, `DOCUMENTS/openGym`
# as the Capacitor Filesystem mock keys it), so the folder part is matched case-insensitively.
DOCS_FOLDER = re.compile(r'(?i:documents)/openGym(?![\w.-])')


REPO = HOST = ''


def patch(path: Path, name: str, slug: str) -> int:
    src = original = path.read_text(encoding='utf-8')
    src = DOCS_FOLDER.sub(lambda m: m.group(0)[:m.group(0).index('/') + 1] + name, src)
    src = TOKEN.sub(name, src)
    # the backup files members see, renamed with the brand
    src = src.replace('opengym-backup', f'{slug}-backup')
    # Upstream's own repo and domain, where a test asserts the link or the User-Agent.
    if REPO:
        src = src.replace('DuarteSantos8/openGym', REPO)
    if HOST:
        src = src.replace('opengym.ch', HOST).replace('opengym\\.ch', HOST.replace('.', '\\.'))
    if src == original:
        return 0
    path.write_text(src, encoding='utf-8')
    return len(TOKEN.findall(original)) + len(DOCS_FOLDER.findall(original))


def main(frontend_src, name, slug, repo='', host=''):
    global REPO, HOST
    REPO, HOST = repo, host
    root = Path(frontend_src)
    files = [f for f in root.rglob('*')
             if f.suffix in ('.js', '.jsx') and '.test.' in f.name]
    touched, total = 0, 0
    for f in files:
        n = patch(f, name, slug)
        if n:
            touched += 1
            total += n
    print(f"  tests: {total} expectation(s) across {touched} file(s) now say {name}")


if __name__ == '__main__':
    main(*sys.argv[1:6])
