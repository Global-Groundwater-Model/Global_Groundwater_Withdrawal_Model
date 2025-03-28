#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 10 09:50:18 2024

@author: sara.nazari
"""
## ------------------------------------------------------------------------ ##
#                    Calculate annual countries population                  #
#                where groundwater level is less than 100m                  #
## ------------------------------------------------------------------------ ##

import rasterio as rio 
import geopandas as gpd
import rasterstats as rstats 
import pandas as pd
import numpy as np
import xarray as xr

def Countries_Pop (fn_countries, fn_an_Grid_Pop_GWDepth_100m,fn_Countries_Pop_GWdepth_100m):
    
    Shp_df_GWdepth = gpd.read_file(fn_countries)
    ds_Grid_Pop_GWdepth = xr.open_dataset(fn_an_Grid_Pop_GWDepth_100m)
    
    Time_Steps = ds_Grid_Pop_GWdepth.time
    Latitude_GWdepth = ds_Grid_Pop_GWdepth.latitude
    Longitude_GWdepth = ds_Grid_Pop_GWdepth.longitude
    
    Num_Time_Steps = Time_Steps.shape[0]
    Num_Lat_GWdepth = Latitude_GWdepth.shape[0]
    Num_Lon_GWdepth= Longitude_GWdepth.shape[0] 
    
    An_Grid_Pop_GWdepth = np.empty(shape=(Num_Lat_GWdepth,Num_Lon_GWdepth))
    affine_GWdepth = rio.open(fn_an_Grid_Pop_GWDepth_100m).transform 
    
    i=0
    while i<Num_Time_Steps:
            
        An_Grid_Pop_GWdepth[:,:] = ds_Grid_Pop_GWdepth.T_Pop_GWdepth[i,:,:]
        Sum_Pop_Country_GWdepth = rstats.zonal_stats(Shp_df_GWdepth.geometry, An_Grid_Pop_GWdepth, nodata=np.nan, affine=affine_GWdepth, stats="sum", all_touched=True)
        Shp_df_GWdepth['Pop_de'+str(i+2001)] = pd.DataFrame(Sum_Pop_Country_GWdepth)
        i +=1

    Shp_df_GWdepth.to_file(driver = 'ESRI Shapefile', filename = fn_Countries_Pop_GWdepth_100m) 
    
Countries_Pop (snakemake.input[0],snakemake.input[1],snakemake.output[0])