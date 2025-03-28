#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 15 16:44:14 2024

@author: sara.nazari
"""

## ----------------------------------------------------------------------------------------------- ##
#    Calculate annual countries Per irrigated areas irrigatiion groundwater withdrawal (m3/Year)   #
## ----------------------------------------------------------------------------------------------- ##

import geopandas as gpd
import numpy as np

def Grid_Irr_GWW(fn_Countries_Irr_Area_Sum,start_year, end_year,fn_countries_Grid_Irr_GWW):
    
    df_Irr_GWW = gpd.read_file(fn_Countries_Irr_Area_Sum)
    for i in range (0,end_year-start_year+1):
    
        df_Irr_GWW['IrrGWG'+str(i+start_year)]  = np.where (df_Irr_GWW['Sum_IrrGWR'] == 0, 0, df_Irr_GWW['IrrGW_'+str(i+start_year)]/df_Irr_GWW['Sum_IrrGWR']*10**9)
    df_Irr_GWW.to_file(driver = 'ESRI Shapefile', filename = fn_countries_Grid_Irr_GWW) 
    
Grid_Irr_GWW(snakemake.input[0],snakemake.params[0],snakemake.params[1], snakemake.output[0])
