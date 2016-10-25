import numpy as np
import os
import scipy
from VideoData import VideoData

class PhaseMap( VideoData ):

    def __init__(self, vmem, shrink = 4, fs = 1000.0, cutoff = 20.0):

        self.shrink = shrink
        size_org = vmem.data.shape

        super(PhaseMap, self).__init__(size_org[0],size_org[1]/shrink, size_org[2]/shrink)

        nyq = fs/2.0
        fe = cutoff / nyq   # Cut off frequency : 20Hz
        numtaps = 15  # Filter size
        b = scipy.signal.firwin(numtaps, fe) # Low pass filter

        for n in range(self.data.shape[1]):
            for m in range(self.data.shape[2]):
                n_ = n*shrink
                m_ = m*shrink
                try:
                    assert vmem.roi[n_, m_] > 0
                    data = vmem.data[ :, n_, m_]
                    data_an = scipy.signal.lfilter(b, 1, data)
                    data_max = np.max(data_an)
                    data_min = np.min(data_an)
                    assert data_max > data_min
                    data_an  = 2.0 * (data_an - data_min) / (data_max - data_min) - 1.0
                    self.data[:, n, m] = np.angle(scipy.signal.hilbert(data_an))
                    self.roi[n, m] = 1.0
                except:
                    self.data[:, n, m] = 0.0
                    self.roi[n, m] = 0.0

        self.vmin = -np.pi
        self.vmax = np.pi
        self.cmap = 'jet'
        return

    def smooth(self, size = 4):
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

