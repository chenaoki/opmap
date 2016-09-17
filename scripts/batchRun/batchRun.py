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
	
	saveDir = a.replace("ExperimentData", "AnalysisResult")
	print saveDir

	param_cam["path"] = a
	rawcam = RawCam(**param_cam)
	vmem = VmemMap(rawcam)

        vmem.setDiffRange(diff_min=diff_min)

        if True:
            import matplotlib.pyplot as plt
            plt.imsave(
             '{0}/roi.png'.format(savedir),
                vmem.roi, vmin=0.0, vmax=1.0, cmap='gray'
            )
            break

        if smooth_size > 0 : vmem.smooth(size=smooth_size)
	
	pmap = PhaseMap(vmem)
	pvmap = PhaseVarianceMap(pmap)

	vmem.saveImage(saveDir+'/vmem')	
	pmap.saveImage(saveDir+'/pamp')	
	pvmap.saveImage(saveDir+'/pvmap')	
