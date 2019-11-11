import numpy as np
import cupy as xp
import scipy
from videoData import VideoData

class PhaseVarianceMap( VideoData ):

    def __init__(self, phasemap, size = 9):
        assert size > 0
        self.size = size

        super(PhaseVarianceMap, self).__init__(*phasemap.data.shape)
        kernel = np.ones((size, size), dtype=np.float32)
        kernel /= np.sum(kernel)

        for frame in range(self.data.shape[0]):
            im_cos = np.cos(xp.asnumpy(phasemap.data[frame,:,:]))
            im_sin = np.sin(xp.asnumpy(phasemap.data[frame,:,:]))
            im_cos = scipy.signal.convolve2d(im_cos, kernel, mode = 'same', boundary = 'fill')
            im_sin = scipy.signal.convolve2d(im_sin, kernel, mode = 'same', boundary = 'fill')
            self.data[frame, :, :] = xp.asarray(1.0 - np.abs( im_cos + 1j * im_sin ))

        self.roi = xp.copy(phasemap.roi)
        self.roi = xp.asarray(
                scipy.ndimage.binary_erosion(
                    xp.asnumpy(self.roi), 
                    structure=np.ones((size,size))
                )).astype(phasemap.roi.dtype)
        self.data *= self.roi

        self.vmin = 0.0
        self.vmax = 1.0
        self.cmap = 'gray'


