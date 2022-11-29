"""
Analysis of G4 experiment in terms of equivalent potential temperature changes
"""

#Import libraries
import numpy as np
import xarray as xr
import scipy
from scipy import stats
import scipy.special as sp
import cftime
import matplotlib.pyplot as plt
from matplotlib import cm
import cartopy
import cartopy.crs as ccrs
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
from cartopy.util import add_cyclic_point
from glob import glob
import os
import warnings

#Set paths
data_dir = '/Users/mdiamond/Data/CMIP5/HadGEM2-ES'
save_dir = '/Users/mdiamond/Projects/GeoTheta/quick_plots'


"""
Load data
"""

fxa = xr.open_mfdataset(glob(data_dir+'/*a_fx*nc')+glob(data_dir+'/*orog_fx*nc')+glob(data_dir+'/*sftlf_fx*nc'))

da = {} #Atmospheric data

vars_atm = ['od550aer', 'reffclwtop', 'clt', 'evspsbl','huss', 'pr', 'ps', 'rlut', 'rsds', 'rsdscs', 'rsdt', 'rsut', 'rsutcs', 'tas']

print('Loading data...')
for exp in ['rcp26','rcp45','G4','G4cdnc']:
    print(exp)
    
    files_atm = []
    
    for vara in vars_atm: files_atm = files_atm + glob(data_dir+'/*%s_*%s_*r1i1p1_20*nc' % (vara,exp))
        
    da[exp] = xr.open_mfdataset(files_atm)
    
    #Calculate theta_e following Song et al. (2022), PNAS
    Lv = 2500000 #J kg-1
    Cp = 1005.7 #J K-1 kg-1
    Rd = 287.04 #J K-1 kg-1
    T = da[exp]['tas'] #K
    r = da[exp]['huss']/(1-da[exp]['huss'])
    ps = da[exp]['ps']/100 #hPa
    
    da[exp]['the'] = (T+Lv/Cp*r)*(1000/ps)**(Rd/Cp)
    da[exp]['the'].attrs = {'units' : 'K', 'long_name' : 'theta_e'}
    
    da[exp]['theT'] = (T)*(1000/ps)**(Rd/Cp)
    da[exp]['theT'].attrs = {'units' : 'K', 'long_name' : 'Temperature component of theta_e'}
    
    da[exp]['theM'] = (Lv/Cp*r)*(1000/ps)**(Rd/Cp)
    da[exp]['theM'].attrs = {'units' : 'K', 'long_name' : 'Moisture component of theta_e'}

print('...Done!')





















