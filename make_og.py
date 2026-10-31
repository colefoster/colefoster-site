"""Render site/og.png, the 1200x630 link-share card, from projects.yaml.

Run on a Mac after changing projects.yaml: python3 make_og.py (needs Pillow + PyYAML).
Uses macOS system fonts, so CI does not run it; the PNG is committed.
"""
from pathlib import Path

import yaml
from PIL import Image, ImageDraw, ImageFont

from build import ROOT, visible_sections

W, H, PAD = 1200, 630, 80
BG, FG, MUTED, ACCENT = "#111111", "#dddddd", "#9a9a9a", "#8ab4f8"  # the site's dark-mode palette
FONT = "/System/Library/Fonts/HelveticaNeue.ttc"


def font(size, bold=False):
    return ImageFont.truetype(FONT, size, index=1 if bold else 0)


def render(data):
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    d.text((PAD, PAD - 8), data["title"], font=font(84, bold=True), fill=FG)
    d.text((PAD, PAD + 104), data["intro"], font=font(30), fill=MUTED)

    groups = list(visible_sections(data))
    col_w = (W - 2 * PAD) // len(groups)
    top = 310
    for i, (title, projects) in enumerate(groups):
        x = PAD + i * col_w
        d.text((x, top), title.upper(), font=font(22, bold=True), fill=MUTED)
        for j, p in enumerate(projects):
            d.text((x, top + 46 + j * 50), p["name"], font=font(38, bold=True), fill=FG)

    d.line((PAD, H - PAD - 40, W - PAD, H - PAD - 40), fill="#333333", width=2)
    d.text((PAD, H - PAD - 16), data["url"].removeprefix("https://").rstrip("/"),
           font=font(28), fill=ACCENT)
    return img


if __name__ == "__main__":
    data = yaml.safe_load((ROOT / "projects.yaml").read_text())
    render(data).save(ROOT / "site" / data["image"], optimize=True)
