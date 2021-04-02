# glyph2svgpath ufo-font glyph-name
# gets the glyph with the specified from the font at ufo-font and prints an SVG path for the glyph (in vertical mirror-image)

import sys

from fontParts.world import OpenFont
from fontTools.pens import svgPathPen
from fontTools.ufoLib.glifLib import GlyphSet

font = OpenFont(sys.argv[1])
glyph_set = GlyphSet(sys.argv[1] + '/glyphs/')
pen = svgPathPen.SVGPathPen(glyph_set)

glyph = font[sys.argv[2]]
glyph.draw(pen)
print(pen.getCommands())

