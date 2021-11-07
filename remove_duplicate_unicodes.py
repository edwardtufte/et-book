# NB and warning!: works in-place
import os
import os.path
import sys


def rewrite_glyph(path):
    with open(path + '.new', 'w', encoding='iso-8859-1') as ouf:
        with open(path, 'r', encoding='iso-8859-1') as inf:
            for line in inf:
                if '<unicode' not in line:
                    ouf.write(line)

    os.rename(path + '.new', path)

def remove_duplicate_unicodes(glyphs_dir):
    glyphs = {}
    
    for glyph_file in os.listdir(glyphs_dir):
        if not glyph_file.endswith('.glif'): continue
        glyph_name = glyph_file[:-5]
        glyphs[glyph_name] = os.path.join(glyphs_dir, glyph_file)

    for glyph_name, glyph_path in glyphs.items():
        glyph_basename = glyph_name.rsplit('.', 1)[0]
        if glyph_name != glyph_basename and glyph_basename in glyphs:
            rewrite_glyph(glyph_path)

if __name__ == '__main__':
    glyphs_dir = sys.argv[1]
    remove_duplicate_unicodes(glyphs_dir)

