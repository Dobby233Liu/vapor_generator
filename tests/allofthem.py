import sys
import os.path
mydir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(mydir + "/..")

import vapor_generator as vaporizer
import io
import PIL.ImageChops
import difflib
import shutil
import sys

allvapor = []
with open(os.path.join(mydir, "allofthem.txt"), "r", encoding="utf-8") as all_dat:
    all_dat_l = all_dat.readlines()
    all_dat_l.reverse()
    allvapor = map(lambda x: x.rstrip().encode("ascii"), all_dat_l)

shutil.rmtree(os.path.join(mydir, "allofthem"), ignore_errors=True)
os.mkdir(os.path.join(mydir, "allofthem"))

optimize = len(sys.argv) > 1

for i, vapor in enumerate(allvapor):
    with open(os.path.join(mydir, f"allofthem/{i:02}.bin"), "wb") as f:
        f.write(vapor)
    with vaporizer.decompress(vapor) as im:
        im.save(os.path.join(mydir, f"allofthem/{i:02}.png"))
        recom = vaporizer.compress(im, optimize=optimize)
        if recom == vapor:
            continue
        print(f"{i} is not the same")
        #print([li for li in difflib.ndiff(vapor.decode("utf-8"), recom.decode("utf-8")) if not li.startswith(" ")])
        print(f"{len(vapor)} vs {len(recom)} ({-(1 - len(recom) / len(vapor)) * 100:.2f}%)")
        with open(os.path.join(mydir, f"allofthem/{i:02}_r.bin"), "wb") as f:
            f.write(recom)
        with vaporizer.decompress(recom) as imx:
            imx.save(os.path.join(mydir, f"allofthem/{i:02}_r.png"))
            with PIL.ImageChops.difference(im, imx) as imd:
                if imd.getbbox():
                    imd.save(os.path.join(mydir, f"allofthem/{i:02}_d.png"))
                else:
                    print(f"no diff in both decompression output according to PIL")