import sys
import os
from opmap.opmap import VmemMap
import json

if len(sys.argv) != 2:
    print('Please enter diredtory name')
    exit()

with open("experiment.json", "r") as f : params = json.load(f)
param_vmem = params["basic"]
diff_min = params["option"]["diff_min"]
smooth_size = params["option"]["smooth_size"]

dir_name = sys.argv[1]
param_vmem["path"] = dir_name

vmem = VmemMap(**param_vmem)
vmem.setDiffRange(diff_min=diff_min)
if smooth_size > 0 : vmem.smooth(size=smooth_size)

vmem.saveMovie(dir_name+"/vmem.mp4")
