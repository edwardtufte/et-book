# ET Book

An OpenType version of the typeface used in Edward Tufte’s [books][], from the open-source release of the typeface at [edwardtufte/et-book][orig].

[books]: https://www.edwardtufte.com/tufte/books_vdqi
[orig]: https://github.com/edwardtufte/et-book

The `fontforge-old` branch contains a usable, but not really very good, conversion of the original fonts using FontForge. This branch contains a work-in-progress second attempt at a conversion using more modern toolchains, in particular the UFO font format.

At the moment, the converstion is essentially complete:

* All fonts have been converted from the original PostScript Type 1 files to UFO format.
* The Roman and Bold weights have had the lining and old-style variant files merged into single fonts, which use the OpenType `onum` and `lnum` features to select between the two figure styles.
* The letter combinations ff, fi, fl, ffi, and ffl are replaced by their corresponding ligatures with the OpenType `liga` feature.
* Small caps are supported for all letters in the Roman font, and for hopefully all of the smaller punctuation activated by the `c2sc` feature.
* Numerator and denominator figures are available as `numr` and `dnom` in the Roman font, and OpenType fractions can be built using the `frac` feature.
* The kerning tables which were present in the original font suitcase files have been merged into the OpenType `kern` table.
* … but there are still one or two odd characters from the Expert font which aren’t supported in the OpenType font. These will probably end up under `ss01` or something.

But before these fonts are actually released as version 2.0, the following additional features will be added/problems addressed:

* Support for all the official languages of the European Union that use the LAtin alphabet. There was fairly decent support for Western European languages in the original ET Book fonts, but characters for Eastern European languages were lacking. There are two characters that need(ed) designing specially, d with crossbar for Croatian and h with crossbar for Maltese. The former is done, the latter will be done soon. The remainder are simple compositions of a base character plus a diacritic, and the design of the existing accented characters in the fonts is currently being analysed to facilitate adding further such characters to harmonize with the original ones. See issue #2.
* **Help wanted!** The original ET Book fonts had no hinting information — as a result, the webfonts rendered badly on various platforms. I’m trying to get auto-hinting for PostScript outlines to work, but it seems to be a bit of a dark art. If you have knowledge in this area, please let me know! See issue #4.
* The original PostScript fonts had replaced the ‹, ›, and ‡ characters with extended ligatures, presumably because Edward Tufte did not need those characters for his books, but access to those ligatures without having to switch to the Expert font was rather handy. Regardless, since those ligatures are now automatically used with the right letter combinations, and those characters are actually used in many countries, new guillemets and double-dagger characters will be supplied. See issue #17.
* 2.0 will likely include an fj ligature (useful for Scandinavian languages and loanwords therefrom).
* In time for (or perhaps after) 2.0, figures in the Roman font will be available in superscript and subscript positions as well as numerator and denominator positions.

Also after 2.0: language support will be further improved to also cover all the minority and regional languages of Europe; I hope to improve the kerning, which at present is rather minimal; there may well be further ligatures of fb, fh, etc., and a specially designed f for situations where a ligature can’t be used to avoid an unsightly collission or near-miss; and who knows what else.

-------------------------------------

ET Book was designed by Dmitry Krasny, Bonnie Scranton, and [Edward Tufte][et]. It was converted from the original `suit` files by [Daphne Preston-Kendal][dpk] ([@dpk][dpkgh]) following the original webfont conversion by  [Adam Schwartz][as] ([@adamschwartz][asgh]).

[et]: https://www.edwardtufte.com/tufte/
[dpk]: http://dpk.io/
[dpkgh]: https://github.com/dpk
[as]: http://adamschwartz.co/
[asgh]: https://github.com/adamschwartz

ET Book OT is MIT-licensed. You may use it in both personal and commercial projects.
