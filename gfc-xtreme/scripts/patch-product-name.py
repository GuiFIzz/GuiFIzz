#!/usr/bin/env python3
"""Replace the product name throughout the UI, without breaking anything that is a key.

"openGym" appears about 1,470 times in the frontend. A find-and-replace over all of them
would be wrong in two directions at once:

  * the 1,224 in the locale packs are inside TRANSLATIONS whose KEYS are the English
    source strings -- rewrite the key and the pack stops matching, rewrite only the value
    and the next upstream update brings the old name back in every new string;
  * about a hundred are not the brand at all. `opengym-state.json`, `opengym-device-id`,
    `opengym-media-v1`, `Documents/openGym`, `opengym:back-preview` are storage keys,
    cache names, backup paths and event names. Renaming them orphans members' data,
    caches and automatic backups.

So the brand is substituted at the single point every translated string passes through --
t() and tn() in lib/i18n-core.js -- from one constant. Every language is covered, the keys
are untouched, and a string upstream adds next month is rebranded the day it arrives.

That leaves the places that print the name OUTSIDE t(). They are listed one by one below,
each replaced deliberately, because each needed a decision about whether it is the brand or
an identifier. Anything not listed is left exactly as upstream wrote it.
"""
import re
import sys
from pathlib import Path

# ---------------------------------------------------------------- the chokepoint --
I18N_IMPORT_ANCHOR = "import { INSTR_LANGS, EXERCISE_NAME_LANGS } from './catalogue-langs.js'"

BRAND_HELPER = '''
/* ------------------------------------------------------------------- branding --
   openGym's source strings, and the nineteen locale packs keyed off them, spell the
   product "openGym". Substituting here rebrands every one of them, in every language,
   from a single constant -- and keeps doing it for strings upstream adds later.

   The KEY is never touched, only the resolved value, so a pack still matches its
   entries after an upstream update. The swap runs BEFORE {0} interpolation so that a
   member's own routine or exercise name, passed in as an argument, is never rewritten.
   The includes() guard keeps the common case (a string without the name, which is
   almost all of them) to one scan with no allocation. */
const UPSTREAM_NAME = 'openGym'
const brandName = v =>
  typeof v === 'string' && v.includes(UPSTREAM_NAME) ? v.replaceAll(UPSTREAM_NAME, PRODUCT_NAME) : v
'''

T_OLD = """  for (let i = 0; i < args.length; i++) v = v.replaceAll('{' + i + '}', args[i])
  return v
}

/* ------------------------------------------------------------------ plurals --"""
T_NEW = """  v = brandName(v)
  for (let i = 0; i < args.length; i++) v = v.replaceAll('{' + i + '}', args[i])
  return v
}

/* ------------------------------------------------------------------ plurals --"""

# tn() has a fast path that returns without going through t(), so it needs the swap too.
TN_OLD = """    if (form) {
      let v = form
      const args = [n, ...rest]"""
TN_NEW = """    if (form) {
      let v = brandName(form)
      const args = [n, ...rest]"""


def patch_i18n(path: Path):
    src = path.read_text(encoding='utf-8')
    if 'brandName' in src:
        return False
    for old in (I18N_IMPORT_ANCHOR, T_OLD, TN_OLD):
        if src.count(old) != 1:
            sys.exit(f"patch-product-name: expected 1 occurrence in {path.name}:\n  {old[:90]}")
    src = src.replace(I18N_IMPORT_ANCHOR,
                      I18N_IMPORT_ANCHOR + "\nimport { PRODUCT_NAME } from './brand.js'" + BRAND_HELPER, 1)
    src = src.replace(T_OLD, T_NEW, 1).replace(TN_OLD, TN_NEW, 1)
    path.write_text(src, encoding='utf-8')
    return True


