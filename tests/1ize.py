import PIL.Image
import sys
import os.path

with PIL.Image.open(sys.argv[1]) as im:
    im = im.convert("1")
    im.save(os.path.splitext(sys.argv[1])[0] + "_1ed.png")