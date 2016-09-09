import sys
import os
from opmap.opmap import VmemMap, RawCam
import json

with open("experiment.json", "r") as f : params = json.load(f)
param_vmem = params["basic"]
diff_min = params["option"]["diff_min"]
smooth_size = params["option"]["smooth_size"]
interval_time = params["option"]["interval"]
flg_plot = True if params["option"]["plot"] > 0 else False
saveDir = param_vmem["path"]+"/result/"

if not os.path.exists(saveDir):
	os.makedirs(saveDir)

cam = RawCam(**param_vmem)
vmem = VmemMap(cam)
vmem.setDiffRange(diff_min=diff_min)
if smooth_size > 0 : vmem.smooth(size=smooth_size)
vmem.saveMovie(saveDir + "vmem.mp4", interval=interval_time)
if flg_plot:
	points = cam.selectPoints(saveDir+"selectPoints.png")
	vmem.plot(points, savepath = saveDir + "plot.png")

