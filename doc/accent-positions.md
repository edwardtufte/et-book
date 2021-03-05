# Diacritic mark positioning

These the correct `xOffset` and `yOffset` values for characters built from the following bases plus accents above the character in question, calculated using dieresis as the combining character except where noted (and therefore possibly incorrect for others, but this will eventually be checked and noted).

## Roman

| base | `xOffset` | `yOffset` |
| -- | --:| --:|
| A | 180 | 222 |
| a | 0 | 0 |
| a.sc | 74 | 75 |
| E* | 137 | 222 |
| e* | 56 | 0 |
| e.sc | 45 | 75 |
| I** | 0 | 222 |
| dotlessi** | -39 | 0 |
| i.sc | -30 | 75 |
| N† | 256 | 228 |
| n† | 81 | 0 |
| n.sc† | 119 | 75 |
| O | 240 | 222 |
| o* | 77 | 0 |
| o.sc | 111 | 75 |
| S‡ | 83 | 222 |
| s‡ | -17 | 0 |
| U | 240 | 222 |
| u* | 89 | 0 |
| u.sc | 119 | 75 |
| Y | 196 | 222 |
| y | 72 | 0 |
| y.sc | 86 | 75 |
| Z‡ | 180 | 222 |
| z‡ | 39 | 0 |

\* the dots on Edieresis, edieresis, odieresis, and udieresis are slightly smaller than those in dieresis itself. The numbers give the centre-point position, i.e. so that the right edge of the left dot and the left edge of the right dot match up.
** accented I and i characters might need to be made wider to accommodate the accent mark? I’m unsure.
† tested with tilde, not dieresis.
‡ tested with caron, not dieresis.

## Semibold

To be filled in.

## Bold

To be filled in.

## Italic

To be filled in.

## Display Italic

To be filled in.
