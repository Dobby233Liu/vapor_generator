import glob
import os.path

codes = []
mydir = os.path.dirname(os.path.realpath(__file__))
for i in glob.iglob(os.path.join(mydir, "allofthem", "*.bin")):
    if i.endswith("_r.bin"):
        continue
    if os.path.exists(i.replace(".bin", "_r.bin")):
        i = i.replace(".bin", "_r.bin")
    print(i)
    with open(i, "rb") as f:
        codes.append(f.read().decode("utf-8"))

with open(os.path.join(mydir, "allofthem", "scr_newvapordata.gml"), "w") as f:
    for i, c in enumerate(codes):
        f.write(f'if (argument0 == {i})\n    mydata = "')
        f.write(c.replace("\\", "\\\\"))
        f.write('"\n')