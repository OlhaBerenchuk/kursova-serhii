import pdoc
import os

libpath = os.path.abspath('doc')
print(libpath)
mod = pdoc.import_module('app')
doc = pdoc.Module(mod)
string = doc.html()

with open(os.path.join(libpath, "appp.html"), "w") as f:
    f.write(string)
