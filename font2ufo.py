import sys

import defcon
import extractor


if __name__ == '__main__':
    ufo = defcon.Font()
    extractor.extractUFO(sys.argv[1], ufo)
    ufo.save(sys.argv[2])
else:
    raise ImportError('font2ufo is a script, not a module')
