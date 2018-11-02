import numpy as np
import scipy
import scipy.interpolate as interpolate
from scipy.ndimage import gaussian_filter
from scipy.ndimage.filters import gaussian_filter1d
from scipy.signal import hilbert
from .videoData import VideoData
from .f_peakdetect import peakdetect
from .f_pixel import f_pixel_mean, f_pixel_phase

from phaseMap import PhaseMap

class PhaseMapFTDT( PhaseMap ):

    def __init__(self, vmem, v_mean, dt, width = 128, sigma_t = 1):
        
        super(PhaseMap, self).__init__(vmem, width)
        self.v_mean  = v_mean 
                
        V = vmem.data[:,::self.shrink,::self.shrink]
        # temporal filtering
        if sigma_t > 1:
            V = np.apply_along_axis(gaussian_filter1d, 0, V, sigma = sigma_t)
        
        V_x = np.zeros_like(V)
        V_y = np.zeros_like(V)
        V_x[:dt,:,:] = 1
        V_x[:dt,:,:] = 0
        V_x[dt:,:,:] = V[:-dt,:,:] - self.v_mean
        V_y[dt:,:,:] = V[ dt:,:,:] - self.v_mean
        V_comp = V_x + 1j * V_y
        self.data = np.angle(V_comp)
        self.data *= self.roi

        return
