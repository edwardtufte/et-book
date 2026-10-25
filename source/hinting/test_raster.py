"""Compare actual FreeType bytecode rasters with the untouched fonts.

python test_raster.py ORIGINAL_ROOT FIXED_ROOT
Requires fonttools==4.67.0 and freetype-py==2.5.1.
This is rasterizer coverage, not a desktop/browser compatibility test.
"""

import ctypes
import hashlib
import json
from pathlib import Path
import platform
import sys

import freetype
from fontTools.ttLib import TTFont


SIZES = list(range(8, 49)) + [64, 96]
FAMILIES = ["et-book-roman-line-figures", "et-book-roman-old-style-figures"]
COVERAGE_LEVELS = [32, 128, 224]


def capture(path):
    face = freetype.Face(str(path))
    with TTFont(path) as font:
        names = font.getGlyphOrder()
    if face.num_glyphs != len(names):
        raise AssertionError("Unexpected glyph count")
    results = {}
    for size in SIZES:
        face.set_pixel_sizes(0, size)
        for index, name in enumerate(names):
            # Use the font's TrueType instructions, never the auto-hinter.
            face.load_glyph(index, freetype.FT_LOAD_NO_AUTOHINT | freetype.FT_LOAD_TARGET_NORMAL)
            face.glyph.render(freetype.FT_RENDER_MODE_NORMAL)
            glyph, bitmap = face.glyph, face.glyph.bitmap
            pixels = bytes(bitmap.buffer)
            row_maxima = [max(pixels[y * bitmap.pitch:y * bitmap.pitch + bitmap.width], default=0) for y in range(bitmap.rows)]
            # FreeType's allocation bounds can include entirely transparent
            # rows or 1/255 coverage fringes. Measure the visible serif edge
            # at three coverage levels, while retaining the full bitmap and
            # raw bounds for the strict unrelated-glyph comparison below.
            coverage_tops = {}
            for level in COVERAGE_LEVELS:
                first = next((y for y, maximum in enumerate(row_maxima) if maximum >= level), None)
                coverage_tops[level] = None if first is None else glyph.bitmap_top - first
            results[size, name] = {
                "advance": [glyph.advance.x, glyph.advance.y],
                "origin": [glyph.bitmap_left, glyph.bitmap_top],
                "box": [bitmap.width, bitmap.rows],
                "pitch": bitmap.pitch,
                "bitmap_sha256": hashlib.sha256(pixels).hexdigest(),
                "coverage_tops": coverage_tops,
            }
    return results


def compare(original_root, fixed_root):
    report = {"platform": platform.platform(), "freetype": freetype.version(), "sizes": SIZES, "results": []}
    print(json.dumps({"platform": report["platform"], "freetype": report["freetype"], "coverage_levels": COVERAGE_LEVELS}), flush=True)
    for interpreter in [35, 40]:
        version = ctypes.c_uint(interpreter)
        code = freetype.FT_Property_Set(freetype.get_handle(), b"truetype", b"interpreter-version", ctypes.byref(version))
        if code:
            raise RuntimeError(f"FreeType interpreter {interpreter} unavailable: {code}")
        for family in FAMILIES:
            relative = Path("et-book") / family / f"{family}.ttf"
            old_path, new_path = original_root / relative, fixed_root / relative
            before, after = capture(old_path), capture(new_path)
            changed = []
            for key, old in before.items():
                new = after[key]
                if old["advance"] != new["advance"]:
                    raise AssertionError((interpreter, family, key, "advance changed"))
                if old != new:
                    if key[1] != "w":
                        raise AssertionError((interpreter, family, key, "unrelated glyph changed"))
                    changed.append(key[0])
            controls = []
            for size in [12, 17, 22]:
                for level in COVERAGE_LEVELS:
                    old_w, old_v = before[size, "w"]["coverage_tops"][level], before[size, "v"]["coverage_tops"][level]
                    new_w, new_v = after[size, "w"]["coverage_tops"][level], after[size, "v"]["coverage_tops"][level]
                    if old_w is None or old_v is None or new_w is None or new_v is None or old_w == old_v or new_w != new_v:
                        raise AssertionError((interpreter, family, size, level, old_w, old_v, new_w, new_v))
                    controls.append({"size": size, "coverage_level": level, "original_w_top": old_w, "v_top": old_v, "fixed_w_top": new_w, "raw_bitmap_tops": {"original_w": before[size, "w"]["origin"][1], "fixed_w": after[size, "w"]["origin"][1], "v": before[size, "v"]["origin"][1]}})
            for metric in ["box", "origin", "advance"]:
                if before[20, "w"][metric] != after[20, "w"][metric]:
                    raise AssertionError((interpreter, family, "20px geometry", metric))
            result = {"interpreter": interpreter, "family": family, "comparisons": len(before), "changed_w_sizes": changed, "all_other_glyphs_and_advances_unchanged": True, "original_failed_fixed_passed": controls, "original_sha256": hashlib.sha256(old_path.read_bytes()).hexdigest(), "fixed_sha256": hashlib.sha256(new_path.read_bytes()).hexdigest()}
            report["results"].append(result)
            print(json.dumps(result), flush=True)
    print(json.dumps({"PASS": True, "platform": report["platform"], "freetype": report["freetype"], "raster_comparisons": sum(r["comparisons"] for r in report["results"])}))
    return report


if __name__ == "__main__":
    compare(Path(sys.argv[1]), Path(sys.argv[2]))
