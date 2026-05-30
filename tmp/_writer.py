import pathlib,sys,base64
x=base64.b64decode(pathlib.Path(chr(100)+chr(58)+chr(47)+"bskyhygiene/tmp/_b64payload.txt").read_text()).decode()
pathlib.Path(chr(100)+chr(58)+chr(47)+"bskyhygiene/tmp/cofollow_hunter.py").write_text(x)
print(len(x),"bytes")