# ------------------------------------------------- the name outside t(), one by one --
# (file, old, new, why). Each must match exactly once.
SITES = [
    # The wordmark on the sign-in and onboarding screens.
    ('views/Login.jsx',
     ">openGym</h1>", ">{PRODUCT_NAME}</h1>",
     'sign-in wordmark'),
    ('views/MobileOnboarding.jsx',
     ">openGym</h1>", ">{PRODUCT_NAME}</h1>",
     'onboarding wordmark'),

    # The version line at the foot of Settings.
    ('views/Settings.jsx',
     '<div className="dim small sp-version">openGym v{__APP_VERSION__}</div>',
     '<div className="dim small sp-version">{PRODUCT_NAME} v{__APP_VERSION__}</div>',
     'Settings version line'),

    # The masthead of a printed plan, and the default filename of the print job.
    ('lib/print-doc.js',
     "<span>openGym</span>", "<span>${esc(PRODUCT_NAME)}</span>",
     'printed plan masthead'),
    ('lib/print-doc.js',
     "printHtml(html, name || 'openGym', printOptions())",
     "printHtml(html, name || PRODUCT_NAME, printOptions())",
     'print job name'),

    # The wordmark burned into the shareable workout card -- the one piece of branding
    # that leaves the app and lands in somebody else's feed.
    ('lib/workout-card.js',
     "text: 'openGym', x: start", "text: PRODUCT_NAME, x: start",
     'shared workout card wordmark'),

    # The fallback title when a workout image is shared.
    ('sheets.jsx',
     "shareImage(img.blob, name, w.name || 'openGym')",
     "shareImage(img.blob, name, w.name || PRODUCT_NAME)",
     'shared image title'),

    # The README written into a backup .zip, which a member reads months later.
    ('lib/backup-media.js',
     "const README = `openGym backup with photos and videos",
     "const README = `${PRODUCT_NAME} backup with photos and videos",
     'backup README heading'),
    ('lib/backup-media.js',
     "To bring it back: openGym -> Settings",
     "To bring it back: ${PRODUCT_NAME} -> Settings",
     'backup README instructions'),

    # Console diagnostics -- developer-facing, but it should say whose app crashed.
    ('components/ErrorBoundary.jsx',
     "console.error('openGym render error:', err)",
     "console.error(PRODUCT_NAME + ' render error:', err)",
     'crash log prefix'),
    # These are the one set of machine identifiers a member actually reads: they
    # browse to the folder, and the UI names it in its own copy. Leaving them as
    # "openGym" while the text above them says GFCXtremeFit would make the app lie
    # about where it put their data. Nothing else named opengym-* is renamed --
    # cache names, event names, state files and Health Connect record ids are never
    # read as a brand and renaming them orphans data for no gain.
    ('lib/mobile.js',
     "export const AUTO_BACKUP_DIR = 'openGym'",
     "export const AUTO_BACKUP_DIR = PRODUCT_NAME",
     'auto-backup folder'),
    ('lib/mobile.js',
     "const AUTO_BACKUP_NAME = /^opengym-backup-\\d{4}-\\d{2}-\\d{2}(-[2-9])?\\.json$/",
     "const AUTO_BACKUP_NAME = /^{slug}-backup-\\d{{4}}-\\d{{2}}-\\d{{2}}(-[2-9])?\\.json$/",
     'auto-backup filename pattern'),
    ('lib/mobile.js',
     "const n = `opengym-backup-${day}${suffix}.json`",
     "const n = `${FILE_SLUG}-backup-${day}${suffix}.json`",
     'auto-backup filename (rotation)'),
    ('lib/mobile.js',
     "const name = `opengym-backup-${day}.json`",
     "const name = `${FILE_SLUG}-backup-${day}.json`",
     'auto-backup filename (folder plugin)'),
    ('lib/mobile.js',
     "export const BACKUP_FOLDER_FILE = 'opengym-backup-folder.json'",
     "export const BACKUP_FOLDER_FILE = FILE_SLUG + '-backup-folder.json'",
     'chosen-folder record'),
    ('views/Settings.jsx',
     "const name = 'opengym-backup-' + todayISO() + '.json'",
     "const name = FILE_SLUG + '-backup-' + todayISO() + '.json'",
     'exported backup filename (JSON)'),
    ('views/Settings.jsx',
     "const name = 'opengym-backup-' + todayISO() + '.zip'",
     "const name = FILE_SLUG + '-backup-' + todayISO() + '.zip'",
     'exported backup filename (zip)'),
    ('lib/backup-media.js',
     "export const BACKUP_JSON = 'opengym-backup.json'",
     "export const BACKUP_JSON = FILE_SLUG + '-backup.json'",
     'filename inside the backup zip'),
    ('lib/backup-media.js',
     "opengym-backup.json  your data - the same file",
     "${BACKUP_JSON}  your data - the same file",
     'backup README file list'),
    ('components/BackupFolderRow.jsx',
     "const DEFAULT_FOLDER = 'Documents/openGym'",
     "const DEFAULT_FOLDER = 'Documents/' + PRODUCT_NAME",
     'default backup folder shown in Settings'),

    # ---- the name as it leaves the app ---------------------------------------
    # Written into exported FIT files as the producing product, read by Garmin,
    # Strava and anything else a member sends a workout to. 16-byte field.
    ('lib/fit-export.js',
     "[27, 'string', 'openGym', 16],", "[27, 'string', PRODUCT_NAME, 16],",
     'FIT export product name'),

    # The label the importer gives our own CSV, shown in "Import from another app".
    # Both sides move together, so a round trip still recognises itself.
    ('lib/import-csv.js',
     "if (h.includes('exercise id') && h.includes('set type')) return 'openGym'",
     "if (h.includes('exercise id') && h.includes('set type')) return PRODUCT_NAME",
     'CSV source label (detect)'),
    ('lib/import-csv.js',
     "const own = source === 'openGym'", "const own = source === PRODUCT_NAME",
     'CSV source label (read)'),

    # Nominatim asks for an app name and a contact URL in the User-Agent, and refuses
    # traffic that does not identify itself. It must be ours, not upstream's.
    ('views/GymReminder.jsx',
     "const USER_AGENT = 'openGym/' + (typeof __APP_VERSION__ === 'string' ? __APP_VERSION__ : 'dev') + ' (gym reminder; +https://opengym.ch)'",
     "const USER_AGENT = PRODUCT_NAME + '/' + (typeof __APP_VERSION__ === 'string' ? __APP_VERSION__ : 'dev') + ' (gym reminder; +' + SITE + ')'",
     'Nominatim User-Agent'),

    # The domain printed in the footer of a member's plan, and on the last page.
    ('lib/print-doc.js',
     '@bottom-left { content: "opengym.ch";',
     '@bottom-left { content: "${SITE_HOST}";',
     'printed plan footer domain'),
    ('lib/print-doc.js',
     "${esc(t('Made with openGym'))} · opengym.ch",
     "${esc(t('Made with openGym'))} · ${SITE_HOST}",
     'printed plan end line'),
    ('lib/print-doc.js',
     "return { paper: paperFor(locale), footer: { left: 'opengym.ch',",
     "return { paper: paperFor(locale), footer: { left: SITE_HOST,",
     'print footer (native)'),
]


