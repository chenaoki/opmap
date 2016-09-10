import opmap
import numpy as np
import copy
from scipy import signal
import cv2
import matplotlib.pyplot as plt
from opmap.opmap import RawCam, VmemMap, PhaseMap, PhaseVarianceMap
import json

with open("purkinje_param.json", "r") as f : params = json.load(f)
param_vmem = params["basic"]
purkinje_end = params["purkinje_end"]
saveDir = param_vmem["path"]+"/result/purkinje/"
bmp_file = param_vmem["path"] + "mask.bmp"


cam_org = RawCam(**param_vmem)
vmem_total = VmemMap(cam_org)

points = cam_org.selectPoints()
vmem_total.plot(points, savepath=(saveDir+"/waves.png"))