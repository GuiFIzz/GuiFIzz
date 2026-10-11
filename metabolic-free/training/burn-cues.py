#!/usr/bin/env python
"""Burn the GFC Xtreme logo + a trainer cue caption into a workout clip.

One source clip -> one captioned output. Portrait 1080x1920 in, same out.
Text is rendered with Pillow (the Homebrew ffmpeg here has no drawtext).
"""
import json
import subprocess
import sys
import textwrap
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

SCRATCH = Path(__file__).parent
LOGO = SCRATCH / "logo_rgba.png"

BOLD = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
REG = "/System/Library/Fonts/Supplemental/Arial.ttf"

ACCENT = (242, 107, 42, 255)   # GFC orange
INK = (255, 255, 255, 255)
BODY = (232, 232, 232, 255)

W, H = 1080, 1920
MARGIN = 52
LOGO_W = 345
SCRIM_H = 560
TOP_SCRIM_H = 300


def wrap(draw, text, font, max_w):
    words, lines, cur = text.split(), [], ""
    for word in words:
        trial = f"{cur} {word}".strip()
        if draw.textlength(trial, font=font) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def build_overlay(name, variant, cue):
    """Return an RGBA overlay: logo top-left, caption bottom."""
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))

    # --- top scrim: keeps the logo legible over bright gym windows ---
    top = Image.new("RGBA", (W, TOP_SCRIM_H), (0, 0, 0, 0))
    td = ImageDraw.Draw(top)
    for y in range(TOP_SCRIM_H):
        a = int(165 * (1 - y / TOP_SCRIM_H) ** 1.6)
        td.line([(0, y), (W, y)], fill=(8, 8, 8, a))
    ov.alpha_composite(top, (0, 0))

    # --- bottom scrim: transparent -> near-black, so text stays readable ---
    scrim = Image.new("RGBA", (W, SCRIM_H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(scrim)
    for y in range(SCRIM_H):
        a = int(235 * (y / SCRIM_H) ** 1.45)
        sd.line([(0, y), (W, y)], fill=(8, 8, 8, a))
    ov.alpha_composite(scrim, (0, H - SCRIM_H))

    d = ImageDraw.Draw(ov)

    # --- logo, top-left (site branding lives top-left too) ---
    logo = Image.open(LOGO).convert("RGBA")
    logo = logo.resize((LOGO_W, round(logo.height * LOGO_W / logo.width)), Image.LANCZOS)
    ov.alpha_composite(logo, (MARGIN, MARGIN))

    # --- caption block, bottom ---
    max_w = W - 2 * MARGIN
    f_chip = ImageFont.truetype(BOLD, 30)
    f_name = ImageFont.truetype(BOLD, 60)
    f_cue = ImageFont.truetype(REG, 46)

    name_lines = wrap(d, name, f_name, max_w)
    cue_lines = wrap(d, cue, f_cue, max_w)

    block_h = 38 + 16 + len(name_lines) * 70 + 14 + len(cue_lines) * 58
    y = H - MARGIN - block_h

    chip = variant.upper()
    d.text((MARGIN, y), " ".join(chip), font=f_chip, fill=ACCENT)
    y += 38 + 16

    for line in name_lines:
        d.text((MARGIN, y), line, font=f_name, fill=INK)
        y += 70
    y += 14
    for line in cue_lines:
        d.text((MARGIN, y), line, font=f_cue, fill=BODY)
        y += 58

    return ov


def render(src, dst, name, variant, cue):
    """Composite in a single ffmpeg pass.

    PIL draws the overlay once to a PNG; ffmpeg's `overlay` filter burns it in.
    Far faster than decoding every frame into Python. `drawtext` is unavailable
    in this Homebrew ffmpeg, which is why the text is a pre-rendered image.
    """
    ov = build_overlay(name, variant, cue)
    png = Path(dst).with_suffix(".overlay.png")
    ov.save(png)
    cmd = [
        "ffmpeg", "-v", "error", "-y",
        "-i", str(src), "-i", str(png),
        # scale guards against any clip that is not already 1080x1920
        "-filter_complex", f"[0:v]scale={W}:{H}[v];[v][1:v]overlay=0:0:format=auto[o]",
        "-map", "[o]", "-map", "0:a?",
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "20",
        "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "128k",
        "-movflags", "+faststart",
        str(dst),
    ]
    subprocess.run(cmd, check=True)
    png.unlink(missing_ok=True)


if __name__ == "__main__":
    manifest = json.loads(Path(sys.argv[1]).read_text())
    outdir = Path(sys.argv[2])
    outdir.mkdir(parents=True, exist_ok=True)
    for job in manifest:
        dst = outdir / job["out"]
        render(job["src"], dst, job["name"], job["variant"], job["cue"])
        print("rendered", dst.name, flush=True)
