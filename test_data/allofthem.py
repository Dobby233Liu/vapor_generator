import vapor_generator.new_vaporizer as vaporizer
import os.path
import io
import PIL.ImageChops
import difflib

mydir = os.path.dirname(os.path.realpath(__file__))

allvapor = []
with open(os.path.join(mydir, "allofthem.txt"), "r", encoding="utf-8") as all_dat:
    all_dat_l = all_dat.readlines()
    all_dat_l.reverse()
    allvapor = map(lambda x: x.rstrip().encode("ascii"), all_dat_l)

for i, vapor in enumerate(allvapor):
    with vaporizer.decompress(vapor) as im:
        im.save(os.path.join(mydir, f"allofthem/{i}.png"))
        recom = vaporizer.compress(im) + b'~~'
        if recom == vapor:
            continue
        print(f"{i} is not the same")
        print([li for li in difflib.ndiff(vapor.decode("utf-8"), recom.decode("utf-8")) if not li.startswith(" ")])
        with vaporizer.decompress(recom) as imx:
            imx.save(os.path.join(mydir, f"allofthem/{i}_r.png"))
            with PIL.ImageChops.difference(im, imx) as imd:
                if imd.getbbox():
                    imd.save(os.path.join(mydir, f"allofthem/{i}_d.png"))
                else:
                    print(f"but pixel-perfect according to our decompressor")