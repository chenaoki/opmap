import numpy as np
from glob import glob
import cv2
import scipy
import matplotlib.pyplot as plt
from VideoData import VideoData

class CoreMap( VideoData ):

  def __init__(self, pvmap, threshold=0.8):
    assert threshold >= 0.0 and threshold <= 1.0
    self.threshold = threshold

    super(CoreMap, self).__init__(*pvmap.data.shape)

    self.roi = pvmap.roi
    self.data, self.coreNum = scipy.ndimage.label((pvmap.data>self.threshold)*1) 

    self.vmin = 0
    self.vmax = np.max(self.data) 
    self.cmap = plt.cm.spectral 

  def getCoreLog(self):
    log_core = []
    for frame in range(self.data.shape[0]):
      im_label = self.data[frame,:,:]
      im_bin = (im_label>0)*1
      im_label_tmp, n = scipy.ndimage.label(im_bin)
      coms = scipy.ndimage.measurements.center_of_mass(im_bin, im_label_tmp, range(1,n+1))
      for i in range(1, n+1):
        label=np.max(((im_label_tmp==i)*1)*im_label)
        log_core.append((frame, label, coms[i-1][0], coms[i-1][1]))
    return log_core 

