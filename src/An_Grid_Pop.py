#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 20 11:57:01 2023

@author: sara.nazari
"""

## ------------------------------------------------------------------------------------ ##
# Calculate annual Grid Populaton Based on the 5 years population data of GPW Version 4  #
## ------------------------------------------------------------------------------------ ##


import xarray as xr
import pandas as pd 
import numpy as np

def An_Grid_Pop (fn_Grid_Pop_5year, fn_an_Grid_Pop):

    first_year = 2001
    last_year = 2020
    df_time = pd.DataFrame({'Date':pd.date_range(str(first_year), str(last_year+1), freq='A')})
    Year = df_time.Date.dt.strftime('%Y')
    
    ds_Pop_5Years = xr.open_dataset(fn_Grid_Pop_5year)
    
    latitude = ds_Pop_5Years.latitude
    longitude = ds_Pop_5Years.longitude
    
    Num_Time = df_time.shape[0]
    Nam_latitude = latitude.shape[0]
    Nam_longitude = longitude.shape[0]
    
    Annual_Pop = np.empty(shape = (Num_Time,Nam_latitude, Nam_longitude))
    
        
    for i in range(0, 5):
        P2000 = ds_Pop_5Years.isel(raster = 0)
        P2005 = ds_Pop_5Years.isel(raster = 1)
        P2000_2005 = P2005-P2000
        P_nextYear = ((P2000_2005)/5)*(i+1)+P2000
        P_nextYear = P_nextYear.to_array(dim='UN WPP-Adjusted Population Count, v4.11 (2000, 2005, 2010, 2015, 2020): 2.5 arc-minutes')
        Annual_Pop[i,:,:] = P_nextYear
        
    for i in range(5, 10):
        P2005 = ds_Pop_5Years.isel(raster = 1)
        P2010 = ds_Pop_5Years.isel(raster = 2)
        P2010_2005 = P2010-P2005
        P_nextYear = ((P2010_2005)/5)*(i-5+1)+P2005
        P_nextYear = P_nextYear.to_array(dim='UN WPP-Adjusted Population Count, v4.11 (2000, 2005, 2010, 2015, 2020): 2.5 arc-minutes')
        Annual_Pop[i,:,:] = P_nextYear
    
    for i in range(10, 15):
        P2010 = ds_Pop_5Years.isel(raster = 2)
        P2015 = ds_Pop_5Years.isel(raster = 3)
        P2015_2010 = P2015-P2010
        P_nextYear = ((P2015_2010)/5)*(i-10+1)+P2010
        P_nextYear = P_nextYear.to_array(dim='UN WPP-Adjusted Population Count, v4.11 (2000, 2005, 2010, 2015, 2020): 2.5 arc-minutes')
        Annual_Pop[i,:,:] = P_nextYear
    
    for i in range(15, 20):
        P2015 = ds_Pop_5Years.isel(raster = 3)
        P2020 = ds_Pop_5Years.isel(raster = 4)
        P2020_2015 = P2020-P2015
        P_nextYear = ((P2020_2015)/5)*(i-15+1)+P2015
        P_nextYear = P_nextYear.to_array(dim='UN WPP-Adjusted Population Count, v4.11 (2000, 2005, 2010, 2015, 2020): 2.5 arc-minutes')
        Annual_Pop[i,:,:] = P_nextYear
        
        
    ar_Annual_Pop = xr.DataArray(Annual_Pop, dims = ['time','latitude','longitude'],coords =[df_time.Date[:], latitude, longitude], 
                                    attrs=dict(description="Calculation of Linear Population changes between 5 years of data based on GPW Version 4", units='Persons')) 
    ds_Annual_Pop = ar_Annual_Pop.to_dataset(name='Annual_Pop')
            
    ds_Annual_Pop.to_netcdf(fn_an_Grid_Pop)

An_Grid_Pop (snakemake.input[0], snakemake.output[0])