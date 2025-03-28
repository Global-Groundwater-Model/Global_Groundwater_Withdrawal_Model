#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 15 13:05:57 2024

@author: sara.nazari
"""

## ------------------------------------------------------------------------------------------------------- ##
#        Merg the Eurostat Annual irrigation Groundwater Withdrawal and countires boundries                #
## ------------------------------------------------------------------------------------------------------- ##


import pandas as pd
import geopandas as gpd
import numpy as np

def Merge_Irr_GWW_Eu_World(fn_Irr_GWW_EU, fn_Irr_GWW_country, start_year, end_year, fn_Irr_GWW_Eu_World):
    
    df_IrrGW_Eu = pd.read_csv(fn_Irr_GWW_EU)
    df_IrrGw_Aqua_igrac = gpd.read_file(fn_Irr_GWW_country)

    df_merg = pd.merge(df_IrrGW_Eu, df_IrrGw_Aqua_igrac, left_on='Country', right_on='NAME_EN', suffixes=('Eu', 'wor'))
    

    rename_dict = {f'IrrGW_{year}Eu': f'IrrGW_{year}' for year in range(start_year, end_year + 1)}
    df_merg = df_merg.rename(columns=rename_dict)
    
    col_list = [f'IrrGW_{year}' for year in range(start_year, end_year + 1)]

    for col in col_list:
        df_merg[col] = df_merg[col].fillna(df_merg[col + 'wor'])

    drop_cols = ['Country'] + [f'IrrGW_{year}wor' for year in range(start_year, end_year + 1)]
    df_merg = df_merg.drop(drop_cols, axis=1)

    df_IrrGW_World = df_merg.append(df_IrrGw_Aqua_igrac).drop_duplicates(subset=['NAME_EN'], keep='first')

    df_IrrGW_World = df_IrrGW_World[['OBJECTID', 'NAME_EN'] + 
                                    [f'TGWW_{year}' for year in range(start_year, end_year + 1)] +
                                    ['Irr_Frac'] + 
                                    col_list + 
                                    ['geometry']]

    # Set irrigation groundwater withdrawal to 0 where 'Irr_Frac' is 0
    df_IrrGW_World.loc[df_IrrGW_World['Irr_Frac'] == 0, col_list] = 0   

    gdf_IrrGW_World = gpd.GeoDataFrame(df_IrrGW_World, crs="EPSG:4326", geometry='geometry')
    gdf_IrrGW_World.to_file(fn_Irr_GWW_Eu_World, driver='ESRI Shapefile')

    print(f"Shapefile saved at: {fn_Irr_GWW_Eu_World}")

Merge_Irr_GWW_Eu_World(snakemake.input[0],snakemake.input[1],snakemake.params[0],snakemake.params[1], snakemake.output[0])