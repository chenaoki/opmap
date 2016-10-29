import os
import numpy as np

def phase_add(a, b):
    a_ = np.cos(a) + np.sin(a)*1j
    b_ = np.cos(b) + np.sin(b)*1j
    return np.angle(a_*b_)

def makeMovie(path, img_type='png'):

    cmd = 'ffmpeg -r 15 -y -i "{0}/%06d.{1}" -c:v libx264 -pix_fmt yuv420p -qscale 0 "{0}.mp4"'.format(path, img_type)
    print cmd
    os.system(cmd)

