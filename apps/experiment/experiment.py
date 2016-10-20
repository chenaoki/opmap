import sys
import os
from opmap.opmap import VmemMap, RawCam, makeMovie
import json

def experiment(path, saveDir, param_file="param.json"):

    assert os.path.exists(path)
    if not os.path.exists(saveDir): os.makedirs(saveDir)
    
    with open("param.json", "r") as f : params = json.load(f)
    param_basic         = params["basic"]
    param_basic["path"] = path
    diff_min            = params["option"]["diff_min"]
    smooth_size         = params["option"]["smooth_size"]
    interval            = params["option"]["interval"]
    flg_plot            = (params["option"]["plot"] > 0)
    flg_map             = (params["option"]["map"]  > 0)

    print "Loading camera data...",
    cam = RawCam(**param_basic)
    print "done"

    print "Making vmem data...",
    vmem = VmemMap(cam)
    vmem.setDiffRange(diff_min=diff_min)
    if smooth_size > 0 : vmem.smooth(size=smooth_size)
    print "done"

    if flg_map:
            print "Saving images...",
            vmem.saveImage(saveDir + "/vmem", img_type = 'png', skip=interval)
            makeMovie(saveDir+"/vmem", img_type="png")
            print "done"
    if flg_plot:
            print "Plot start...",
            points = cam.selectPoints(saveDir+"selectPoints.png")
            vmem.plot(points, savepath = saveDir + "plot.png")
            print "done"
