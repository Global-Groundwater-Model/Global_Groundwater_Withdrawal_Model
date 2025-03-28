#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 15 11:45:11 2024

@author: sara.nazari
"""

## ---------------------------------------------------------------------------------- ##
#    Calculate annual countries Per Grid Total Industrial groundwater withdrawal      #
#               constant value for the whole country                                  #
#    considering the urban and mining grids and GW depth less than 100m (m3/Year)     #
#                   and assign to these grids                                         #
## ---------------------------------------------------------------------------------- ##

import geopandas as gpd
import rasterio
from rasterio import features
from rasterio.enums import MergeAlg
import numpy as np
import xarray as xr
import pandas as pd

def Total_Grid_Ind_GWW(fn_assigned_countries_Grid_Ind_GWW,fn_Urban_Mining_GWDepth_100m,start_year, end_year,fn_An_Grid_Total_Ind_GWW):
    
    raster = rasterio.open(fn_Urban_Mining_GWDepth_100m)
    vector = gpd.read_file(fn_assigned_countries_Grid_Ind_GWW, crs="epsg:4326")
    ds_Grid_Urban = xr.open_dataset(fn_Urban_Mining_GWDepth_100m)
    ds_Grid_Urban = ds_Grid_Urban.astype(float)
    ds_Grid_Urban.rio.write_crs("epsg:4326", inplace=True)
    df_time = pd.DataFrame({'Date':pd.date_range(str(start_year), str(end_year+1), freq='A')})
    
    latitude = ds_Grid_Urban.latitude
    longitude = ds_Grid_Urban.longitude
    Num_Time = df_time.shape[0]
    Num_Lat = latitude.shape[0]
    Num_Lon = longitude.shape[0] 
    
    An_Grid_Ind_GWW = np.empty(shape=(Num_Time,Num_Lat,Num_Lon))
    
    i = 0
    for year in range(start_year, end_year+1):
        
        geom_value = ((geom,value) for geom, value in zip(vector.geometry, vector['InGW_G'+str(year)]))
        geom = [shapes for shapes in vector.geometry]
        rasterized = features.rasterize(geom_value,
                                        out_shape = raster.shape,
                                        transform = raster.transform,
                                        all_touched = True,
                                        fill = np.nan,   # background value
                                        merge_alg = MergeAlg.replace,
                                        )
    
        An_Grid_Ind_GWW[i,:,:] = rasterized
        i = i+1
    
    An_Urban_Grid_Total_Ind_GWW = np.empty(shape=(Num_Time,Num_Lat,Num_Lon))
    ds_urban =  np.empty(shape=(Num_Lat,Num_Lon))
    ds_urban [:,:]  = ds_Grid_Urban.Urban_Mining_GWdepth[:,:]
    
    for i in range (0,end_year-start_year+1):
        An_Urban_Grid_Total_Ind_GWW[i,:,:] = An_Grid_Ind_GWW [i,:,:]* ds_urban [:,:]
    
        
    ar_An_Urban_Grid_Ind_GWW = xr.DataArray(An_Urban_Grid_Total_Ind_GWW, dims = ['time','latitude','longitude'],coords =[df_time.Date[:], latitude, longitude], 
                                    attrs=dict(description="Calculation of per urban and mining grid where groundwater depth is less than 100m Industrial groundwater withdrawal for the country", units='m3/year')) 
    ds_Urban_Grid_Ind_GWW = ar_An_Urban_Grid_Ind_GWW.to_dataset(name='T_Ind_GWW_Urban_Mining_Grid')
    
    ds_Urban_Grid_Ind_GWW.to_netcdf(fn_An_Grid_Total_Ind_GWW)

Total_Grid_Ind_GWW(snakemake.input[0],snakemake.input[1], snakemake.params[0], snakemake.params[1], snakemake.output[0])
