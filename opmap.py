import numpy as np
from glob import glob
import os
import matplotlib.pyplot as plt
from cmap_bipolar import bipolar
from scipy import signal, ndimage
from scipy.interpolate import interp1d, splrep, splev


class VideoData(object):
    
    def __init__(self, length, height, width ):
        self.data = np.zeros((length, height, width), dtype=np.float32)
        self.roi = np.ones( ( height, width), dtype=np.float32 )
        self.vmin =  0.0
        self.vmax = 1.0
        self.cmap = 'hot'
    
    def showFrame(self, frame):
        assert frame >= 0 and frame < self.data.shape[0]
        plt.imshow(self.data[frame, :, :], vmin=self.vmin, vmax=self.vmax, cmap=self.cmap)
    
    def showROI(self):
        plt.imshow(self.roi, vmin=0.0, vmax=1.0, cmap='gray')
        
    def saveImage(self, savedir, img_type = 'png'):
        if not os.path.exists(savedir):
            os.mkdir(savedir)
        for frame in range(self.data.shape[0]):
            plt.imsave(
                '{0}/{1:0>6}.{2}'.format(savedir, frame, img_type), 
                self.data[frame, :, :], vmin=self.vmin, vmax=self.vmax, cmap=self.cmap
            )
        plt.imsave(
         '{0}/roi.{1}'.format(savedir, img_type), 
            self.roi, vmin=0.0, vmax=1.0, cmap='gray'
        )
    
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
        

class VmemMap( VideoData ):
    
    def __init__(self, path, cam_type, image_width, image_height, frame_start, frame_end, range_min, range_max ):
    
        postfix = {'sa4' : 'raww'}

        self.files = glob(path+"/*."+postfix[cam_type])
        self.files = sorted(self.files)[frame_start:frame_end]
        
        super(VmemMap, self).__init__(len(self.files), image_height, image_width)

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
        
        self.vmin = -1.0
        self.vmax = 1.0
        self.cmap = bipolar(neutral=0, lutsize=1024)        
        return
    
    def smooth(self, size):
        assert size > 0
        for frame in range( self.data.shape[0]):
            self.data[frame,:,:] = ndimage.gaussian_filter(self.data[frame,:,:], sigma = size)
        return
        
class PhaseMap( VideoData ):
    
    def __init__(self, vmem, shrink = 4, fs = 1000.0, cutoff = 20.0):
        
        self.shrink = shrink
        size_org = vmem.data.shape
        
        super(PhaseMap, self).__init__(size_org[0],size_org[1]/shrink, size_org[2]/shrink)
        
        nyq = fs/2.0
        fe = cutoff / nyq   # Cut off frequency : 20Hz
        numtaps = 15  # Filter size
        b = signal.firwin(numtaps, fe) # Low pass filter
        
        for n in range(self.data.shape[1]):
            for m in range(self.data.shape[2]):
                n_ = n*shrink
                m_ = m*shrink       
                try:
                    assert vmem.roi[n_, m_] > 0
                    data = vmem.data[ :, n_, m_]
                    data_an = signal.lfilter(b, 1, data)
                    data_max = np.max(data_an)
                    data_min = np.min(data_an)
                    assert data_max > data_min
                    data_an  = 2.0 * (data_an - data_min) / (data_max - data_min) - 1.0
                    self.data[:, n, m] = np.angle(signal.hilbert(data_an))
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
                    diff = signal.medfilt2d(difference, kernel_size=size*2+1)[size,size]
                    new_data[frame, n, m] = phaseComplement( base +  diff)
                    #new_data[frame, n, m] = phaseComplement( base + np.mean(difference.flatten()) )
        self.data = new_data
        
    def plot(self, points, start=None, end=None, filter_size=None, savepath = None):
        points = ( np.array(points) / float(self.shrink)).astype(np.int8)
        super(PhaseMap, self).plot(points, start, end, filter_size, savepath)
        
        