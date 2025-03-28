#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 14 12:53:02 2024

@author: sara.nazari
"""
## ------------------------------------------------------------------------------------------ ##
#   Calculate annual countries Per urban and mining grid where GW depth is less than 100m     #
#                       industrial groundwater withdrawal (m3/Year)                           #
## ------------------------------------------------------------------------------------------ ##


import geopandas as gpd
import numpy as np

def Countries_Grid_Ind_GWW(fn_Countries_Urban_Mining_GWDepth_100m_Count,start_year, end_year,fn_Countries_Grid_Ind_GWW):

    df = gpd.read_file(fn_Countries_Urban_Mining_GWDepth_100m_Count)    
    for i in range (0,end_year-start_year+1):
        df['InGW_G'+str(i+start_year)]  = np.where (df['Ur_Min_GW'] == 0, 0, df['IndGW_'+str(i+start_year)]/df['Ur_Min_GW']*10**9)

    df.to_file(driver = 'ESRI Shapefile', filename = fn_Countries_Grid_Ind_GWW) 
    
Countries_Grid_Ind_GWW(snakemake.input[0], snakemake.params[0], snakemake.params[1], snakemake.output[0])