# -*- coding: utf-8 -*-

import numpy as np
from .videoData import VideoData
from .f_pixel import f_pixel_apd

class APDMap( VideoData ):

    def __init__(self, vmem, width = 64, sigma_mean = 32, sigma_t = 5):
        
        shrink = int(vmem.data.shape[2] / width)
        self.shrink = shrink
        
        size_org = vmem.data.shape
        super(APDMap, self).__init__(size_org[0],size_org[1]//shrink, size_org[2]//shrink)

        V = vmem.data[:,::shrink,::shrink]
        self.data = (np.apply_along_axis(f_pixel_apd, 0, V)).astype(self.data.dtype)
        self.roi = np.array(vmem.roi[::shrink, ::shrink])
        self.data *= self.roi

        self.vmin = 0
        self.vmax = self.data.max()
        self.cmap = 'gray'
        return
