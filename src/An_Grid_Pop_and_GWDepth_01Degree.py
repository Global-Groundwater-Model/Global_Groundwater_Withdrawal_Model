#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  8 17:11:44 2024

@author: sara.nazari
"""

## -----------------------------------------------------------------------------------------##
#                    Use the annaul Population data driven from GPWv4                       #
#                   and calculate the sum of the grids within 0.1 degree                    #
## ---------------------------------------------------------------------------------------- ##

import xarray as xr
import geopandas as gpd
from shapely.geometry import mapping

def Pop_and_GWDepth_To_01Degree (fn_an_Grid_Pop, fn_GW_depth, fn_countries, fn_Refrence, fn_an_Grid_Pop_01degree, fn_GWDepth_01Degree):

    ds_Annual_Pop = xr.open_dataset(fn_an_Grid_Pop)
    ds_GW_depth = xr.open_dataset(fn_GW_depth)
    World_Shape = gpd.read_file(fn_countries, crs="epsg:4326")
    ds_Ref = xr.open_dataset(fn_Refrence)
    
    latitude_Pop = ds_Annual_Pop.latitude
    longitude_Pop = ds_Annual_Pop.longitude
    latitude_GW_depth = ds_GW_depth.y
    longitude_GW_depth = ds_GW_depth.x
    
    
    Num_Lat_Pop = latitude_Pop.shape[0]
    Num_Lon_Pop = longitude_Pop.shape[0] 
    Num_Lat_GW_depth = latitude_GW_depth.shape[0]
    Num_Lon_GW_depth = longitude_GW_depth.shape[0] 
    
    # Calculate the sum in each 0.1 degree grid
    ds_sum_Pop = ds_Annual_Pop.coarsen(longitude=int(Num_Lon_Pop/Num_Lon_GW_depth), latitude=int(Num_Lat_Pop/Num_Lat_GW_depth), boundary='trim').sum()
    ds_sum_Pop.rio.write_crs("epsg:4326", inplace=True)
    ds_Ref.rio.write_crs("epsg:4326", inplace=True)
    ds_sum_Pop_reprojected = ds_sum_Pop.rio.reproject(ds_Ref.rio.crs, resolution=(0.1, 0.1))
    ds_GW_depth = ds_GW_depth.rio.reproject(ds_Ref.rio.crs, resolution=(0.1, 0.1))
    
    clipped = ds_sum_Pop_reprojected.rio.clip(World_Shape.geometry.apply(mapping), World_Shape.crs, drop=False)
    clipped.to_netcdf(fn_an_Grid_Pop_01degree, 
                      mode='w', format = 'NETCDF4',engine='netcdf4') 
    ds_GW_depth.to_netcdf(fn_GWDepth_01Degree, 
                      mode='w', format = 'NETCDF4',engine='netcdf4') 
    
Pop_and_GWDepth_To_01Degree (snakemake.input[0], snakemake.input[1], snakemake.input[2], snakemake.input[3], snakemake.output[0], snakemake.output[1])