#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  1 10:12:32 2023

@author: sara.nazari
"""

## ------------------------------------------------------------------------------------------------------- ##
#           Merg the Eurostat Annual Domestic Groundwater Withdrawal and countires boundries                #
## ------------------------------------------------------------------------------------------------------- ##


import pandas as pd
import geopandas as gpd

def Merge_Dom_GWW_Eu_World(fn_Dom_GWW_EU, fn_Dom_GWW_country, start_year, end_year, fn_Dom_GWW_Eu_World):
    df_dgw_eu = pd.read_csv(fn_Dom_GWW_EU)
    df_dgw_aqua_igrac = gpd.read_file(fn_Dom_GWW_country)

    df_merg = pd.merge(df_dgw_eu, df_dgw_aqua_igrac, left_on='Country', right_on='NAME_EN', suffixes=('Eu', 'wor'))

    rename_dict = {f'DomGW_{year}Eu': f'DomGW_{year}' for year in range(start_year, end_year + 1)}
    df_merg = df_merg.rename(columns=rename_dict)

    col_list = [f'DomGW_{year}' for year in range(start_year, end_year + 1)]

    for col in col_list:
        df_merg[col] = df_merg[col].fillna(df_merg[col + 'wor'])

    drop_cols = ['Country'] + [f'DomGW_{year}wor' for year in range(start_year, end_year + 1)]
    df_merg = df_merg.drop(drop_cols, axis=1)

    df_dgw_world = df_merg.append(df_dgw_aqua_igrac).drop_duplicates(subset=['NAME_EN'], keep='first')

    df_dgw_world = df_dgw_world[['OBJECTID', 'NAME_EN'] + 
                                [f'TGWW_{year}' for year in range(start_year, end_year + 1)] +
                                ['Dom_Frac'] + 
                                col_list + 
                                ['geometry']]

    gdf_dgw_world = gpd.GeoDataFrame(df_dgw_world, crs="EPSG:4326", geometry='geometry')
    gdf_dgw_world.to_file(fn_Dom_GWW_Eu_World, driver='ESRI Shapefile')

    print(f"Shapefile saved at: {fn_Dom_GWW_Eu_World}")


Merge_Dom_GWW_Eu_World(snakemake.input[0], snakemake.input[1], snakemake.params[0], snakemake.params[1], snakemake.output[0])