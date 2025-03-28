#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 12 20:47:33 2024

@author: sara.nazari
"""

## --------------------------------------------------------------------------------------------------------- ##
#  Merg the Aquastat Annual Total Groundwater Withdrawal and igrac fraction of Industrial groundwater usage  #
#                 to calculate the annual countries Industrial groundwater abstraction (10*9 m3/year)        #
## --------------------------------------------------------------------------------------------------------- ##


import pandas as pd
import geopandas as gpd

def Countries_Ind_GWW(fn_TGWW_country, fn_GWW_Frac, start_year, end_year, fn_Ind_GWW_country): 
    shp_TGWW_country = gpd.read_file(fn_TGWW_country)
    shp_GW_fraction = gpd.read_file(fn_GWW_Frac)
          
    
    df_industrial_GWW = pd.merge(shp_TGWW_country,shp_GW_fraction[['industrial','region']],left_on=('NAME_EN'), right_on = ('region'))
    df_industrial_GWW['industrial'] = df_industrial_GWW ['industrial']/100
    df_industrial_GWW['Ind_Frac'] = df_industrial_GWW ['industrial']
    
    df_industrial_GWW ['Ind_Frac'] = df_industrial_GWW['Ind_Frac'].mask(df_industrial_GWW['Ind_Frac']<0)
    
        
    df_industrial_GWW = df_industrial_GWW.drop(columns=['region','industrial'])
    
    for i in range (start_year,end_year+1):
    
        df_industrial_GWW['TGWW_'+str(i)]=df_industrial_GWW['TGWW_'+str(i)].astype(float)
        df_industrial_GWW['IndGW_'+str(i)]= df_industrial_GWW.Ind_Frac*df_industrial_GWW['TGWW_'+str(i)]
    
    df_industrial_GWW.to_file(fn_Ind_GWW_country,driver = 'ESRI Shapefile') 
    
Countries_Ind_GWW(snakemake.input[0], snakemake.input[1], snakemake.params[0], snakemake.params[1], snakemake.output[0])