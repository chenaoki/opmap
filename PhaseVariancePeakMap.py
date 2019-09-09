import numpy as np
import scipy
import math
from videoData import VideoData

class PhaseVariancePeakMap( VideoData ):
    vmin = 0
    cmap = 'gray'
    
    @classmethod
    def load(cls, npy_path):
        data = np.load(npy_path)
        assert len(data.shape) == 3
        L,H,W = data.shape
        obj = VideoData(1,1,1)
        obj.data = data
        obj.vmin = cls.vmin
        obj.vmax = np.max(data)
        obj.cmap = cls.cmap
        return obj

    def __init__(self, pvmap, threshold=None):
        if threshold is not None:
            assert threshold >= 0.0 and threshold <= 1.0
            self.threshold = threshold
        else:
            self.threshold = 1 - math.sqrt( -math.log(0.05) / ( pvmap.size**2) )

        super(PhaseVariancePeakMap, self).__init__(*pvmap.data.shape)

        self.roi = pvmap.roi
        self.data_label, self.coreNum = scipy.ndimage.label((pvmap.data>self.threshold)*1) 
        self.data = ( self.data_label > 0 ) * 1

        #self.vmin =  cls_vmin
        self.vmax = np.max(self.data) 
        #self.cmap = cls_cmap


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

