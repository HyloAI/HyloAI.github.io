"""Subset MiSans to the characters the website uses and write web fonts to assets/fonts.

Re-run after building Research whenever website text changes:

    uv run --no-project --with fonttools --with brotli python tools/subset_fonts.py <dir with MiSans-*.otf>

The source OTFs come from Xiaomi (https://hyperos.mi.com/font) and are not kept in this repository.
"""

import pathlib
import sys

from fontTools import subset

ROOT = pathlib.Path(__file__).resolve().parent.parent
WEIGHTS = {"Regular": 400, "Medium": 500, "Demibold": 600, "Bold": 700, "Heavy": 900}


def main() -> None:
    src = pathlib.Path(sys.argv[1])
    text = (ROOT / "index.html").read_text(encoding="utf-8")
    for page in (ROOT / "research").rglob("*.html"):
        text += page.read_text(encoding="utf-8")
    text += (ROOT / "assets/research.js").read_text(encoding="utf-8")
    # every character on the website, plus printable ASCII so a missing Latin font still renders
    chars = sorted(set(text) | {chr(c) for c in range(0x20, 0x7F)})
    chars = "".join(c for c in chars if c.isprintable())
    out = ROOT / "assets" / "fonts"
    out.mkdir(parents=True, exist_ok=True)
    for name, weight in WEIGHTS.items():
        options = subset.Options()
        options.flavor = "woff2"
        options.layout_features = ["*"]
        options.name_IDs = ["*"]
        options.notdef_outline = True
        font = subset.load_font(str(src / f"MiSans-{name}.otf"), options)
        subsetter = subset.Subsetter(options)
        subsetter.populate(text=chars)
        subsetter.subset(font)
        target = out / f"misans-{weight}.woff2"
        subset.save_font(font, str(target), options)
        print(f"{target.relative_to(ROOT)}  {target.stat().st_size // 1024} KB")
    print(f"{len(chars)} characters")


if __name__ == "__main__":
    main()
