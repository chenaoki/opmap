import sys
import os
from opmap.opmap import VmemMap, RawCam,PhaseMap,PhaseVarianceMap
import json
import glob

if len(sys.argv) < 2:
	print 'Usage : ',
	print 'python batchRun.py [target directory]'
	exit()

p = sys.argv[1]
dirs = glob.glob(p+"/*")

for a in dirs:

	with open("param.json", "r") as f : params = json.load(f)
	param_cam = params["basic"]
	diff_min = params["option"]["diff_min"]
	smooth_size = params["option"]["smooth_size"]
	interval_time = params["option"]["interval"]
	flg_plot = True if params["option"]["plot"] > 0 else False
	flg_imsave = True if params["option"]["save_image"] > 0 else False
	
	saveDir = a.replace("ExperimentData", "AnalysisResult")
	print saveDir

	param_cam["path"] = a
	rawcam = RawCam(**param_cam)
	vmem = VmemMap(rawcam)
	
	pmap = PhaseMap(vmem)
	pvmap = PhaseVarianceMap(pmap)

	vmem.saveImage(saveDir+'/vmem')	
	pmap.saveImage(saveDir+'/pamp')	
	pvmap.saveImage(saveDir+'/pvmap')	
