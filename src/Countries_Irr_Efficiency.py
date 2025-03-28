#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 16 10:30:28 2024

@author: sara.nazari
"""
## ------------------------------------------------------------------------------------------------------------ ##
#  Add the country level irrigation efficiency F_Irr, based on the Project efficiency EP of Rohwer et al. 2007  # 
## ------------------------------------------------------------------------------------------------------------ ##

import pandas as pd
import geopandas as gpd

def Irr_Efficiency(fn_assigned_countries_Irr_Grid_Irr_GWW,fn_Countries_F_Irr,fn_assigned_countries_Irr_Grid_Irr_GWW_F_Irr):

    df_Per_Grid_Irr_GWW = gpd.read_file(fn_assigned_countries_Irr_Grid_Irr_GWW)
    
    df_R_Irr = pd.read_csv(fn_Countries_F_Irr)
    
    # Merge the shapefile DataFrame with the CSV DataFrame on the 'NAME_EN' column
    merged_df = pd.merge(df_Per_Grid_Irr_GWW, df_R_Irr, on='NAME_EN', how='left')
    
    # Fill missing values in the 'FP' column with 0.7
    merged_df['FP'].fillna(0.70, inplace=True)
    
    merged_df.rename(columns={'FP': 'F_Irr'}, inplace=True)
    
    merged_df.to_file(fn_assigned_countries_Irr_Grid_Irr_GWW_F_Irr)
    
Irr_Efficiency(snakemake.input[0],snakemake.input[1],snakemake.output[0])