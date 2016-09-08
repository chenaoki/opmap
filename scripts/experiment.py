import sys
import os
from opmap.opmap import VmemMap, RawCam
import json

if len(sys.argv) < 2 or len(sys.argv) > 3:
    print('Please check argument')
    exit()

with open("experiment.json", "r") as f : params = json.load(f)
param_vmem = params["basic"]
diff_min = params["option"]["diff_min"]
smooth_size = params["option"]["smooth_size"]
interval_time = params["option"]["interval"]

if len(sys.argv) == 2:
	dir_name = sys.argv[1]
else:
	dir_name = sys.argv[1]
	interval_time = int(sys.argv[2])
param_vmem["path"] = dir_name

cam = RawCam(**param_vmem)
vmem = VmemMap(cam)
vmem.setDiffRange(diff_min=diff_min)
if smooth_size > 0 : vmem.smooth(size=smooth_size)

vmem.saveMovie(dir_name+"/vmem.mp4", interval=interval_time)
