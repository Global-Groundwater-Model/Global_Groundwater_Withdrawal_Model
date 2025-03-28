#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov  3 13:14:03 2023

@author: sara.nazari
"""
## ------------------------------------------------------------------------------------------- ##
#     Calculate annual countries Per Person domestic groundwater withdrawal                    #
#            where groundwater level is less than 100m (m3/Year*Person)                        #
## ------------------------------------------------------------------------------------------- ##

import geopandas as gpd
import pandas as pd

def Person_Dom_GWW (fn_Dom_GWW_country_Fillno_DomFrac, fn_Countries_Pop_GWdepth_100m, start_year, end_year, fn_countries_Person_Dom_GWW_GWDepth):
    df_dom_gww = gpd.read_file(fn_Dom_GWW_country_Fillno_DomFrac)
    df_pop_gwdepth = gpd.read_file(fn_Countries_Pop_GWdepth_100m)

    merg_dom_gww_pop_gwdepth = pd.merge(df_dom_gww, df_pop_gwdepth, left_on='geometry', right_on='geometry')

    for i in range(start_year, end_year + 1):
        merg_dom_gww_pop_gwdepth[f'DomGWP{i}'] = (merg_dom_gww_pop_gwdepth[f'DomGW_{i}'] / merg_dom_gww_pop_gwdepth[f'Pop_de{i}']) * 10**9

    PDom_GWW_GWdepth = merg_dom_gww_pop_gwdepth.drop(['OBJECTID_y', 'NAME_EN_y'] + [f'Pop_de{y}' for y in range(start_year, end_year + 1)], axis=1)
    PDom_GWW_GWdepth = PDom_GWW_GWdepth.rename(columns={'NAME_EN_x': 'NAME_EN', 'OBJECTID_x': 'OBJECTID'})
    PDom_GWW_GWdepth.to_file(driver='ESRI Shapefile', filename=fn_countries_Person_Dom_GWW_GWDepth)


Person_Dom_GWW (snakemake.input[0],snakemake.input[1], snakemake.params[0], snakemake.params[1], snakemake.output[0])
