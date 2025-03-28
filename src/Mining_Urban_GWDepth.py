#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 13 10:14:02 2024

@author: sara.nazari
"""

## ---------------------------------------------------------------------------------- ##
#         Find the grids where groundwater depth is less than 100m and                #
#            is an urban center or/and mining location                                #
## ---------------------------------------------------------------------------------- ##

import xarray as xr
import numpy as np
import rasterio as rio 
from rasterio import transform

def Mining_Urban_GWDepth_100m (fn_Urban_Mining,fn_GW_depth,fn_Urban_Mining_GWDepth_100m):

    ds_Grid_Urban_mining = xr.open_dataset(fn_Urban_Mining)
    ds_GW_depth = xr.open_dataset(fn_GW_depth)
    latitude = ds_GW_depth.y
    longitude = ds_GW_depth.x
    Num_Lat = latitude.shape[0]
    Num_Lon = longitude.shape[0] 
    
    An_Gw_depth = np.empty(shape=(Num_Lat,Num_Lon))
    An_Gw_depth[:,:] = ds_GW_depth.band_data<100 
    
    An_Grid_Urban_mining = np.empty(shape=(Num_Lat,Num_Lon))
    An_Grid_Urban_mining[:,:] = ds_Grid_Urban_mining.Urban_Mining == 1 
    
    An_urban_mining_GW_depth = An_Grid_Urban_mining*An_Gw_depth
    ar_urban_mining_GW_depth = xr.DataArray(An_urban_mining_GW_depth, dims = ['latitude','longitude'],coords =[latitude, longitude], 
                                    attrs=dict(description='Urban and mining locations where groundwater depth < 100m')) 
    ds_urban_mining_GW_depth = ar_urban_mining_GW_depth.to_dataset(name='Urban_Mining_GWdepth')
    
    # ds_urban_mining_GW_depth = ds_urban_mining_GW_depth.astype(float)
    ds_urban_mining_GW_depth = xr.where(ds_urban_mining_GW_depth.Urban_Mining_GWdepth > 0,1,np.nan)
    
    # Get the data variable
    #data_var = ds_urban_mining_GW_depth.Urban_Mining_GWdepth

    # # Define the spatial extent and resolution
    left, bottom, right, top = ds_urban_mining_GW_depth.rio.bounds()
    x_res = (right - left) / ds_urban_mining_GW_depth.rio.width
    y_res = (top - bottom) / ds_urban_mining_GW_depth.rio.height

    # # Create the affine transformation matrix
    transform_matrix = transform.from_bounds(left, bottom, right, top, ds_urban_mining_GW_depth.rio.width, ds_urban_mining_GW_depth.rio.height)

    # # Assign the transform to the data variable
    ds_urban_mining_GW_depth = ds_urban_mining_GW_depth.rio.write_crs("epsg:4326", inplace=True)
    ds_urban_mining_GW_depth = ds_urban_mining_GW_depth.rio.write_transform(transform_matrix, inplace=True)

    ds_urban_mining_GW_depth_N = ds_urban_mining_GW_depth.to_dataset(name='Urban_Mining_GWdepth')
                
    ds_urban_mining_GW_depth_N.to_netcdf(fn_Urban_Mining_GWDepth_100m)
    
Mining_Urban_GWDepth_100m (snakemake.input[0],snakemake.input[1],snakemake.output[0])