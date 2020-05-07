# ET Book OT

An OpenType version of the typeface used in Edward Tufte’s [books][], from the open-source release of the typeface at [edwardtufte/et-book][orig].

[books]: https://www.edwardtufte.com/tufte/books_vdqi
[orig]: https://github.com/edwardtufte/et-book

Created by converting the fonts to FontForge source files, then making various technical changes to use modern OpenType font features while leaving the typeface design itself unaltered. With these changes it’s easy to use ET Book with all the fancy typographical features on your website, in your word processor, or in a professional typesetting program with OpenType support like [LuaTeX][], [XeTeX][], and [Adobe InDesign][id].

[LuaTeX]: http://www.luatex.org/
[XeTeX]: http://xetex.sourceforge.net/
[id]: https://en.wikipedia.org/wiki/Adobe_InDesign

The following features are currently available:

* Old-style figures (the default) in all styles
* Lining figures (through an OpenType feature) in the Bold and Roman styles
* Automatic ligature substitution (for the included ligatures ff fi fl ffi ffl)

There remain some features to be brought over from the Expert font, of which the most obvious is small-caps support.

-------------------------------------

ET Book was designed by Dmitry Krasny, Bonnie Scranton, and [Edward Tufte][et]. It was converted from the original `suit` files by [David Kendal][dpk] ([@dpk][dpkgh]) following the original webfont conversion by  [Adam Schwartz][as] ([@adamschwartz][asgh]).

[et]: https://www.edwardtufte.com/tufte/
[dpk]: http://dpk.io/
[dpkgh]: https://github.com/dpk
[as]: http://adamschwartz.co/
[asgh]: https://github.com/adamschwartz

ET Book OT is MIT-licensed. You may use it in both personal and commercial projects.
