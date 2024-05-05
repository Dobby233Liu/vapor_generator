import vapor_generator as vaporizer
import os.path
import io
import PIL.ImageChops
import difflib
import shutil
import sys

mydir = os.path.dirname(os.path.realpath(__file__))

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
        im.save(os.path.join(mydir, f"allofthem/{i}.png"))
        recom = vaporizer.compress(im, optimize=optimize) + (not optimize and b'~~' or b'')
        if recom == vapor:
            continue
        print(f"{i} is not the same")
        #print([li for li in difflib.ndiff(vapor.decode("utf-8"), recom.decode("utf-8")) if not li.startswith(" ")])
        print(len(vapor), len(recom))
        with open(os.path.join(mydir, f"allofthem/{i:02}_r.bin"), "wb") as f:
            f.write(recom)
        with vaporizer.decompress(recom) as imx:
            imx.save(os.path.join(mydir, f"allofthem/{i}_r.png"))
            with PIL.ImageChops.difference(im, imx) as imd:
                if imd.getbbox():
                    imd.save(os.path.join(mydir, f"allofthem/{i}_d.png"))
                else:
                    print(f"no diff in both decompression output according to PIL")