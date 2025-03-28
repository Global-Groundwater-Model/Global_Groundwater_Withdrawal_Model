#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  8 15:10:14 2024

@author: sara.nazari
"""

import xarray as xr
import pandas as pd
import numpy as np

def Total_Dom_GWW (fn_Grid_Person_Dom_GWW_GWdepth, fn_Grid_Pop_GWDepth, start_year, end_year,fn_Grid_Total_Dom_GWW_GWdepth):
    
    df_time = pd.DataFrame({'Date':pd.date_range(str(start_year), str(end_year+1), freq='A')})
    Year = df_time.Date.dt.strftime('%Y')
    
    ds_Annual_D_GWW_Per_P_GWdepth = xr.open_dataset(fn_Grid_Person_Dom_GWW_GWdepth)
    ds_Annual_Pop_GWdepth = xr.open_dataset(fn_Grid_Pop_GWDepth)
    latitude_GWdepth = ds_Annual_Pop_GWdepth.latitude
    longitude_GWdepth = ds_Annual_Pop_GWdepth.longitude
    Num_Time = df_time.shape[0]
    Num_Lat_GWdepth = latitude_GWdepth.shape[0]
    Num_Lon_GWdepth = longitude_GWdepth.shape[0] 

    Annual_Grid_D_GWW_GWdepth= np.empty(shape=(Num_Time,Num_Lat_GWdepth,Num_Lon_GWdepth))
    
    
    for year in range (start_year, end_year+1):
        i = year-start_year
        Annual_Grid_D_GWW_GWdepth [i,:,:] = ds_Annual_Pop_GWdepth.T_Pop_GWdepth [i+start_year-2001,:,:]*ds_Annual_D_GWW_Per_P_GWdepth.T_D_GWW_Per_P_GWdepth[i,:,:]
    

    ar_Annual_Grid_D_GWW_GWdepth = xr.DataArray(Annual_Grid_D_GWW_GWdepth, dims = ['time','latitude','longitude'],coords =[df_time.Date[:], latitude_GWdepth, longitude_GWdepth], 
                                                attrs=dict(description="Calculation of per grid total domestic groundwater withdrawal with groundwater depth less than 100m (total population of the grid*domestic groundwater withdrawal per person)", units='m3/year')) 
    ds_Annual_Grid_D_GWW_GWdepth = ar_Annual_Grid_D_GWW_GWdepth.to_dataset(name='T_D_GWW_GWdepth')
    ds_Annual_Grid_D_GWW_GWdepth.to_netcdf(fn_Grid_Total_Dom_GWW_GWdepth)
    
Total_Dom_GWW (snakemake.input[0],snakemake.input[1], snakemake.params[0], snakemake.params[1], snakemake.output[0])