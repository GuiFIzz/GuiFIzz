#!/usr/bin/env python3
"""The three rename consequences that are not string swaps.

1. LINKS that pointed at upstream. The in-app update check asked GitHub for openGym's
   latest release -- left alone, a member tapping "check for updates" in a rebranded
   app would be offered openGym's APK. The source-code link matters more than it looks:
   the AGPL obliges us to offer members the source of the version they are running, and
   that link is how. Both come from brand.config.json, and while a URL is null the
   feature is switched off rather than left pointing at someone else's project.

2. JAVA/JS PARITY. The Android backup plugin carries its own copy of the backup-filename
   pattern, and upstream has a test asserting the two agree. Renaming the files in JS
   alone would have let the native pruner stop recognising -- and so stop tidying -- the
   very files the app writes.

3. THE CSP HASH. index.html's inline boot script is allowed by a sha256 pinned in
   web/Dockerfile. Editing that script's text changes the hash, and a stale one means the
   browser refuses the script: the app loads without its first-paint language and
   direction. The hash is recomputed from the file as patched.

One deliberate non-change: the sentence "Media licensed for use in openGym only" in
Settings. That is a quotation of the media licence's own wording (agreement 8c, which is
why upstream marks it as not translated). It describes the agreement openGym holds with
gymvisual.com, so rewriting it to say our name would misstate a licence we do not yet
have. It stays, and the NOTICE.md link beside it keeps pointing at upstream's notice,
which is the document it refers to.
"""
import base64
import hashlib
import json
import re
import sys
from pathlib import Path


# api.test.js keeps a locale KEY as the English source string -- it looks the German
# translation up by it -- while also comparing it against rendered output, which IS
# rebranded. The key must stay; the two comparisons get the brand applied.
API_TEST = (
    ("  afterEach(() => { _setLangState('en', {}, null, null); vi.unstubAllGlobals() })",
     "  // KEY stays the English source string because `de[KEY]` looks the pack up by it;\n"
     "  // what it is compared against went through t(), so it carries the product name.\n"
     "  const branded = v => v.replaceAll('openGym', PRODUCT_NAME)\n"
     "  afterEach(() => { _setLangState('en', {}, null, null); vi.unstubAllGlobals() })"),
    ("expect(e.message).toBe(de[KEY].replace('{0}', 'http://localhost:8080'))",
     "expect(e.message).toBe(branded(de[KEY]).replace('{0}', 'http://localhost:8080'))"),
    ("expect(passkeyError(e, 'x')).toBe(KEY.replace('{0}', 'https://gym.example.com'))",
     "expect(passkeyError(e, 'x')).toBe(branded(KEY).replace('{0}', 'https://gym.example.com'))"),
)


def patch_api_test(path: Path, name: str):
    if not path.exists():
        return []
    src = path.read_text(encoding='utf-8')
    if 'const branded =' in src:
        return []
    # the patcher that runs before this one rebrands the KEY literal; put it back
    src = src.replace(f'If you opened {name} at another address', 'If you opened openGym at another address')
    for old, new in API_TEST:
        if src.count(old) != 1:
            sys.exit(f"patch-product-name: api.test.js anchor missing:\n  {old[:80]}")
        src = src.replace(old, new, 1)
    # Anchor on the module, not on the order of the named imports: upstream lists them
    # alphabetically here and that is not something to depend on.
    if "PRODUCT_NAME } from './brand.js'" not in src:
        m = re.search(r"^import .*from 'vitest'$", src, re.M)
        if not m:
            sys.exit("patch-links-and-parity: no vitest import to anchor to in api.test.js")
        src = src[:m.end()] + "\nimport { PRODUCT_NAME } from './brand.js'" + src[m.end():]
    path.write_text(src, encoding='utf-8')
    return ['api.test.js locale key kept, comparisons branded']


