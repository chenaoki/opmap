# -*- coding: utf-8 -*-
import numpy as np
import scipy.interpolate as interpolate
from scipy.ndimage.filters import gaussian_filter1d
from scipy.signal import hilbert
from .f_peakdetect import peakdetect

def f_pixel_peaks(ts):
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
        
        return (_peaks_, _bottoms_)

    except:
        return (np.ones_like(ts)*np.mean(ts),np.ones_like(ts)*np.mean(ts))
    
def f_pixel_mean(ts, h=0.5):
    peaks, bottoms = f_pixel_peaks(ts)
    return h*peaks+(1-h)*bottoms

def f_pixel_updown(ts, thre_up=0.75, thre_down=0.25):
    
    peaks, bottoms = f_pixel_peaks(ts)
    threp_up_line = thre_up*peaks+(1-thre_up)*bottoms
    threp_down_line = thre_down*peaks+(1-thre_down)*bottoms
    arr_updown = np.zeros_like(ts, dtype=np.int8)
    for i, v in enumerate(ts):
        if i == 0 : continue
        flg_up = 1 if v > threp_up_line[i] else 0
        flg_down = 1 if v < threp_down_line[i] else 0
        flg_up *= ( 1 - arr_updown[i-1] )
        flg_down *= ( arr_updown[i-1] )
        arr_updown[i] = (1-flg_down)*(flg_up+arr_updown[i-1])
            
    return arr_updown

def f_pixel_apd(ts, thre_up=0.6, thre_down=0.4):
    
    peaks, bottoms = f_pixel_peaks(ts)
    thre_up_line = thre_up*peaks+(1-thre_up)*bottoms
    thre_down_line = thre_down*peaks+(1-thre_down)*bottoms
    
    #vmax = ts.max(); vmin=ts.min()
    #thre_up_v= (thre_up)*vmax + (1-thre_up)*vmin
    #thre_down_v = (thre_down)*vmax + (1-thre_down)*vmin
    
    updown = 0; cnt = 0
    arr_apd = np.zeros_like(ts, dtype=np.int8)    
    for i, v in enumerate(ts):
        if i == 0 : continue
        flg_up = 1 if v > thre_up_line[i] else 0
        flg_down = 1 if v < thre_down_line[i] else 0
        flg_up *= ( 1 - updown )
        flg_down *= ( updown )
        updown = (1-flg_down)*(flg_up+updown)
        cnt = (1-flg_up)*(cnt+updown)
        arr_apd[i] = flg_down*cnt + (1-flg_down)*arr_apd[i-1]
    return arr_apd

def f_pixel_phase(ts, sigma_t):
    return np.angle(hilbert(gaussian_filter1d(ts, sigma=sigma_t)))
