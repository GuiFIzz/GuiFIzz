// Verifies the colour pairs in brand.config.json actually meet WCAG, and that the
// contrastOn* figures recorded in the config are true. Run it in CI: a brand tweak that
// quietly makes the app unreadable should fail the build, not ship.
import { readFileSync } from 'node:fs'
import { fileURLToPath } from 'node:url'
import { dirname, join } from 'node:path'

const here = dirname(fileURLToPath(import.meta.url))
const brand = JSON.parse(readFileSync(join(here, '../brand/brand.config.json'), 'utf8'))
const C = brand.color

const lum = hex => {
  const v = [1, 3, 5].map(i => parseInt(hex.slice(i, i + 2), 16) / 255)
    .map(x => (x <= 0.03928 ? x / 12.92 : ((x + 0.055) / 1.055) ** 2.4))
  return 0.2126 * v[0] + 0.7152 * v[1] + 0.0722 * v[2]
}
const ratio = (a, b) => {
  const [x, y] = [lum(a), lum(b)].sort((p, q) => q - p)
  return (x + 0.05) / (y + 0.05)
}

// [label, foreground, background, minimum]. 4.5 is AA body text; 3.0 is AA large text
// and non-text UI, which is what an accent on a surface has to clear.
const checks = [
  ['accent on background',        C.accent.hex,   C.ink.hex,      3.0],
  ['accent on surface',           C.accent.hex,   C.surface.hex,  3.0],
  ['label on background',         C.label.hex,    C.ink.hex,      4.5],
  ['label on surface',            C.label.hex,    C.surface.hex,  4.5],
  ['secondary label on surface',  C.label2.hex,   C.surface.hex,  4.5],
  ['button text on accent',       C.onAccent.hex, C.accent.hex,   4.5]
]

let bad = 0
console.log('GFC Xtreme — contrast\n')
for (const [name, fg, bg, min] of checks) {
  const r = ratio(fg, bg)
  const ok = r >= min
  if (!ok) bad++
  console.log(`  ${ok ? 'PASS' : 'FAIL'}  ${name.padEnd(28)} ${fg} on ${bg}  ${r.toFixed(2)} (needs ${min.toFixed(1)})`)
}

// The config records measured figures; drift between them and reality means someone
// edited a colour and left the note behind.
const recorded = [
  ['color.accent.contrastOnBg',        C.accent.contrastOnBg,       ratio(C.accent.hex, C.ink.hex)],
  ['color.label.contrastOnBg',         C.label.contrastOnBg,        ratio(C.label.hex, C.ink.hex)],
  ['color.onAccent.contrastOnAccent',  C.onAccent.contrastOnAccent, ratio(C.onAccent.hex, C.accent.hex)]
]
for (const [key, claimed, actual] of recorded) {
  if (claimed === undefined) continue
  if (Math.abs(claimed - actual) > 0.05) {
    bad++
    console.log(`  FAIL  ${key} says ${claimed}, actual ${actual.toFixed(2)} — update the config`)
  }
}

// White on this accent is the classic mistake: it looks right and measures 3.04.
const whiteOnAccent = ratio('#FFFFFF', C.accent.hex)
console.log(`\n  note  white on the accent is ${whiteOnAccent.toFixed(2)} — below 4.5, which is why onAccent is ${C.onAccent.hex}.`)

console.log(bad ? `\n${bad} problem(s).` : '\nAll pairs pass.')
process.exit(bad ? 1 : 0)
