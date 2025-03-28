#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 10 10:07:16 2024

@author: sara.nazari
"""

## ----------------------------------------------------------------------------##
#      Find the grids where groundwater depth is less than 100m and            #
#   and assign the number of people based on the population to the grid        #
## --------------------------------------------------------------------------- ##

import xarray as xr
import numpy as np
import pandas as pd

def Pop_GWdepth_100m (fn_an_Grid_Pop_01degree,fn_GWDepth_01Degree,fn_an_Grid_Pop_GWDepth_100m,fn_GW_depth_100m ):

    ds_Annual_Pop = xr.open_dataset(fn_an_Grid_Pop_01degree)
    ds_GW_depth = xr.open_dataset(fn_GWDepth_01Degree)
    
    first_year = 2001
    last_year = 2020
    df_time = pd.DataFrame({'Date':pd.date_range(str(first_year), str(last_year+1), freq='A')})
    Year = df_time.Date.dt.strftime('%Y')
    
    latitude = ds_Annual_Pop.y
    longitude = ds_Annual_Pop.x
    Num_Time = df_time.shape[0]
    Num_Lat = latitude.shape[0]
    Num_Lon = longitude.shape[0] 
    
    Ar_Pop_GW_depth = np.empty(shape=(Num_Time,Num_Lat,Num_Lon))
    
    GW_depth_less_100m_value = xr.where(ds_GW_depth.band_data<=100,ds_GW_depth.band_data,np.nan)
    GW_depth_less_100m = xr.where(ds_GW_depth.band_data<=100,1,np.nan)
    
    for year in range (first_year, last_year+1):
        i = year-first_year
        Ar_Pop_GW_depth[i,:,:] = xr.where(GW_depth_less_100m[0,:,:]==1, ds_Annual_Pop.Annual_Pop[i,:,:], np.nan)
    
    Pop_GW_depth = xr.DataArray(Ar_Pop_GW_depth, dims = ['time','latitude','longitude'],coords =[df_time.Date[:], latitude, longitude], 
                                    attrs=dict(description="Calculation of per grid total population where groundwater depth is less than 100m", units='person')) 
    ds_Pop_GW_depth = Pop_GW_depth.to_dataset(name='T_Pop_GWdepth')
    ds_Pop_GW_depth.to_netcdf(fn_an_Grid_Pop_GWDepth_100m)
    GW_depth_less_100m_value = GW_depth_less_100m_value.to_dataset(name='GW_depth_less_100m')
    GW_depth_less_100m_value.to_netcdf(fn_GW_depth_100m)

Pop_GWdepth_100m (snakemake.input[0],snakemake.input[1],snakemake.output[0], snakemake.output[1] )