import sys
import os
from opmap.opmap import VmemMap, RawCam
import json

with open("param.json", "r") as f : params = json.load(f)
param_vmem = params["basic"]
diff_min = params["option"]["diff_min"]
smooth_size = params["option"]["smooth_size"]
interval_time = params["option"]["interval"]
flg_plot = True if params["option"]["plot"] > 0 else False
flg_imsave = True if params["option"]["save_image"] > 0 else False
saveDir = param_vmem["path"]+"/result/experiment/"

if not os.path.exists(saveDir+"img/"):
	os.makedirs(saveDir+"img/")

print "Loading camera data...",
cam = RawCam(**param_vmem)
print "done"

print "Making vmem data...",
vmem = VmemMap(cam)
vmem.setDiffRange(diff_min=diff_min)
if smooth_size > 0 : vmem.smooth(size=smooth_size)
print "done"

print "Saving movie...",
vmem.saveMovie(saveDir + "vmem.mp4", interval=interval_time)
print "done"

if flg_imsave:
	print "Saving images...",
	vmem.saveImage(saveDir + "img/", img_type = 'png')
	print "done"
if flg_plot:
	print "Plot start...",
	points = cam.selectPoints(saveDir+"selectPoints.png")
	vmem.plot(points, savepath = saveDir + "plot.png")
	print "done"
