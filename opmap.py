import numpy as np
from glob import glob
import os
import matplotlib.pyplot as plt
from cmap_bipolar import bipolar
from scipy import signal, ndimage
from scipy.interpolate import interp1d, splrep, splev

def Smooth(V, time = None, image = None):
    assert time is not None or image is not None
    assert time is None or time > 0 
    assert image is None or image > 0
    assert len(V.shape) == 3
    if time is not None:
        for i in range( V.shape[1]):
            for j in range( V.shape[2]):
                V[:, i, j] = signal.savgol_filter(V[:, i, j], time, 3)
    if image is not None:
        for frame in range( V.shape[0]):
            V[frame,:,:] = ndimage.gaussian_filter(V[frame,:,:], sigma = image)
    return V
    

def SaveImage(V, savedir, vmin=-1.0, vmax=1.0, cmap='hot', img_type = 'png'):
    assert len(V.shape) == 3
    if not os.path.exists(savedir):
        os.mkdir(savedir)
    for frame in range(V.shape[0]):
        plt.imsave(
            '{0}/{1:0>6}.{2}'.format(savedir, frame, img_type), 
            V[frame, :, :], vmin=vmin, vmax=vmax, cmap=cmap
        )
    
class VmemMap( object ):
    
    def __init__(self, path, cam_type, image_width, image_height, frame_start, frame_end, range_min, range_max ):
    
        postfix = {'sa4' : 'raww'}

        self.files = glob(path+"/*."+postfix[cam_type])
        self.files = sorted(self.files)[frame_start:frame_end]

        self.data = np.zeros((len(self.files), image_width, image_height), dtype=np.float32)

        if cam_type == 'sa4':
            for i, f in enumerate(self.files):
                im = np.fromfile(f, dtype=np.ushort).reshape(image_height, image_width)
                self.data[i, :,:] = im
                
        im_max = np.max(self.data, axis=0)
        im_min = np.min(self.data, axis=0)
        im_range = (im_max - im_min) + (im_max == im_min) * 1
        
        self.roi = ( (im_range > range_min) * 1 ) * ((im_range < range_max)  * 1)
        self.data = 2.0 * (im_max - self.data ) / im_range - 1.0
        self.data *= self.roi
        
        pass
    
    def showFrame(self, frame):
        assert frame >= 0 and frame < self.data.shape[0]
        print self.files[frame]
        plt.imshow(self.data[frame, :, :], vmin=-1.0, vmax=1.0, cmap=bipolar(neutral=0, lutsize=1024))
    
    def saveImage(self, savedir):
        SaveImage(
            self.data, savedir, vmin=-1.0, vmax=1.0, 
            cmap=bipolar(neutral=0, lutsize=1024)
        )
        pass
    
    def plot(self, points, start=None, end=None, filter_size=None, savepath = None):
        if start is None : start = 0
        if end is None : end = self.data.shape[0]
        for i, p in enumerate(points):
            assert len(p) == 2
            x, y = p
            assert y >= 0 and y < self.data.shape[1]
            assert x >= 0 and x < self.data.shape[2]
            plt.subplot(len(points),1,i+1)
            ts = self.data[start:end, y, x]
            if filter_size is not None:
                ts = signal.savgol_filter(ts, filter_size, 3)
            plt.plot(ts)
        if savepath is None:
            plt.show()
        else:
            plt.savefig(savepath)
        
    def smooth(self, time = None, image = None):
        self.data = Smooth(self.data, time=time, image = image)
        
