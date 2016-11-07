import numpy as np
import os
import scipy
from scipy.signal import firwin
from scipy.interpolate import interp1d
from VideoData import VideoData

class PhaseMap( VideoData ):

    def __init__(self, vmem, shrink = 4, fs = 1000.0, fe = [2.0, 20.0] ):

        self.shrink = shrink
        size_org = vmem.data.shape

        super(PhaseMap, self).__init__(size_org[0],size_org[1]/shrink, size_org[2]/shrink)

        nyq = fs/2.0
        fe = np.array(fe) / nyq   # Cut off frequency : 20Hz
        numtaps = 127  # Filter size
        b = firwin(numtaps, fe, pass_zero=(len(fe)<2)) # Low pass or band pass filter
        
        def f_pixelwise(src):
            dst = np.zeros_like(src)
            for n in range(src.shape[1]):
                for m in range(src.shape[2]):
                    y = src[ :, n, m]
                    y = scipy.signal.lfilter(b, 1, y)[numtaps/2:]
                    y -= np.mean(y)
                    y_ = np.r_[y, np.zeros(numtaps/2)]
                    dst[:, n, m] = np.angle(scipy.signal.hilbert(y_))
            return dst
        self.data = f_pixelwise(vmem.data[:, ::shrink, ::shrink])

        self.roi = np.array(vmem.roi[::shrink, ::shrink])
        self.data *= self.roi

        self.vmin = -np.pi
        self.vmax = np.pi
        self.cmap = 'jet'
        return
    
    def smooth(self, size = 5):
        C = np.cos(self.data) + 1j*np.sin(self.data)
        for frame in range( self.data.shape[0]):
            img = C[frame, :, :]
            self.data[frame,:,:] = np.angle(scipy.ndimage.filters.uniform_filter(img, size=size, mode='const'))

    def smooth_median(self, size = 4):
        assert size > 0
        def phaseComplement(value):
            value -= (value > np.pi)*2*np.pi
            value += (value < - np.pi)*2*np.pi
            return value
        new_data = np.zeros_like(self.data)
        for frame in range( self.data.shape[0]):
            if frame % 10 == 0 : print frame
            for n in range(self.data.shape[1])[size:-size]:
                for m in range(self.data.shape[2])[size:-size]:
                    base = self.data[frame, n, m]
                    target = self.data[frame, n-size:n+size+1, m-size:m+size+1]
                    difference = phaseComplement(target-base)
                    diff = scipy.signal.medfilt2d(difference, kernel_size=size*2+1)[size,size]
                    new_data[frame, n, m] = phaseComplement( base +  diff)
                    #new_data[frame, n, m] = phaseComplement( base + np.mean(difference.flatten()) )
        self.data = new_data

