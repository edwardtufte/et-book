"""Checks against an untouched checkout, not regenerated reference fonts.

python test_fonts.py ORIGINAL_ROOT FIXED_ROOT
Requires fonttools==4.67.0.
"""

import hashlib
from contextlib import contextmanager
import importlib.util
import io
from pathlib import Path
import struct
import sys
import tempfile
import unittest

from fontTools.ttLib import TTFont

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("fix_roman_w", HERE / "fix_roman_w.py")
fix = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fix)
ORIGINAL, FIXED = map(Path, sys.argv[1:3])
sys.argv = sys.argv[:1]


def path(root, family, extension):
    return root / "et-book" / family / f"{family}.{extension}"


@contextmanager
def temporary_directory(prefix):
    root = Path(tempfile.gettempdir()).resolve()
    with tempfile.TemporaryDirectory(prefix=prefix) as directory:
        target = Path(directory).resolve()
        if target.parent != root or not target.name.startswith(prefix):
            raise ValueError("Temporary cleanup target escaped its expected root")
        yield target


class FontPreservation(unittest.TestCase):
    def test_original_identity(self):
        for family, formats in fix.ORIGINALS.items():
            for extension, expected in formats.items():
                self.assertEqual(hashlib.sha256(path(ORIGINAL, family, extension).read_bytes()).hexdigest(), expected)

    def test_only_w_instructions_change(self):
        for family in fix.ORIGINALS:
            for extension in ("ttf", "woff"):
                with TTFont(path(ORIGINAL, family, extension)) as old, TTFont(path(FIXED, family, extension)) as new:
                    self.assertEqual(old.getGlyphOrder(), new.getGlyphOrder())
                    changed = []
                    for name in old.getGlyphOrder():
                        a, b = old["glyf"][name], new["glyf"][name]
                        if a.compile(old["glyf"]) != b.compile(new["glyf"]):
                            changed.append(name)
                        self.assertEqual(a.getCoordinates(old["glyf"]), b.getCoordinates(new["glyf"]))
                    self.assertEqual(changed, ["w"])
                    self.assertEqual(old["hmtx"].metrics, new["hmtx"].metrics)

    def test_other_tables_are_identical(self):
        for family in fix.ORIGINALS:
            for extension in ("ttf", "woff"):
                with TTFont(path(ORIGINAL, family, extension)) as old, TTFont(path(FIXED, family, extension)) as new:
                    self.assertEqual(old.reader.keys(), new.reader.keys())
                    for tag in old.reader.keys():
                        if tag not in ("glyf", "loca", "head"):
                            self.assertEqual(old.reader[tag], new.reader[tag], (family, extension, tag))
                    # Only the mandatory sfnt checksum adjustment may change.
                    a, b = old.reader["head"], new.reader["head"]
                    self.assertEqual(a[:8] + a[12:], b[:8] + b[12:])

    def test_x_height_anchor_and_original_serif_cvt(self):
        for family, cvt in [("et-book-roman-line-figures", 4), ("et-book-roman-old-style-figures", 7)]:
            with TTFont(path(FIXED, family, "ttf")) as font:
                self.assertEqual(font["glyf"]["w"].coordinates[69][1], font["cvt "].values[1])
                self.assertEqual(font["cvt "].values[cvt], 59)
                self.assertTrue(font["glyf"]["w"].program.getBytecode().startswith(bytes.fromhex("00b24501002b")))

    def test_woff_matches_ttf_tables(self):
        for family in fix.ORIGINALS:
            with TTFont(path(FIXED, family, "ttf")) as ttf, TTFont(path(FIXED, family, "woff")) as woff:
                self.assertEqual(ttf.reader.keys(), woff.reader.keys())
                for tag in ttf.reader.keys():
                    a, b = ttf.reader[tag], woff.reader[tag]
                    if tag == "head":
                        a, b = a[:8] + a[12:], b[:8] + b[12:]
                    self.assertEqual(a, b, (family, tag))

    def test_eot_metadata_and_exact_ttf_payload(self):
        for family in fix.ORIGINALS:
            old, new = path(ORIGINAL, family, "eot").read_bytes(), path(FIXED, family, "eot").read_bytes()
            total, length, version, flags = struct.unpack_from("<4I", new)
            self.assertEqual((total, version, flags), (len(new), 0x20002, 0))
            self.assertEqual(new[-length:], path(FIXED, family, "ttf").read_bytes())
            old_header = old[:-struct.unpack_from("<I", old, 4)[0]]
            new_header = new[:-length]
            self.assertEqual(old_header[16:60] + old_header[64:], new_header[16:60] + new_header[64:])
            with TTFont(io.BytesIO(new[-length:])) as font:
                self.assertEqual(struct.unpack_from("<I", new, 60)[0], font["head"].checkSumAdjustment)

    def test_rebuild_is_byte_reproducible(self):
        with temporary_directory("etbook-rebuild-") as directory:
            fix.rebuild(ORIGINAL, Path(directory))
            for family, formats in fix.ORIGINALS.items():
                for extension in formats:
                    self.assertEqual(path(Path(directory), family, extension).read_bytes(), path(FIXED, family, extension).read_bytes())

    def test_wrong_input_rejected_without_outputs(self):
        with temporary_directory("etbook-reject-") as directory:
            destination = Path(directory) / "out"
            with self.assertRaises(ValueError):
                fix.rebuild(FIXED, destination)
            self.assertFalse(destination.exists())

    def test_refuses_in_place_rebuild(self):
        with self.assertRaises(ValueError):
            fix.rebuild(ORIGINAL, ORIGINAL)


if __name__ == "__main__":
    unittest.main(verbosity=2)
