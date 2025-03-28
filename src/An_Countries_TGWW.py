#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 29 10:36:11 2023

@author: sara.nazari
"""

## ---------------------------------------------------------------------------------------- ##
#  Merg the countries shapefile based and the Aquastat Annual Total Groundwater Withdrawal  #
## ---------------------------------------------------------------------------------------- ##

import pandas as pd
import geopandas as gpd

def Countries_TGWW_data(fn_countries, fn_TGWW, start_year, end_year, fn_TGWW_country):
    shp_df_country = gpd.read_file(fn_countries)
    df_gw_w = pd.read_csv(fn_TGWW)

    for i in range(start_year, end_year + 1):   
        for index, row in df_gw_w.iterrows():
            country_name = row['Country']
            matching_row = shp_df_country[shp_df_country['NAME_EN'] == country_name]
            matching_indices = matching_row.index.tolist()
    
            if not matching_row.empty:
                shp_df_country.loc[matching_indices, 'TGWW_' + str(i)] = row[str(i)]
            
    shp_df_country.to_file(fn_TGWW_country, driver='ESRI Shapefile')


Countries_TGWW_data(snakemake.input[0], snakemake.input[1], snakemake.params[0], snakemake.params[1], snakemake.output[0])
   

