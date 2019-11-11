import numpy as np
import cupy as xp
import os, shutil
import matplotlib.pyplot as plt
import scipy
from scipy.ndimage import gaussian_filter
from scipy.ndimage.filters import gaussian_filter1d
from util import makeMovie

class VideoData(object):

    def __init__(self, length, height, width ):
        self.data = xp.zeros((length, height, width), dtype=np.float32)
        self.roi = xp.ones( ( height, width), dtype=np.float32 )
        self.vmin =  0.0
        self.vmax = 1.0
        self.cmap = 'hot'

    def showFrame(self, frame):
        assert frame >= 0 and frame < self.data.shape[0]
        plt.imshow( xp.asnumpy(self.data[frame, :, :]) , vmin=self.vmin, vmax=self.vmax, cmap=self.cmap)

    def setRectROI(self, top=None, bottom=None, left=None, right=None):
        if top is not None :
            assert top >= 0 and top < self.roi.shape[0]
            self.roi[:top, :] = 0
        if bottom is not None :
            assert bottom >= 0 and bottom < self.roi.shape[0]
            self.roi[bottom:, :] = 0
        if left is not None :
            assert left >= 0 and left < self.roi.shape[1]
            self.roi[:, :left] = 0
        if right is not None :
            assert right >= 0 and right < self.roi.shape[1]
            self.roi[:, right:] = 0
        self.data *= self.roi

    def setIntROI(self, val_min=None, val_max=None):
        if val_min is not None:
            self.roi *= (xp.min(self.data, axis=0)>val_min)*1
        if val_max is not None:
            self.roi *= (xp.max(self.data, axis=0)<val_max)*1
        self.data *= self.roi
    
    def morphROI(self, closing=None, erosion=None):
        if closing : 
            self.roi = xp.asarray(scipy.ndimage.binary_closing(
                xp.asnumpy(self.roi), 
                structure=np.ones((closing,closing))).astype(self.roi.dtype
            ))
        if erosion : 
            self.roi = xp.asarray(scipy.ndimage.binary_erosion(
                xp.asnumpy(self.roi), 
                structure=np.ones((erosion,erosion))).astype(self.roi.dtype
            ))
        self.data *= self.roi

    def showROI(self):
        plt.imshow(xp.asnumpy(self.roi), vmin=0.0, vmax=1.0, cmap='gray')

    def saveImage(self, savedir, img_type = 'png', skip=1):
        if not os.path.exists(savedir):
            os.makedirs(savedir)
        for frame in range(self.data.shape[0]):
            if frame % skip == 0:
                plt.imsave(
                    '{0}/{1:0>6}.{2}'.format(savedir, int(frame/skip), img_type),
                    xp.asnumpy(self.data[frame, :, :]), vmin=self.vmin, vmax=self.vmax, cmap=self.cmap
                )
        plt.imsave(
         '{0}/roi.{1}'.format(savedir, img_type),
         xp.asnumpy(self.roi), vmin=0.0, vmax=1.0, cmap='gray'
        )
        
    def saveMovie(self, save_path, skip=1):
        savedir = './temp_mov'
        if os.path.exists(savedir):
            shutil.rmtree(savedir)
        self.saveImage(savedir, skip=skip)
        makeMovie(savedir)
        shutil.move(savedir+'.avi', save_path)
        
    def plot(self, points, start=None, end=None, filter_size=None, savepath = None):
        if start is None : start = 0
        if end is None : end = self.data.shape[0]
        fig = plt.figure()
        for i, p in enumerate(points):
            assert len(p) == 2
            x, y = p
            assert y >= 0 and y < self.data.shape[1]
            assert x >= 0 and x < self.data.shape[2]
            ax = fig.add_subplot(len(points),1,i+1)
            ts = xp.asnumpy(self.data[start:end, y, x])
            if filter_size is not None:
                ts = scipy.signal.savgol_filter(ts, filter_size, 3)
            ax.plot(ts)
        if savepath is None:
            plt.show()
        else:
            plt.savefig(savepath)

    def smooth_xy(self, size):
        assert size > 0
        self.data = xp.asarray( [ gaussian_filter(im, sigma = size) for im in xp.asnumpy(self.data)])
        self.data *= self.roi
        return

    def smooth_t(self,size):
        assert size > 0
        self.data = xp.asarray( gaussian_filter1d( xp.asnumpy(self.data), size, axis=0) )
        return

    def shrink_xy(self,interval):
        assert interval > 0
        self.data = self.data[:,::interval,::interval]
        self.roi = self.roi[::interval,::interval]
        return
