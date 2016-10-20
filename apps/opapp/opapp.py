import sys, os, json, glob
import matplotlib.pyplot as plt
import cv2
import numpy as np

from opmap.opmap import VmemMap, RawCam,PhaseMap,PhaseVarianceMap, CoreMap, makeMovie
from opmap.cmap_bipolar import bipolar

if len(sys.argv) < 2:
  print 'Usage : ',
  print 'python {0} [target directory]'.format(sys.argv[0])
  exit()

with open("param.json", "r") as f : params = json.load(f)
param_cam     = params.get("basic",{})
menu_list     = params.get("menu",{})
param_opt     = params.get("option",{})
roi_rect      = param_opt.get("roi_rect",None)
diff_min      = param_opt.get("diff_min",0)
intensity_min = param_opt.get("intensity_min",0)
smooth_size   = param_opt.get("smooth_size",9)
threshold     = param_opt.get("core_thre",0.6)
pv_win        = param_opt.get("pv_win",9)
save_int      = param_opt.get("save_int",1)
p_min         = param_opt.get("phase_min",-0.6*np.pi)
p_max         = param_opt.get("phase_max", 0.6*np.pi)
p_d           = param_opt.get("phase_mergin", 0.1 *np.pi)

path = sys.argv[1]
param_cam["path"] = path
saveDir = path.replace("ExperimentData", "AnalysisResult")
if not os.path.exists(saveDir):
  os.makedirs(saveDir)
print saveDir


if menu_list["cam"] == 0 : exit()
print "RawCam..."
rawcam = RawCam(**param_cam)
if roi_rect is not None : rawcam.setRectROI(**roi_rect)
if intensity_min > 0 : rawcam.setIntROI(val_min=intensity_min)
rawcam.morphROI(closing=10)
rawcam.morphROI(erosion=10)
if menu_list["cam"] > 1:
  rawcam.saveImage(saveDir+'/cam', skip=save_int)
print "done",

if menu_list["vmem"] == 0 : exit()
print "VmemMap..."
vmem = VmemMap(rawcam)
if diff_min > 0 : vmem.setDiffRange(diff_min=diff_min)
vmem.morphROI(closing=10)
vmem.morphROI(erosion=10)
if smooth_size > 0 : vmem.smooth(size=smooth_size)
if menu_list["vmem"] in [2,3] : vmem.saveImage(saveDir+'/vmem', skip=save_int)
if menu_list["vmem"] == 3 : makeMovie(saveDir+'/vmem')
if menu_list["vmem"] == 4 : np.save(saveDir+'/vmem', vmem.data) 
print "done",

if menu_list["pmap"] == 0 : exit()
print "PhaseMap..."
pmap = PhaseMap(vmem)
if menu_list["pmap"] in [2,3] : pmap.saveImage(saveDir+'/pmap', skip=save_int)
if menu_list["pmap"] == 3 : makeMovie(saveDir+'/pmap')
if menu_list["pmap"] == 4 : np.save(saveDir+'/pmap', pmap.data) 
print "done",

if menu_list["pvmap"] == 0 : exit()
print "PhaseVarianceMap..."
pvmap = PhaseVarianceMap(pmap, size=pv_win)
if menu_list["pvmap"] in [2,3] : pvmap.saveImage(saveDir+'/pvmap', skip=save_int)
if menu_list["pvmap"] == 3 : makeMovie(saveDir+'/pvmap')
if menu_list["pvmap"] == 4 : np.save(saveDir+'/pvmap', pvmap.data) 
print "done",

if menu_list["core"] == 0 : exit()
print "CoreMap..."
coremap = CoreMap(pvmap, threshold=threshold)
if menu_list["core"] in [2,3] : coremap.saveImage(saveDir+'/core', skip=save_int)
if menu_list["core"] == 3 : makeMovie(saveDir+'/core')
if menu_list["core"] == 4 : np.save(saveDir+'/core', coremap.data)
if menu_list["core_log"] == 1 : np.savetxt(saveDir+'/core.log', coremap.getCoreLog())
print "done",

if menu_list["integrate"] == 0 : exit()
print "Integrate..."

s = coremap.data.shape
a = np.zeros([s[0],s[1],s[2],3])
cam_resize = np.zeros([s[0],s[1],s[2]])
vmem_resize = np.zeros([s[0],s[1],s[2]])

for f in range(s[0]):
  cam_resize[f,:,:] = cv2.resize( rawcam.data[f,:,:], (s[1],s[2]) )
  vmem_resize[f,:,:] = cv2.resize( vmem.data[f,:,:], (s[1],s[2]) )
cam_resize = cam_resize.astype(np.float32) / float(np.max(cam_resize))
img_vmem = (1.0+vmem_resize)*0.5
wf = ( ( pmap.data >= p_min - p_d )*1 ) * ( ( pmap.data <= p_min       )*1 )
rf = ( ( pmap.data >  p_min       )*1 ) * ( ( pmap.data <  p_max       )*1 )
wt = ( ( pmap.data >= p_max       )*1 ) * ( ( pmap.data <= p_max + p_d )*1 )
core = (coremap.data>0)*1

cmap = bipolar()
a = ( cmap(img_vmem)[:,:,:,:3] * 255 ).astype(np.uint8)[:,:,:,::-1]
a[:,:,:,1] = wf*255
a[:,:,:,0] = wt*255
for i, c in enumerate('rgb') : a[:,:,:,i] = core*255 + (1-core)*a[:,:,:,i]
for i, c in enumerate('rgb') : a[:,:,:,i] = a[:,:,:,i] * 0.7 + cam_resize * 255 * 0.3
for i, c in enumerate('rgb') : a[:,:,:,i] *= pmap.roi.astype(np.uint8)

if menu_list["integrate"] > 1 : 
  if not os.path.exists(saveDir+'/all'):
    os.makedirs(saveDir+'/all')
  for f in range(s[0]):
    img = np.array(a[f,:,:,:])
    cv2.putText(img, "{0:0>4}".format(f), (5,15), cv2.FONT_HERSHEY_PLAIN,.8,(255,255,255))
    cv2.imwrite(saveDir+'/all/{0:0>6}.png'.format(f), img)
if menu_list["integrate"] > 2 : makeMovie(saveDir+'/all', img_type='png')

print "done"