# Files that need FILE_SLUG too (or instead).
SLUG_IMPORTS = {
    'lib/mobile.js':        './brand.js',
    'views/Settings.jsx':   '../lib/brand.js',
    'lib/backup-media.js':  './brand.js',
}

# Files needing PRODUCT_NAME beyond the SITES list's own imports.
MORE_IMPORTS = {
    'lib/fit-export.js':      './brand.js',
    'lib/import-csv.js':      './brand.js',
    'views/GymReminder.jsx':  '../lib/brand.js',
}
IMPORTS = {
    'views/Login.jsx':            ("import { t } from '../lib/i18n.js'", "../lib/brand.js"),
    'views/MobileOnboarding.jsx': (None, "../lib/brand.js"),
    'views/Settings.jsx':         (None, "../lib/brand.js"),
    'lib/print-doc.js':           (None, "./brand.js"),
    'lib/workout-card.js':        (None, "./brand.js"),
    'sheets.jsx':                 (None, "./lib/brand.js"),
    'lib/backup-media.js':        (None, "./brand.js"),
    'components/ErrorBoundary.jsx': (None, "../lib/brand.js"),
    'components/BackupFolderRow.jsx': (None, "../lib/brand.js"),
    'lib/mobile.js':              (None, "./brand.js"),
}


def add_import(path: Path, spec: str, names='PRODUCT_NAME'):
    """Add `names` to this file's import from the brand module, merging rather than
    adding a second import line for the same module."""
    src = path.read_text(encoding='utf-8')
    if names in src.split('\n\n')[0] and f"from '{spec}'" in src:
        return
    existing = f"from '{spec}'"
    for line in src.splitlines():
        if line.startswith('import {') and line.rstrip().endswith(existing):
            have = [n.strip() for n in line[line.index('{') + 1:line.index('}')].split(',')]
            if names in have:
                return
            merged = f"import {{ {', '.join(sorted(have + [names]))} }} {existing}"
            path.write_text(src.replace(line, merged, 1), encoding='utf-8')
            return
    line = f"import {{ {names} }} from '{spec}'\n"
    lines = src.splitlines(keepends=True)
    # Insert AFTER the last complete import statement. An import can span several lines
    # (`import {` … `} from '…'`), and inserting inside one splits it into a syntax error
    # the whole module tree then fails to load — which is exactly what happened once.
    # A line ending in `from '...'` or a bare `import '...'` terminates a statement.
    end_of_import = re.compile(r"""(from\s+['"][^'"]+['"];?|^\s*import\s+['"][^'"]+['"];?)\s*$""")
    last = -1
    for i, l in enumerate(lines[:80]):
        if end_of_import.search(l.rstrip()):
            last = i
    if last >= 0:
        lines.insert(last + 1, line)
    else:
        first_code = next((i for i, l in enumerate(lines)
                           if l.strip() and not l.lstrip().startswith(('//', '*', '/*'))), 0)
        lines.insert(first_code, line)
    path.write_text(''.join(lines), encoding='utf-8')


