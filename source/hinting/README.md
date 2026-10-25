# Roman lowercase w hint repair

The distributed Roman LF and OSF fonts placed the underside of `w`'s top
serif on the pixel grid, then added the serif thickness. At sizes including
12, 17 and 22 pixels, that made `w` one pixel taller than the adjacent
lowercase letters.

The repair anchors point 69 to the font's existing x-height control value
before placing the serif underside. It uses the existing alignment function
and each font's original serif control value. The remainder of `w`'s
instructions is retained. No outlines, advance widths, side bearings,
kerning, character mappings, other glyph instructions or global hint tables
are changed. Capital `W` already uses the cap-height control value and is
unchanged.

Both Roman TTFs and their WOFFs contain the repair. Their EOT containers keep
the existing names, embedding metadata and root strings, but use the
format's uncompressed TTF payload instead of MTX compression. They are
therefore larger. The EOT payload is exactly the corresponding fixed TTF.
The unhinted `source/4-ttf` fonts, SVGs, other styles and ligature-enabled
fonts do not contain this faulty instruction sequence and are left intact.

## Reproduce

Use Python 3.11+ and `fonttools==4.67.0`. Keep an untouched checkout of
commit `24d3a3bbfc880095d3df2b9e9d60d05819138e89` in `../et-book-original`.
From this repository root:

```sh
python source/hinting/fix_roman_w.py ../et-book-original .
python source/hinting/test_fonts.py ../et-book-original .
```

The builder verifies all six original file hashes before writing and
preserves font timestamps. Repeated builds produce identical bytes. It
does not install fonts or invoke an auto-hinter. Tests compare every glyph's
coordinates and metrics, all unaffected tables, the WOFF/TTF content and
the EOT metadata/payload, and reject unexpected inputs.

For actual FreeType raster comparisons, additionally install
`freetype-py==2.5.1`, then run:

```sh
python source/hinting/test_raster.py ../et-book-original .
```

This exercises native TrueType interpreters 35 and 40 at 8–48, 64 and 96
pixels, including every defined glyph and the original x-height failures.
FreeType bitmap allocation bounds may contain transparent rows or tiny
antialias fringes, so x-height is compared at coverage levels 32, 128 and
224 out of 255. All three levels must reproduce the original mismatch
and align after the repair. Raw bitmap bounds and hashes are retained;
unrelated glyphs still require exact pixel and metric equality.
The repaired `w` can have different antialias coverage even where its
dimensions were already correct, including 20 pixels. Other glyphs and
all advances must remain identical. These checks do not establish every
browser, operating-system font setting, or legacy EOT consumer's behavior.

References: [TrueType control values](https://learn.microsoft.com/en-us/typography/truetype/hinting-tutorial/basic-global-tables),
[instruction semantics](https://learn.microsoft.com/en-us/typography/opentype/spec/tt_instructions),
[EOT format and compression flag](https://www.w3.org/submissions/EOT/).
