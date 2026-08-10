#!/usr/bin/env python3
"""Turn the raw Chrome captures into the assets used by the welcome pages.

Reads the four screenshots from the project root, removes everything that is
not part of the instruction (macOS window buttons, the new tab page clutter),
crops the dead space at the bottom and writes 1x/2x WebP into assets/img.

Run from anywhere:  python3 welcome-site/tools/prepare_screens.py
"""

from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parents[1] / "assets" / "img"

# Full-window captures, 3420x2146, taken with an English Chrome on macOS.
SHOTS = {
    "step-pin": {"dark": "7.png", "light": "9.png", "popup": True},
    "step-open": {"dark": "8.png", "light": "10.png", "popup": False},
}

CROP_HEIGHT = 1700  # drops the empty page bottom together with "Customise Chrome"
WIDTHS = {"": 1000, "@2x": 2000}

# macOS close/minimise/zoom, up to the tab search chevron at x=181.
TRAFFIC_LIGHTS = (0, 0, 168, 84)
# Shortcut tiles and the "Add extensions..." promo card, both on flat background.
SHORTCUT_TILES = (1520, 864, 1915, 1050)
PROMO_CARD = (1128, 1136, 2275, 1311)
# "Gmail Images" and the apps grid sit right next to the popup, whose drop
# shadow reaches ~20px to the right of its border at x=3228. A flat fill would
# cut that gradient off, so the band is rebuilt from a row below the text where
# the same shadow is present and nothing else is.
GOOGLE_LINKS_BAND = (214, 266)
GOOGLE_LINKS_DONOR_ROW = 300
# A few pixels inside the popup, so the border column itself is rebuilt too:
# the first glyph of "Images" touches it.
POPUP_EDGE = 3218
PAGE_LEFT = 3090
PAGE_RIGHT = 3378


def clear_google_links(im: Image.Image, beside_popup: bool) -> None:
    left = POPUP_EDGE if beside_popup else PAGE_LEFT
    top, bottom = GOOGLE_LINKS_BAND
    donor = im.crop((left, GOOGLE_LINKS_DONOR_ROW, PAGE_RIGHT, GOOGLE_LINKS_DONOR_ROW + 1))
    im.paste(donor.resize((PAGE_RIGHT - left, bottom - top)), (left, top))


def prepare(name: str, spec: dict) -> None:
    for theme in ("dark", "light"):
        src = ROOT / spec[theme]
        im = Image.open(src).convert("RGB")
        px = im.load()
        strip = px[2, 2]
        page = px[100, 1500]

        im.paste(page, SHORTCUT_TILES)
        im.paste(page, PROMO_CARD)
        clear_google_links(im, spec["popup"])
        im.paste(strip, TRAFFIC_LIGHTS)

        im = im.crop((0, 0, im.width, CROP_HEIGHT))

        for suffix, width in WIDTHS.items():
            height = round(im.height * width / im.width)
            out = OUT / f"{name}-{theme}{suffix}.webp"
            im.resize((width, height), Image.LANCZOS).save(
                out, "WEBP", quality=86, method=6
            )
            print(f"{src.name} -> {out.relative_to(OUT.parents[1])} ({width}x{height})")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for name, spec in SHOTS.items():
        prepare(name, spec)


if __name__ == "__main__":
    main()