def patch_sites(root: Path, name='GFCXtremeFit', slug='gfcxtremefit'):
    """`new` may carry {slug} or {name}: upstream's Java-parity test reads
    AUTO_BACKUP_NAME as a literal regex, so the slug is written in rather than
    composed at runtime, and that test keeps doing its job."""
    done = []
    for rel, old, new, why in SITES:
        if '{slug}' in new or '{name}' in new:
            new = new.replace('{{', '\x00').replace('}}', '\x01')
            new = new.replace('{slug}', slug).replace('{name}', name)
            new = new.replace('\x00', '{').replace('\x01', '}')
        f = root / rel
        src = f.read_text(encoding='utf-8')
        if new in src:
            continue
        n = src.count(old)
        if n != 1:
            sys.exit(f"patch-product-name: expected 1 occurrence of\n  {old}\nin {rel}, found {n}")
        f.write_text(src.replace(old, new, 1), encoding='utf-8')
        done.append(why)
    for rel, (_, spec) in IMPORTS.items():
        add_import(root / rel, spec)
    for rel, spec in SLUG_IMPORTS.items():
        add_import(root / rel, spec, 'FILE_SLUG')
    for rel, spec in MORE_IMPORTS.items():
        add_import(root / rel, spec)
    add_import(root / 'views' / 'GymReminder.jsx', '../lib/brand.js', 'SITE')
    add_import(root / 'lib' / 'print-doc.js', './brand.js', 'SITE_HOST')
    return done


# ------------------------------------------ surfaces with no t() to go through --
# index.html runs before any JavaScript module loads, so its boot-failure text and its
# title cannot be translated or imported -- the name is written in at build time. The
# manifest is what the phone shows under the home-screen icon. The API has no i18n layer
# at all, and its push titles are the name a member sees on a locked phone.
def patch_static(repo: Path, name: str):
    done = []

    html = repo / 'frontend' / 'index.html'
    src = html.read_text(encoding='utf-8')
    if 'openGym' in src:
        src = src.replace('openGym', name)
        html.write_text(src, encoding='utf-8')
        done.append('index.html (title, home-screen name, boot errors)')

    man = repo / 'frontend' / 'public' / 'manifest.json'
    src = man.read_text(encoding='utf-8')
    if '"openGym"' in src:
        man.write_text(src.replace('"openGym"', f'"{name}"'), encoding='utf-8')
        done.append('manifest.json (PWA name)')

    # The push title a member reads on a locked phone. Taken from the environment rather
    # than compiled in: the API image is upstream's, and .env is where this deployment's
    # brand already lives (RP_NAME is the name shown in the Face ID prompt).
    push = repo / 'api' / 'push-messages.js'
    src = push.read_text(encoding='utf-8')
    if "BRAND_NAME" not in src:
        old_t = "return { title: 'openGym', body: copyFor(lang).testBody, tag: 'test' };"
        old_n = "const name = routine?.name || 'openGym';"
        if src.count(old_t) == 1 and src.count(old_n) == 1:
            decl = ("// The product name on a push notification. The API has no i18n layer, so it comes from\n"
                    "// the environment the rest of this deployment's branding already lives in.\n"
                    "const BRAND_NAME = process.env.BRAND_NAME || process.env.RP_NAME || 'openGym';\n")
            src = src.replace(old_t, "return { title: BRAND_NAME, body: copyFor(lang).testBody, tag: 'test' };", 1)
            src = src.replace(old_n, "const name = routine?.name || BRAND_NAME;", 1)
            lines = src.splitlines(keepends=True)
            first = next((i for i, l in enumerate(lines)
                          if l.strip() and not l.lstrip().startswith(('//', '*', '/*'))), 0)
            lines.insert(first, decl)
            push.write_text(''.join(lines), encoding='utf-8')
            done.append('api push notification title (via BRAND_NAME)')
    return done


def main(frontend_src, product_name=None, repo=None, slug=None):
    root = Path(frontend_src)
    changed = patch_i18n(root / 'lib' / 'i18n-core.js')
    print(f"  i18n-core.js: {'t() and tn() now rebrand every string' if changed else 'already patched'}")
    done = patch_sites(root, product_name or 'GFCXtremeFit', slug or 'gfcxtremefit')
    print(f"  outside t(): {len(done)} site(s) — {', '.join(done) if done else 'already patched'}")
    if product_name and repo:
        st = patch_static(Path(repo), product_name)
        print(f"  no-t() surfaces: {len(st)} — {', '.join(st) if st else 'already patched'}")


if __name__ == '__main__':
    main(sys.argv[1], *sys.argv[2:5])
