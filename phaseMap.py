import numpy as np
import scipy
import scipy.interpolate as interpolate
from scipy.ndimage import gaussian_filter
from scipy.ndimage.filters import gaussian_filter1d
from scipy.signal import hilbert
from .videoData import VideoData
from .f_peakdetect import peakdetect

class PhaseMap( VideoData ):

    def __init__(self, vmem, width = 128, sigma_mean = 32, sigma_t = 5):
        
        shrink = int(vmem.data.shape[2] / width)
        self.shrink = shrink
        size_org = vmem.data.shape

        super(PhaseMap, self).__init__(size_org[0],size_org[1]//shrink, size_org[2]//shrink)
        

        def f_pixel_mean(ts):
            try:    
                peaks, bottoms = peakdetect(ts, lookahead=50)
                peaks = np.array(peaks)
                bottoms = np.array(bottoms)
                start = np.array([[0, ts[0]]])
                end = np.array([[len(ts), ts[-1]]])
                peaks_ = np.concatenate((start,peaks, end))
                bottoms_ = np.concatenate((start,bottoms, end))

                f = interpolate.interp1d(peaks_[:,0], peaks_[:,1], kind="linear")
                _peaks_ = f(np.arange(len(ts)))
                f = interpolate.interp1d(bottoms_[:,0], bottoms_[:,1], kind="linear")
                _bottoms_ = f(np.arange(len(ts)))

                mean = (_peaks_+_bottoms_)/2
                return mean

            except:
                return np.ones_like(ts)*np.mean(ts)

        def f_pixel_phase(ts):
            return np.angle(hilbert(gaussian_filter1d(ts, sigma=sigma_t)))
        
        V = vmem.data[:,::shrink,::shrink]
        Vmean = np.apply_along_axis(f_pixel_mean, 0, V)        
        for frame in range(len(Vmean)):
            Vmean[frame,:,:] = gaussian_filter(Vmean[frame,:,:], sigma = sigma_mean)
        self.data = np.apply_along_axis(f_pixel_phase, 0, V - Vmean)

        self.roi = np.array(vmem.roi[::shrink, ::shrink])
        self.data *= self.roi

        self.vmin = -np.pi
        self.vmax = np.pi
        self.cmap = 'jet'
        return
    
    def smooth(self, size = 5):
        for frame in range( self.data.shape[0]):
            img_cos = np.cos(self.data[frame, :,:]) 
            img_sin = np.sin(self.data[frame, :,:]) 
            img_cos = scipy.ndimage.filters.uniform_filter(img_cos, size=size, mode='constant')
            img_sin = scipy.ndimage.filters.uniform_filter(img_sin, size=size, mode='constant')
            self.data[frame,:,:] = np.angle(img_cos+1j*img_sin)

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

