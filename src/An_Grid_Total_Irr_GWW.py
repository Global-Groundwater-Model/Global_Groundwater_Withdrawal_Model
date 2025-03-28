#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 16 09:46:47 2024

@author: sara.nazari
"""


## ----------------------------------------------------------------------------------------- ##
#         Calculate annual countries Per Grid Total Irrigation groundwater withdrawal        #
#                          constant value for the whole country                              #
#           Consider the groundwater irrigated areas and proportionally assign               #
#           the constant value to the irrigated areas within the country                     #
## ----------------------------------------------------------------------------------------- ##

import geopandas as gpd
import rasterio
from rasterio import features
from rasterio.enums import MergeAlg
import numpy as np
import xarray as xr
import pandas as pd

def Total_Grid_Irr_GWW(fn_assigned_countries_Irr_Grid_Irr_GWW, fn_GW_Irr_Area, start_year, end_year,fn_An_Grid_Total_Irr_GWW):

    raster = rasterio.open(fn_GW_Irr_Area)
    vector = gpd.read_file(fn_assigned_countries_Irr_Grid_Irr_GWW, crs="epsg:4326")
    ds_Grid_Irr_Area = xr.open_dataset(fn_GW_Irr_Area)
    ds_Grid_Irr_Area.rio.write_crs("epsg:4326", inplace=True)
    df_time = pd.DataFrame({'Date':pd.date_range(str(start_year), str(end_year+1), freq='A')})
    
    latitude = ds_Grid_Irr_Area.y
    longitude = ds_Grid_Irr_Area.x
    Num_Time = df_time.shape[0]
    Num_Lat = latitude.shape[0]
    Num_Lon = longitude.shape[0] 
    
    An_Grid_Irr_GWW = np.empty(shape=(Num_Time,Num_Lat,Num_Lon))
    
    i = 0
    for year in range(start_year, end_year+1):
        
        geom_value = ((geom,value) for geom, value in zip(vector.geometry, vector['IrrGWG'+str(year)]))
        geom = [shapes for shapes in vector.geometry]
        rasterized = features.rasterize(geom_value,
                                        out_shape = raster.shape,
                                        transform = raster.transform,
                                        all_touched = True,
                                        fill = np.nan,   # background value
                                        merge_alg = MergeAlg.replace,
                                        )
    
        An_Grid_Irr_GWW[i,:,:] = rasterized
        i = i+1
   
    An_Irr_Area_Grid_Irr_GWW = np.empty(shape=(Num_Time,Num_Lat,Num_Lon))
    ds_Irr_Area =  np.empty(shape=(Num_Lat,Num_Lon))
    ds_Irr_Area [:,:]  = ds_Grid_Irr_Area.band_data[:,:]
    
    for i in range (0,end_year-start_year+1):
        An_Irr_Area_Grid_Irr_GWW[i,:,:] = An_Grid_Irr_GWW [i,:,:]* ds_Irr_Area [:,:]

    ar_An_Irr_Area_Grid_Irr_GWW = xr.DataArray(An_Irr_Area_Grid_Irr_GWW, dims = ['time','latitude','longitude'],coords =[df_time.Date[:], latitude, longitude], 
                                    attrs=dict(description="Calculation of per irrigated area's grid irrigation groundwater withdrawal for the country", units='m3/year')) 
    ds_Irr_Area_Grid_Irr_GWW = ar_An_Irr_Area_Grid_Irr_GWW.to_dataset(name='T_Irr_GWW_Irr_Areas')
    
    ds_Irr_Area_Grid_Irr_GWW.to_netcdf(fn_An_Grid_Total_Irr_GWW)

Total_Grid_Irr_GWW(snakemake.input[0],snakemake.input[1],snakemake.params[0],snakemake.params[1], snakemake.output[0])