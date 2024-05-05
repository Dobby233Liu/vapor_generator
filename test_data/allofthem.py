import vapor_generator.new_vaporizer
import os.path
import io

mydir = os.path.dirname(os.path.realpath(__file__))

allvapor = []
with open(os.path.join(mydir, "allofthem.txt"), "r", encoding="utf-8") as all_dat:
    all_dat_l = all_dat.readlines()
    all_dat_l.reverse()
    allvapor = map(lambda x: x.encode("ascii"), all_dat_l)

for i, vapor in enumerate(allvapor):
    with vapor_generator.new_vaporizer.decompress(vapor) as im:
        im.save(os.path.join(mydir, f"allofthem/{i}.png"))