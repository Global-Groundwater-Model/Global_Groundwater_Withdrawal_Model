#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 16 11:43:26 2024

@author: sara.nazari
"""

## ----------------------------------------------------------------------------------------- ##
#         Calculate annual countries Per Grid Net Irrigation groundwater withdrawal          #
#        Net_Irr_GWW = Total_Irr_GW -Frgw*(Total_Irr_GWW - Consumptive_Irr_GW)               #
## ----------------------------------------------------------------------------------------- ##


import pandas as pd
import xarray as xr
import numpy as np

def Net_Irr_GWW(fn_An_Grid_CU_Irr_GWW,fn_An_Grid_Total_Irr_GWW,fn_Frgw,start_year,end_year,fn_An_Grid_Net_Irr_GWW):
    ds_CU_Irr_GWW = xr.open_dataset(fn_An_Grid_CU_Irr_GWW)
    ds_Irr_GWW = xr.open_dataset(fn_An_Grid_Total_Irr_GWW)
    ds_Frgw = xr.open_dataset(fn_Frgw)
    df_time = pd.DataFrame({'Date':pd.date_range(str(start_year), str(end_year+1), freq='A')})
  
    latitude = ds_CU_Irr_GWW.latitude
    longitude = ds_CU_Irr_GWW.longitude
    Num_Time = df_time.shape[0]
    Num_Lat = latitude.shape[0]
    Num_Lon = longitude.shape[0] 
    Ar_An_Dif = np.empty(shape=(Num_Time,Num_Lat,Num_Lon))
    An_Net_Irr_GWW = np.empty(shape=(Num_Time,Num_Lat,Num_Lon))
    An_Frgw = np.empty(shape=(Num_Lat,Num_Lon))
    
    Ar_An_Dif[:,:,:] = ds_Irr_GWW.T_Irr_GWW_Irr_Areas - ds_CU_Irr_GWW.T_CU_Irr_GWW_Irr_Areas
    ds_Frgw = ds_Frgw.reindex(lat = ds_Frgw['lat'][::-1])
    An_Frgw [:,:] = ds_Frgw.Band1
    
    for i in range(start_year-start_year,end_year-start_year+1 ):
        An_Net_Irr_GWW[i,:,:] = ds_Irr_GWW.T_Irr_GWW_Irr_Areas[i,:,:] - An_Frgw [:,:]*Ar_An_Dif[i,:,:]

    ar_An_Net_Irr_GWW = xr.DataArray(An_Net_Irr_GWW, dims = ['time','latitude','longitude'],coords =[df_time.Date[:], latitude, longitude], 
                                    attrs=dict(description="Calculation of grid net irrigation groundwater withdrawal (Considering Groundwater Irrigation Efficiency and Return flow fraction)", units='m3/year')) 
    ds_An_Net_Irr_GWW  = ar_An_Net_Irr_GWW.to_dataset(name='T_N_Irr_GWW')
    ds_An_Net_Irr_GWW.rio.write_crs("epsg:4326", inplace=True)
    ds_An_Net_Irr_GWW.to_netcdf(fn_An_Grid_Net_Irr_GWW)
    
Net_Irr_GWW(snakemake.input[0], snakemake.input[1], snakemake.input[2], snakemake.params[0], snakemake.params[1], snakemake.output[0])
