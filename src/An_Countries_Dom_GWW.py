#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 29 18:32:03 2023

@author: sara.nazari
"""


## ------------------------------------------------------------------------------------------------------- ##
#  Merg the Aquastat Annual Total Groundwater Withdrawal and igrac fraction of domestic groundwater usage  #
#                 to calculate the annual countries domestic groundwater Withdrawal                        #
## ------------------------------------------------------------------------------------------------------- ##

import pandas as pd
import geopandas as gpd

def Countries_Dom_GWW(fn_TGWW_country, fn_GWW_Frac, start_year, end_year, fn_Dom_GWW_country):
    shp_tgww_country = gpd.read_file(fn_TGWW_country)
    shp_gw_fraction = gpd.read_file(fn_GWW_Frac)

    df_domestic_gww = pd.merge(shp_tgww_country, shp_gw_fraction[['domesticgw', 'region']], left_on='NAME_EN', right_on='region')
    df_domestic_gww['domesticgw'] = df_domestic_gww['domesticgw'] / 100
    df_domestic_gww['Dom_Frac'] = df_domestic_gww['domesticgw']
    df_domestic_gww['Dom_Frac'] = df_domestic_gww['Dom_Frac'].mask(df_domestic_gww['Dom_Frac'] < 0)
    df_domestic_gww = df_domestic_gww.drop(columns=['region', 'domesticgw'])

    for i in range(start_year, end_year + 1):
        df_domestic_gww[f'TGWW_{i}'] = df_domestic_gww[f'TGWW_{i}'].astype(float)
        df_domestic_gww[f'DomGW_{i}'] = df_domestic_gww['Dom_Frac'] * df_domestic_gww[f'TGWW_{i}']

    df_domestic_gww.to_file(fn_Dom_GWW_country, driver='ESRI Shapefile')

Countries_Dom_GWW(snakemake.input[0], snakemake.input[1], snakemake.params[0], snakemake.params[1], snakemake.output[0])