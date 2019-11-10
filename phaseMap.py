import numpy as np
import cupy as xp
import scipy
import scipy.interpolate as interpolate
from scipy.ndimage import gaussian_filter
from scipy.ndimage.filters import gaussian_filter1d
from scipy.signal import hilbert
from videoData import VideoData

class PhaseMap( VideoData ):

    def __init__(self, vmem, width = 128):
        
        self.shrink = int(vmem.data.shape[2] / width)
        size_org = vmem.data.shape
        super(PhaseMap, self).__init__(size_org[0],size_org[1]//self.shrink, size_org[2]//self.shrink)
        self.roi = xp.array(vmem.roi[::self.shrink, ::self.shrink])
        self.vmin = -xp.pi
        self.vmax = xp.pi
        self.cmap = 'jet'
        return
    
    def smooth(self, size = 5):
        def framewise(im):
            img_cos = xp.asnumpy(xp.cos(im)) 
            img_sin = xp.asnumpy(xp.sin(im))
            img_cos = scipy.ndimage.filters.uniform_filter(img_cos, size=size, mode='constant')
            img_sin = scipy.ndimage.filters.uniform_filter(img_sin, size=size, mode='constant')
            return xp.asarray(np.angle(img_cos+1j*img_sin))
        self.data = xp.asarray([framewise(im) for im in self.data])

    def smooth_median(self, size = 4):
        assert size > 0
        def phaseComplement(value):
            value -= (value > np.pi)*2*np.pi
            value += (value < - np.pi)*2*np.pi
            return value
        new_data = np.zeros_like(self.data)
        for frame in range( self.data.shape[0]):
            if frame % 10 == 0 : print(frame)
            for n in range(self.data.shape[1])[size:-size]:
                for m in range(self.data.shape[2])[size:-size]:
                    base = self.data[frame, n, m]
                    target = self.data[frame, n-size:n+size+1, m-size:m+size+1]
                    difference = phaseComplement(target-base)
                    diff = scipy.signal.medfilt2d(difference, kernel_size=size*2+1)[size,size]
                    new_data[frame, n, m] = phaseComplement( base +  diff)
                    #new_data[frame, n, m] = phaseComplement( base + np.mean(difference.flatten()) )
        self.data = new_data

