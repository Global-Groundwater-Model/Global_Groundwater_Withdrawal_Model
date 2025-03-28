#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 13 12:49:23 2024

@author: sara.nazari
"""

## ------------------------------------------------------------------------ ##
#          Calculate countries number of urban and mining grids             #
## ------------------------------------------------------------------------ ##

import rasterio as rio 
import geopandas as gpd
import rasterstats as rstats 
import pandas as pd
import numpy as np
import xarray as xr


def Count_Urban_Mining_Grids(fn_Ind_GGW_country_Fillno_IndFrac, fn_Urban_Mining_GWDepth_100m, fn_Countries_Urban_Mining_GWDepth_100m_Count):
       
    ds = xr.open_dataset(fn_Urban_Mining_GWDepth_100m)
    Shp_df = gpd.read_file(fn_Ind_GGW_country_Fillno_IndFrac)
        
    Latitude = ds.latitude
    Longitude = ds.longitude

    Num_Lat = Latitude.shape[0]
    Num_Lon= Longitude.shape[0] 
     
    Ar = np.empty(shape=(Num_Lat,Num_Lon))
    affine = rio.open(fn_Urban_Mining_GWDepth_100m).transform 
     

    Ar[:,:] = ds.Urban_Mining_GWdepth[:,:]
    Sum = rstats.zonal_stats(Shp_df.geometry, Ar, nodata=np.nan, affine=affine, stats="count", all_touched=True)
    Shp_df['Ur_Min_GW'] = pd.DataFrame(Sum)
    Shp_df.to_file(driver = 'ESRI Shapefile', filename =fn_Countries_Urban_Mining_GWDepth_100m_Count) 

Count_Urban_Mining_Grids(snakemake.input[0],snakemake.input[1],snakemake.output[0])