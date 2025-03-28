#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 15 15:39:21 2024

@author: sara.nazari
"""

## -------------------------------------------------------------------------- ##
#   Calculate sum of the irrigated area with groundwater within a country     #
## -------------------------------------------------------------------------- ##

import rasterio as rio 
import geopandas as gpd
import rasterstats as rstats 
import pandas as pd
import numpy as np
import xarray as xr


def Sum_GW_Irr_Area_Country(fn_Irr_GWW_country_Fillno_IrrFrac, fn_GW_Irr_Area, fn_Countries_Irr_Area_Sum):
       
    ds = xr.open_dataset(fn_GW_Irr_Area)
    Shp_df = gpd.read_file(fn_Irr_GWW_country_Fillno_IrrFrac)
        
    Latitude = ds.y
    Longitude = ds.x

    Num_Lat = Latitude.shape[0]
    Num_Lon= Longitude.shape[0] 
     
    Ar = np.empty(shape=(Num_Lat,Num_Lon))
    affine = rio.open(fn_GW_Irr_Area).transform 
     

    Ar[:,:] = ds.band_data[:,:]
    Sum = rstats.zonal_stats(Shp_df.geometry, Ar, nodata=np.nan, affine=affine, stats="sum", all_touched=True)
    Shp_df['Sum_IrrGWR'] = pd.DataFrame(Sum)
    Shp_df.to_file(driver = 'ESRI Shapefile', filename =fn_Countries_Irr_Area_Sum) 
    
Sum_GW_Irr_Area_Country(snakemake.input[0],snakemake.input[1],snakemake.output[0])