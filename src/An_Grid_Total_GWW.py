#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 16 12:41:34 2024

@author: sara.nazari
"""

## ---------------------------------------------------------------------------------------------- ##
#              Calculate annual Total Groundwater withdrawal or the three sectors as follow:      #
#                   Net irrigation groundwater withdrawal in irrigated areas                      #
#   Industrial groundwater withdrawal in urban and mining areas where groundwater depth < 100 m   #
#   Domestic groundwater withdrawal based on population where groundwater depth < 100 m           #
## ---------------------------------------------------------------------------------------------- ##

import xarray as xr
import numpy as np
import pandas as pd

def Grid_Total_GWW(fn_An_Grid_Net_Irr_GWW,fn_An_Grid_Total_Ind_GWW,fn_Grid_Total_Dom_GWW_GWdepth,start_year, end_year,fn_An_Grid_Total_GWW):

    ds_Net_Irr_GWW = xr.open_dataset(fn_An_Grid_Net_Irr_GWW)
    ds_Ind_GWW = xr.open_dataset(fn_An_Grid_Total_Ind_GWW)
    ds_Dom_GWW = xr.open_dataset(fn_Grid_Total_Dom_GWW_GWdepth)
    df_time = pd.DataFrame({'Date':pd.date_range(str(start_year), str(end_year+1), freq='A')})
    Year = df_time.Date.dt.strftime('%Y')
    
    latitude = ds_Net_Irr_GWW.latitude
    longitude = ds_Net_Irr_GWW.longitude
    Num_Time = df_time.shape[0]
    Num_Lat = latitude.shape[0]
    Num_Lon = longitude.shape[0] 

    Ar_Net_Irr_GWW = np.empty(shape=(Num_Time,Num_Lat,Num_Lon))
    Ar_Net_Irr_GWW [:,:,:]  = ds_Net_Irr_GWW.T_N_Irr_GWW [:,:,:]
    mask_Ar_Net_Irr_GWW = np.isnan(Ar_Net_Irr_GWW)
    
    Ar_Ind_GWW = np.empty(shape=(Num_Time,Num_Lat,Num_Lon))
    Ar_Ind_GWW [:,:,:]  =  ds_Ind_GWW.T_Ind_GWW_Urban_Mining_Grid [:,:,:]
    mask_Ar_Ind_GWW = np.isnan(Ar_Ind_GWW)
    
    Ar_Dom_GWW = np.empty(shape=(Num_Time,Num_Lat,Num_Lon))
    Ar_Dom_GWW [:,:,:]  =  ds_Dom_GWW.T_D_GWW_GWdepth [:,:,:]
    mask_Ar_Dom_GWW = np.isnan(Ar_Dom_GWW)
    
    Ar_Total_GWW = np.where(mask_Ar_Net_Irr_GWW & mask_Ar_Ind_GWW, Ar_Dom_GWW,
                np.where(mask_Ar_Net_Irr_GWW & mask_Ar_Dom_GWW, Ar_Ind_GWW,
                    np.where(mask_Ar_Ind_GWW & mask_Ar_Dom_GWW, Ar_Net_Irr_GWW,
                        np.where(mask_Ar_Net_Irr_GWW, Ar_Ind_GWW + Ar_Dom_GWW,
                            np.where(mask_Ar_Ind_GWW, Ar_Net_Irr_GWW + Ar_Dom_GWW,
                                np.where(mask_Ar_Dom_GWW, Ar_Net_Irr_GWW + Ar_Ind_GWW, Ar_Net_Irr_GWW + Ar_Ind_GWW + Ar_Dom_GWW))))))
    
    
    an_Ar_Total_GWW= xr.DataArray(Ar_Total_GWW, dims = ['time','latitude','longitude'],coords =[df_time.Date[:], latitude, longitude], 
                                    attrs=dict(description=" Total per grid groundwater withdrawal for three sectors (irrigation, industrial, domestic)", units='m3/year')) 
    ds_Total_GWW = an_Ar_Total_GWW.to_dataset(name='T_GWW')
    ds_Total_GWW.to_netcdf(fn_An_Grid_Total_GWW)
    
Grid_Total_GWW(snakemake.input[0],snakemake.input[1], snakemake.input[2], snakemake.params[0], snakemake.params[1],snakemake.output[0])