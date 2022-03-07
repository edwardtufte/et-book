# Diacritic mark positioning

These the correct `xOffset` and `yOffset` values for characters built from the following bases plus accents above the character in question, calculated using dieresis as the combining character except where noted (and therefore possibly incorrect for others, but this will eventually be checked and noted).

## Roman

| base | `xOffset` | `yOffset` |
| -- | --:| --:|
| A | 180 | 222 |
| a | 0 | 0 |
| a.sc | 74 | 75 |
| c* | 33 | 0 |
| E† | 137 | 222 |
| e† | 56 | 0 |
| e.sc | 45 | 75 |
| I‡ | 0 | 222 |
| dotlessi‡ | -39 | 0 |
| i.sc | -30 | 75 |
| N§ | 256 | 228 |
| n§ | 81 | 0 |
| n.sc§ | 119 | 75 |
| O | 240 | 222 |
| o† | 77 | 0 |
| o.sc | 111 | 75 |
| S‖ | 83 | 222 |
| s‖ | -17 | 0 |
| U | 240 | 222 |
| u* | 89 | 0 |
| u.sc | 119 | 75 |
| Y | 196 | 222 |
| y | 72 | 0 |
| y.sc | 86 | 75 |
| Z‡ | 180 | 222 |
| z‡ | 39 | 0 |

\* based on observation that c + cedilla matches up with ccedilla at 33, -10, and that accent marks underneath seem generally to be at yOffset -10.
† the dots on Edieresis, edieresis, odieresis, and udieresis are slightly smaller than those in dieresis itself. The numbers give the centre-point position, i.e. so that the right edge of the left dot and the left edge of the right dot match up.
‡ accented I and i characters might need to be made wider to accommodate the accent mark? I’m unsure.
§ tested with tilde, not dieresis.
‖ tested with caron, not dieresis.

## Semibold

To be filled in.

## Bold

To be filled in.

## Italic

| base | ¨ `xOffset` | ¨ `yOffset` | ´ `xOffset` | ´ `yOffset` | \` `xOffset` | \` `yOffset` | Other |
| -- | --:| --:| --:| --:| --:| --:| -- |
| A | 326 | 219 | 336 | 219 | 286 | 219 | | |
| a* | 32 | 16 | 32 | 0 | 32 | 0 | | |
| E | 198 | 219 | 227 | 217 | 157 | 219 | | |
| e† | 12 | 20 | 7 | 0 | 7 | 0 | | |
| I | 73 | 219 | 73 | 219 | 23 | 219 | | |
| dotlessi | -49 | 20 | -47 | 0 | -84 | 0 | | |
| N | — | — | — | — | — | — | See ‡ | See ‡ |
| n | — | — | — | — | — | — | See ‡ | See ‡ |
| O | 273 | 238 | 313 | 219 | 262 | 219 | | |
| o | 26 | 10 | 33 | 0 | 33 | 0 | | |

<!-- | S | @@ | @@ | -->
<!-- | s | @@ | @@ | -->
<!-- | U | @@ | @@ | -->
<!-- | u | @@ | @@ | -->
<!-- | Y | @@ | @@ | -->
<!-- | y | @@ | @@ | -->
<!-- | Z | @@ | @@ | -->
<!-- | z | @@ | @@ | -->

\* The dots on adieresis are slightly larger than the ones in dieresis. This takes a value such that the dieresis dots are pretty much dead centre in the adieresis dots.
† The dots on edieresis are slightly smaller than the ones in dieresis. The numbers give the centre-point position, i.e. so that the right edge of the left dot and the left edge of the right dot match up.
‡ The tilde on Ntilde and ntilde is a different shape from tilde. 300, 219 makes tilde roughly line up with Ntilde; 55, 0 with ntilde. If other tilde’d accented characters are needed, it would probably be best to pull the tildes out pof Ntilde and ntilde, as they look somewhat more italic (and more balanced) than tilde.

## Display Italic

To be filled in.
