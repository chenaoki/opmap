import os
import numpy as np
from .xp_auto import xp
from .cmap import bipolar
from .videoData import VideoData
from .f_pixel import f_pixel_activation
import matplotlib.pyplot as plt

class ActivationMap( VideoData ):

    def __init__(self, vmem, frame_max, frame_min=0, interval=5, thre_up=0.5, thre_down=0.4, bg_image=None):
        shape = vmem.data.shape
        super().__init__(shape[0], shape[1], shape[2])
        self.roi = xp.copy(vmem.roi)
        self.bg_image = np.zeros(shape[1:])
        if not bg_image is None:
            assert self.bg_image.shape == bg_image.shape
            self.bg_image = bg_image
        
        self.data = xp.asarray(np.apply_along_axis(f_pixel_activation, 0, vmem.data, thre_up=thre_up, thre_down=thre_down))        
        self.data = self.data*self.roi

        self.vmin = frame_min
        self.vmax = frame_max
        self.interval = interval
        self.cmap = "jet_r"
        return
    
    def showFrame(self, frame, show_colorbar=True):
        assert frame >= 0 and frame < self.data.shape[0]
        plt.contour(xp.asnumpy(self.data[frame]), cmap=self.cmap, levels=np.arange(self.vmin, self.vmax, self.interval))
        if show_colorbar and frame > self.interval:
            plt.colorbar()
        plt.imshow(xp.asnumpy(self.bg_image), cmap="gray")
    
    def saveImage(self, savedir, dpi=None, img_type = 'png', skip=1, show_colorbar=False):
        if not os.path.exists(savedir):
            os.makedirs(savedir)
        for frame in range(self.data.shape[0]):
            if (frame + 1) % skip == 0:
                plt.clf()
                self.showFrame(frame, show_colorbar=show_colorbar)
                plt.savefig(
                    '{0}/{1:0>6}.{2}'.format(savedir, int(frame/skip), img_type), dpi=dpi
                )
        plt.imsave(
         '{0}/roi.{1}'.format(savedir, img_type),
         xp.asnumpy(self.roi), vmin=0.0, vmax=1.0, cmap='gray'
        )
        plt.close()