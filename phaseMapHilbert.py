import numpy as np
import cupy as xp
import scipy
import scipy.interpolate as interpolate
from scipy.ndimage import gaussian_filter
from scipy.ndimage.filters import gaussian_filter1d
from scipy.signal import hilbert
from numba import double
from numba.decorators import jit, autojit
from numba import cuda
from videoData import VideoData
from f_peakdetect import peakdetect
from f_pixel import f_pixel_mean, f_pixel_phase

from phaseMap import PhaseMap

class PhaseMapHilbert( PhaseMap ):

    def __init__(self, vmem, width = 128, sigma_xy = 32, sigma_t = 5):
        
        super(PhaseMapHilbert, self).__init__(vmem, width)
                
        V = xp.asnumpy(vmem.data[:,::self.shrink,::self.shrink])
        
        im_mean = np.mean(V, axis=0)
        if sigma_xy > 1:
            im_mean = np.array([gaussian_filter(im, sigma=sigma_xy) for im in im_mean])
        
        Vamp = V-im_mean
        if sigma_t > 1:
            Vamp = gaussian_filter1d(Vamp, sigma=sigma_t, axis=0)
        
        self.data = xp.asarray(np.apply_along_axis(f_pixel_phase, 0, arr=Vamp))
        self.data *= self.roi

        return
