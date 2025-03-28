#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 15 12:35:39 2024

@author: sara.nazari
"""

## --------------------------------------------------------------------------------------------------------- ##
#  Merg the Aquastat Annual Total Groundwater Withdrawal and igrac fraction of irrigation groundwater usage  #
#               to calculate the annual countries irrigation groundwater withdrawal                          #
## --------------------------------------------------------------------------------------------------------- ##

import pandas as pd
import geopandas as gpd

def Countries_Irr_GWW(fn_TGWW_country, fn_GWW_Frac, start_year, end_year, fn_Irr_GWW_country):
    
    shp_TGWW_country = gpd.read_file(fn_TGWW_country)
    shp_GW_fraction = gpd.read_file(fn_GWW_Frac)
          
    
    df_irrigation_GWW = pd.merge(shp_TGWW_country,shp_GW_fraction[['agricultur','region']],left_on=('NAME_EN'), right_on = ('region'))
    df_irrigation_GWW['Irr_Frac'] = df_irrigation_GWW['agricultur']/100
    df_irrigation_GWW['Irr_Frac'] = df_irrigation_GWW['Irr_Frac'].mask(df_irrigation_GWW['Irr_Frac']<0)   
    df_irrigation_GWW = df_irrigation_GWW.drop(columns=['region','agricultur'])
    
    for i in range (start_year,end_year+1):
        df_irrigation_GWW[f'TGWW_{i}'] = df_irrigation_GWW[f'TGWW_{i}'].astype(float)
        df_irrigation_GWW['IrrGW_'+str(i)]= df_irrigation_GWW.Irr_Frac*df_irrigation_GWW['TGWW_'+str(i)]
    
    df_irrigation_GWW.to_file(fn_Irr_GWW_country,driver = 'ESRI Shapefile') 
    
Countries_Irr_GWW(snakemake.input[0],snakemake.input[1],snakemake.params[0], snakemake.params[1],snakemake.output[0])