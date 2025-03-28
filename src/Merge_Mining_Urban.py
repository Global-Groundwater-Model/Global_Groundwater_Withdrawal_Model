#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 13 10:15:38 2024

@author: sara.nazari
"""

## ------------------------------------------------------------------------------------------------- ##
#                    Merging mining locations and the urban centre grids                             #
## ------------------------------------------------------------------------------------------------- ##


import xarray as xr
import numpy as np

def Merge_Mining_Urban (fn_Urban,fn_Mining,fn_Urban_Mining):

    ds_urban = xr.open_dataset(fn_Urban)
    ds_mining = xr.open_dataset(fn_Mining)
    
    
    Urban_loc = xr.where(ds_urban.band_data == 1, 1 ,0)
    ds_Urban_loc = Urban_loc.to_dataset(name='Urban_loc')
    
    latitude = ds_mining.y
    longitude = ds_mining.x
    Num_Lat = latitude.shape[0]
    Num_Lon = longitude.shape[0] 
    
    An_Urban_loc = np.empty(shape=(Num_Lat,Num_Lon))
    An_Urban_loc [:,:] = ds_Urban_loc.Urban_loc[0,:,:]
    
    
    mining_loc= xr.where(ds_mining.band_data > 0, 1, 0)
    mining_loc_2 = mining_loc[:,:,:]
    ds_mining_loc = mining_loc_2.to_dataset(name='mining_loc')
    
    An_mining_loc = np.empty(shape=(Num_Lat,Num_Lon))
    An_mining_loc [:,:] = ds_mining_loc.mining_loc[0,:,:]
    
    An_merge_urbans_mining = An_Urban_loc [:,:] + An_mining_loc [:,:]
        
    ar_merge_urbans_mining = xr.DataArray(An_merge_urbans_mining, dims = ['latitude','longitude'],coords =[latitude, longitude], 
                                    attrs=dict(description='Urban and mining locations')) 
    ds_merge_urbans_mining = ar_merge_urbans_mining.to_dataset(name='Urban_Mining')
    ds_merge_urbans_mining = ds_merge_urbans_mining.Urban_Mining > 0
    ds_merge_urbans_mining.to_netcdf(fn_Urban_Mining)

Merge_Mining_Urban (snakemake.input[0],snakemake.input[1],snakemake.output[0])