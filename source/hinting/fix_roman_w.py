"""Rebuild the two Roman distributions from the pinned pre-fix fonts.

Requires fonttools==4.67.0. No font installation, autohinting, or outline edits.
"""

import argparse
import hashlib
import io
from pathlib import Path
import struct

from fontTools.ttLib import TTFont


ORIGINALS = {
    "et-book-roman-line-figures": {
        "ttf": "48a4c0e333ea34f975702a965db80c29bc831f215c3606f47b3fe14f53d0f638",
        "woff": "be0f2c061cd8c57b38b5edd8c03dac72ca7d87fb5c3f7f5c32ed72dede39a601",
        "eot": "8443b33a021f7c4d04762482b9e262f58e7490f73ee3d5297c62ac8ca87db927",
    },
    "et-book-roman-old-style-figures": {
        "ttf": "cd229daa847df81e286943e4da3895df6e186b9379e71d487521fad56cf6a1c0",
        "woff": "58d154747bfa14725671c667c034066242c19039b9e90180ef46ca5c984a1b05",
        "eot": "87b77825d8360c3e5b4de8b3dbcba18259f5d535ff7b5d0180d143c95e5ef957",
    },
}

# Original baseline/serif-first y instructions, ending before SVTCA[x].
OLD_PREFIXES = {
    bytes.fromhex("00b26b00002bb05d33b0742fb41120304052241733b10604e9b129453232"): 4,
    bytes.fromhex("00b26b00002bb05d33b0742fb41120304052241733b10607e9b129453232"): 7,
}

# Anchor point 69 (y=854) to the existing x-height CVT[1], using the
# font's own alignment function 0, just as v does. Move the other serif
# tops with it, then place their undersides using the existing serif CVT
# (index 4 for lining figures, 7 for old-style figures).
# Finally align both baseline extrema. All subsequent x hints and
# interpolation instructions remain byte-for-byte unchanged.
NEW_PREFIX = """
SVTCA[0]
PUSHB[ ]
69
1
0
CALL[ ]
PUSHB[ ]
41
6
SHP[1]
SHP[1]
PUSHB[ ]
116
SERIF_CVT
MIRP[01001]
PUSHB[ ]
17
32
48
64
82
DEPTH[ ]
SLOOP[ ]
SHP[0]
PUSHB[ ]
107
0
0
CALL[ ]
PUSHB[ ]
93
SHP[1]
""".strip().splitlines()


def fix_font(data):
    font = TTFont(io.BytesIO(data), recalcBBoxes=False, recalcTimestamp=False)
    program = font["glyf"]["w"].program
    original = program.getBytecode()
    matched = [(prefix, cvt) for prefix, cvt in OLD_PREFIXES.items() if original.startswith(prefix)]
    if len(matched) != 1:
        raise ValueError("Unexpected Roman w hint program; refusing to modify it")
    prefix, cvt = matched[0]
    program.fromAssembly([str(cvt) if line == "SERIF_CVT" else line for line in NEW_PREFIX])
    program.fromBytecode(program.getBytecode() + original[len(prefix):])
    output = io.BytesIO()
    font.save(output, reorderTables=False)
    font.close()
    return output.getvalue()


def replace_eot_font(original, old_ttf, fixed_ttf):
    # These existing v2.2 EOTs contain MTX-compressed font data. EOT also
    # supports raw sfnt data: retain the original metadata/root strings,
    # clear only the compression flag and replace the payload with the TTF.
    total, data_size, version, flags = struct.unpack_from("<4I", original)
    if total != len(original) or version != 0x20002 or flags != 4:
        raise ValueError("Unexpected EOT container")
    old_font = TTFont(io.BytesIO(old_ttf))
    fixed_font = TTFont(io.BytesIO(fixed_ttf))
    if struct.unpack_from("<I", original, 60)[0] != old_font["head"].checkSumAdjustment:
        raise ValueError("EOT checksum does not identify the original TTF")
    header = bytearray(original[:-data_size])
    struct.pack_into("<4I", header, 0, len(header) + len(fixed_ttf), len(fixed_ttf), version, 0)
    struct.pack_into("<I", header, 60, fixed_font["head"].checkSumAdjustment)
    old_font.close()
    fixed_font.close()
    return bytes(header) + fixed_ttf


def rebuild(original_root, output_root):
    original_root, output_root = Path(original_root).resolve(), Path(output_root).resolve()
    if original_root == output_root:
        raise ValueError("Use separate original and output directories")
    # Validate all input bytes before writing anything.
    originals = {}
    for family, formats in ORIGINALS.items():
        for extension, expected in formats.items():
            relative = Path("et-book") / family / f"{family}.{extension}"
            data = (original_root / relative).read_bytes()
            if hashlib.sha256(data).hexdigest() != expected:
                raise ValueError(f"Unexpected input hash: {relative}")
            originals[family, extension] = data
    outputs = {}
    for family in ORIGINALS:
        ttf = fix_font(originals[family, "ttf"])
        outputs[family, "ttf"] = ttf
        outputs[family, "woff"] = fix_font(originals[family, "woff"])
        outputs[family, "eot"] = replace_eot_font(originals[family, "eot"], originals[family, "ttf"], ttf)
    for (family, extension), data in outputs.items():
        target = output_root / "et-book" / family / f"{family}.{extension}"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
        print(hashlib.sha256(data).hexdigest(), target)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("original_root", type=Path)
    parser.add_argument("output_root", type=Path)
    args = parser.parse_args()
    rebuild(args.original_root, args.output_root)
