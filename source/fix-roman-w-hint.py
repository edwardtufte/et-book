"""Repair the lowercase w hint in the two legacy Roman webfonts.

Run this file from the repository root after installing fonttools.  The script
updates both the TTF and WOFF copies and refuses to touch an unfamiliar font.
"""

from pathlib import Path

from fontTools.ttLib import TTFont
from fontTools.ttLib.tables.ttProgram import Program


FACES = {
    "et-book/et-book-roman-line-figures/et-book-roman-line-figures": {
        "serif_width": 4,
        "before": (
            "00b26b00002bb05d33b0742fb41120304052241733b10604e9b129453232"
            "01b0762fb177012b00b1746b1112b2193664393939b00611b1044e39393031"
        ),
        "after": (
            "00b20601002bb129453333b17404e9b41120304052241732b26b00002b"
            "b05d3301b0762fb177012b00b1746b1112b2193664393939b00611b104"
            "4e39393031"
        ),
    },
    "et-book/et-book-roman-old-style-figures/et-book-roman-old-style-figures": {
        "serif_width": 7,
        "before": (
            "00b26b00002bb05d33b0742fb41120304052241733b10607e9b129453232"
            "01b0762fb177012b00b1746b1112b2193664393939b00611b1044e39393031"
        ),
        "after": (
            "00b20601002bb129453333b17407e9b41120304052241732b26b00002b"
            "b05d3301b0762fb177012b00b1746b1112b2193664393939b00611b104"
            "4e39393031"
        ),
    },
}


def repaired_assembly(serif_width):
    # Anchor the top of w to the Roman x-height, then position its upper serif
    # below that anchor.  The horizontal and interpolation tail is unchanged.
    return [
        "SVTCA[0]",
        "PUSHB[ ]", "6", "1", "0", "CALL[ ]",
        "PUSHB[ ]", "41", "69", "SHP[1]", "SHP[1]",
        "PUSHB[ ]", "116", str(serif_width), "MIRP[01001]",
        "PUSHB[ ]", "17", "32", "48", "64", "82", "DEPTH[ ]", "SLOOP[ ]", "SHP[0]",
        "PUSHB[ ]", "107", "0", "0", "CALL[ ]",
        "PUSHB[ ]", "93", "SHP[1]",
        "SVTCA[1]",
        "PUSHB[ ]", "118", "MDAP[1]",
        "PUSHB[ ]", "119", "1", "CALL[ ]",
        "SVTCA[0]",
        "PUSHB[ ]", "116", "107", "SRP1[ ]", "SRP2[ ]",
        "PUSHB[ ]", "25", "54", "100", "IP[ ]", "IP[ ]", "IP[ ]",
        "PUSHB[ ]", "6", "SRP1[ ]",
        "PUSHB[ ]", "4", "78", "IP[ ]", "IP[ ]",
        "IUP[0]", "IUP[1]",
    ]


def patch_font(path, config):
    font = TTFont(path, recalcBBoxes=False, recalcTimestamp=False)
    glyph = font["glyf"][font.getBestCmap()[ord("w")]]
    current = bytes(glyph.program.getBytecode())
    before = bytes.fromhex(config["before"])
    after = bytes.fromhex(config["after"])

    program = Program()
    program.fromAssembly(repaired_assembly(config["serif_width"]))
    if bytes(program.getBytecode()) != after:
        raise RuntimeError("The assembled hint program did not match the reviewed bytecode")

    if current == after:
        print(f"unchanged  {path}")
        return
    if current != before:
        raise RuntimeError(f"Unexpected lowercase-w hint program in {path}")

    glyph.program = program
    temporary = path.with_suffix(path.suffix + ".tmp")
    font.save(temporary)
    font.close()
    temporary.replace(path)
    print(f"repaired   {path}")


for stem, config in FACES.items():
    for extension in (".ttf", ".woff"):
        patch_font(Path(stem + extension), config)
