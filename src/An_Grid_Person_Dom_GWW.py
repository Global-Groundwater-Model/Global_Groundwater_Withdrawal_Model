#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May  3 15:39:07 2024

@author: sara.nazari
"""
## ---------------------------------------------------------------------------------------------------- ##
#  Calculate annual countries Per Grid and person domestic groundwater withdrawal (m3/Year)             #
#  when only the popultion who are living in areas with groundwater depth less than 100m are considred  #
## ---------------------------------------------------------------------------------------------------- ##

import geopandas as gpd
import rasterio
from rasterio import features
from rasterio.enums import MergeAlg
import numpy as np
import xarray as xr
import pandas as pd

def Grid_Person_Dom_GWW(fn_assigned_countries_Person_Dom_GWW_GWDepth, fn_Grid_Pop_GWDepth, start_year, end_year, fn_Grid_Person_Dom_GWW_GWdepth):
    
    raster_gwdepth = rasterio.open(fn_Grid_Pop_GWDepth)
    vector_gwdepth = gpd.read_file(fn_assigned_countries_Person_Dom_GWW_GWDepth)
    ds_grid_pop_gwdepth = xr.open_dataset(fn_Grid_Pop_GWDepth)

    df_time = pd.DataFrame({'Date': pd.date_range(str(start_year), str(end_year + 1), freq='A')})
    latitude_gwdepth = ds_grid_pop_gwdepth.latitude
    longitude_gwdepth = ds_grid_pop_gwdepth.longitude
    num_time_gwdepth = df_time.shape[0]
    num_lat_gwdepth = latitude_gwdepth.shape[0]
    num_lon_gwdepth = longitude_gwdepth.shape[0]

    an_grid_d_gww_per_p_gwdepth = np.empty(shape=(num_time_gwdepth, num_lat_gwdepth, num_lon_gwdepth))

    for i, year in enumerate(range(start_year, end_year + 1)):
        geom_value_gwdepth = ((geom, value) for geom, value in zip(vector_gwdepth.geometry, vector_gwdepth[f'DomGWP{year}']))

        rasterized_gwdepth = features.rasterize(geom_value_gwdepth,
                                                out_shape=raster_gwdepth.shape,
                                                transform=raster_gwdepth.transform,
                                                all_touched=True,
                                                fill=np.nan,
                                                merge_alg=MergeAlg.replace,
                                                )
        an_grid_d_gww_per_p_gwdepth[i, :, :] = rasterized_gwdepth

        print(year)
    ar_annual_d_gww_per_p_gwdepth = xr.DataArray(an_grid_d_gww_per_p_gwdepth,
                                                  dims=['time', 'latitude', 'longitude'],
                                                  coords=[df_time.Date[:], latitude_gwdepth, longitude_gwdepth],
                                                  attrs=dict(
                                                      description="Calculation of per grid per person domestic groundwater withdrawal where groundwater depth is less than 100m",
                                                      units='m3/year'))
    ds_annual_d_gww_per_p_gwdepth = ar_annual_d_gww_per_p_gwdepth.to_dataset(name='T_D_GWW_Per_P_GWdepth')
    ds_annual_d_gww_per_p_gwdepth.to_netcdf(fn_Grid_Person_Dom_GWW_GWdepth)


Grid_Person_Dom_GWW(snakemake.input[0],snakemake.input[1], snakemake.params[0], snakemake.params[1], snakemake.output[0])