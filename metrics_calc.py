#!/usr/bin/env python

"""metrics calculation module
This module contains the functions for calculating RSL, SINR, path loss,
fading and shadowing"""

import math
import numpy as np

def path_loss(f, h_b, d):
    "compute path loss using COST231 model for a small city"
    pl= 46.3 + (33.9 * math.log10(f)) - (13.82 * math.log10(h_b)) + ((44.9 - (6.55 * math.log10(h_b))) * math.log10(d))
    return pl

def shadowing():
    "create cell 10by10m squares and compute shadowing value for each"
    #creating 2D list of 2000 by 2000 elements (i.e squares/boxes)
    cell_box_list= [0] * 2000
    for i in range(0,2000):
        #computing the shadowing values
        shadow_val= np.random.normal(0.0,2.0,2000)
        cell_box_list[i]= shadow_val.tolist()

    return cell_box_list

def fading():
    "compute fading value"
    x = np.random.rayleigh(1.0,None)
    f = 20 * math.log10(x)
    return f
    
def rsl_dbm(eirp, freq, h_b, d, s):
    "compute received signal level in dBm"
    pl = path_loss(freq, h_b, d)
    fa = fading()
    rsl = eirp - pl + s + fa
    return rsl

def sinr(rsl, pg, N):
    "compute Signal to Interference + Noise ratio"
    #in dBm
    sig_lvl= rsl + pg
    inter_lvl= 0
    inter_lvl_linear= 0
    if N==1: #first call attempt to bstn
        pass
    else:
        inter_lvl= rsl + (10 * math.log10(N - 1))
        inter_lvl_linear= math.pow(10,(inter_lvl / 10))
    noise_lvl= -110 #dBm
    #in linear (mW)
    noise_lvl_linear= math.pow(10,(noise_lvl / 10))
    noise_plus_int= noise_lvl_linear + inter_lvl_linear
    #noise plus interference to dBm
    noise_plus_int= 10 * math.log10(noise_plus_int)
    sinr = sig_lvl - noise_plus_int
    return sinr
    