def patch_links(src_root: Path, cfg: dict):
    links = cfg.get('links') or {}
    done = []

    # ---- the in-app update check ------------------------------------------------
    up = src_root / 'lib' / 'update.js'
    s = up.read_text(encoding='utf-8')
    old = "const REPO = 'DuarteSantos8/openGym'"
    if old in s:
        new = ("// Set from brand.config.json. null switches the update check off, which is right\n"
               "// for a fork with no releases of its own -- upstream's would be the wrong build.\n"
               "const REPO = UPDATE_REPO")
        s = s.replace(old, new, 1)
        if "UPDATE_REPO } from" not in s:
            s = s.replace("import { MOBILE } from './mobile.js'",
                          "import { MOBILE } from './mobile.js'\nimport { UPDATE_REPO } from './brand.js'", 1)
        up.write_text(s, encoding='utf-8')
        done.append(f"update check → {links.get('updateRepo') or 'off (no repo set)'}")

    # ---- the source-code link the AGPL requires ---------------------------------
    st = src_root / 'views' / 'Settings.jsx'
    s = st.read_text(encoding='utf-8')
    old = '<a href="https://github.com/DuarteSantos8/openGym" target="_blank" rel="noopener">{t(\'Source code\')}</a><br />'
    if old in s:
        new = ("{SOURCE_REPO && <><a href={'https://github.com/' + SOURCE_REPO} target=\"_blank\" "
               "rel=\"noopener\">{t('Source code')}</a><br /></>}")
        s = s.replace(old, new, 1)
        if "SOURCE_REPO" not in s.split('\n\n')[0]:
            s = re.sub(r"(import \{ )(FILE_SLUG, PRODUCT_NAME)( \} from '\.\./lib/brand\.js')",
                       r"\1FILE_SLUG, PRODUCT_NAME, SOURCE_REPO\3", s, count=1)
        st.write_text(s, encoding='utf-8')
        done.append('source-code link → brand config' + ('' if links.get('repo') else ' (hidden: repo not set)'))
    return done


def patch_java_parity(repo: Path, slug: str):
    j = repo / 'frontend/android/app/src/main/java/ch/duartesantos/opengym/BackupFolderPlugin.java'
    if not j.exists():
        return []
    s = s0 = j.read_text(encoding='utf-8')
    s = s.replace('Pattern.compile("opengym-backup-', f'Pattern.compile("{slug}-backup-')
    s = s.replace('"opengym-backup-2026-10-15.json"', f'"{slug}-backup-2026-10-15.json"')
    if s == s0:
        return []
    j.write_text(s, encoding='utf-8')
    # The package path stays ch.duartesantos.opengym: renaming it is an Android package
    # rename, which means a new signing identity and a new Play listing, not a brand edit.
    return ['Android backup pattern (JS/Java parity)']


def patch_native_names(repo: Path, name: str):
    """The name members read under the app icon on their home screen.

    Only the DISPLAY names. The Android applicationId and the iOS bundle id stay
    ch.duartesantos.opengym: those are the app's identity to the store and to the
    signing key, and to Health Connect, which files its records against them.
    Changing them is a new listing and a new signing identity, not a brand edit --
    it has to be a deliberate decision before first publish, not a side effect of
    a rename.
    """
    done = []
    cap = repo / 'frontend' / 'capacitor.config.json'
    if cap.exists():
        s = cap.read_text(encoding='utf-8')
        if '"appName": "openGym"' in s:
            cap.write_text(s.replace('"appName": "openGym"', f'"appName": "{name}"', 1), encoding='utf-8')
            done.append('Capacitor appName')
    plist = repo / 'frontend/ios/App/App/Info.plist'
    if plist.exists():
        s = plist.read_text(encoding='utf-8')
        old = "<key>CFBundleDisplayName</key>\n\t<string>openGym</string>"
        if old in s:
            plist.write_text(s.replace(old, f"<key>CFBundleDisplayName</key>\n\t<string>{name}</string>", 1), encoding='utf-8')
            done.append('iOS home-screen name')
    return done


def patch_csp(repo: Path):
    html = (repo / 'frontend/index.html').read_text(encoding='utf-8')
    docker = repo / 'web/Dockerfile'
    s = s0 = docker.read_text(encoding='utf-8')
    inline = re.findall(r'<script(?![^>]*\bsrc=)[^>]*>([\s\S]*?)</script>', html)
    changed = []
    for body in inline:
        want = "'sha256-" + base64.b64encode(hashlib.sha256(body.encode()).digest()).decode() + "'"
        if want in s:
            continue
        # replace whatever sha256 is currently pinned for script-src
        stale = re.findall(r"'sha256-[A-Za-z0-9+/=]+'", s)
        if len(stale) == 1:
            s = s.replace(stale[0], want, 1)
            changed.append(f"{stale[0][:20]}… → {want[:20]}…")
        else:
            sys.exit(f"patch-links-and-parity: expected 1 pinned sha256 in web/Dockerfile, found {len(stale)}")
    if s != s0:
        docker.write_text(s, encoding='utf-8')
    return ['CSP hash for the inline boot script'] if changed else []


def main(repo, cfg_path):
    repo = Path(repo)
    cfg = json.loads(Path(cfg_path).read_text(encoding='utf-8'))
    done = patch_api_test(repo / 'frontend/src/lib/api.test.js', cfg['identity']['productName'])
    done += patch_links(repo / 'frontend' / 'src', cfg)
    done += patch_java_parity(repo, cfg['identity']['fileSlug'])
    done += patch_native_names(repo, cfg['identity']['productName'])
    done += patch_csp(repo)
    print(f"  links & parity: {len(done)} — {', '.join(done) if done else 'already patched'}")


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
