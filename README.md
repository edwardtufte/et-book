# ET Book OT

An OpenType version of the typeface used in Edward Tufte’s [books][], from the open-source release of the typeface at [edwardtufte/et-book][orig].

[books]: https://www.edwardtufte.com/tufte/books_vdqi
[orig]: https://github.com/edwardtufte/et-book

The `master` branch contains a usable, but not really very good, conversion of the original fonts using FontForge. This branch contains a work-in-progress second attempt at a conversion using more modern toolchains, in particular the UFO font format.

Current status of the second conversion is as follows:

* All fonts have been converted from the original PostScript Type 1 files to UFO format.
* The Roman and Bold weights have had the lining and old-style variant files merged into single fonts, which use the OpenType `onum` and `lnum` features to select between the two figure styles.
* The letter combinations ff, fi, fl, ffi, and ffl are replaced by their corresponding ligatures with the OpenType `liga` feature.
* Small caps are supported for all letters in the Roman font, but not yet for the small caps punctuation which will be activated by the `c2sc` feature.
* The Roman font (but not yet any of the others) has had the kerning table which was present in the original font suitcase files merged into the OpenType `kern` table.

Note that most of the hacking right now is going on at the raw UFO/OpenType feature file source level (editing the XML and feature files manually to merge features into font files).

Eventual goals, once the basic hacking of the original font files with all their original features into a modern format is complete, include better Unicode support by building accents characters out of the raw base letters and accents in the original repo.

-------------------------------------

ET Book was designed by Dmitry Krasny, Bonnie Scranton, and [Edward Tufte][et]. It was converted from the original `suit` files by [Daphne Preston-Kendal][dpk] ([@dpk][dpkgh]) following the original webfont conversion by  [Adam Schwartz][as] ([@adamschwartz][asgh]).

[et]: https://www.edwardtufte.com/tufte/
[dpk]: http://dpk.io/
[dpkgh]: https://github.com/dpk
[as]: http://adamschwartz.co/
[asgh]: https://github.com/adamschwartz

ET Book OT is MIT-licensed. You may use it in both personal and commercial projects.
