#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov  3 10:34:39 2023

@author: sara.nazari
"""

## ------------------------------------------------------------------------------------------------------- ##
#           Assign the representative countries domestic fraction of the total groundwater withdrawal      #
#           to the countries that have the total groundwater withdrawal but not the domestic fraction      #
#                            and then calculate the domestic groundwater withdrawal                        #
## ------------------------------------------------------------------------------------------------------- ##


import geopandas as gpd

def Fill_no_data_frac_dom(fn_Dom_GWW_Eu_World, start_year, end_year, fn_Dom_GGW_country_Fillno_DomFrac):
    df_dom_gww = gpd.read_file(fn_Dom_GWW_Eu_World)
    df_dom_gww = df_dom_gww.set_index('NAME_EN')
    no_data_Frac_Dom_list = ['Pakistan', 'Republic of Korea', 'Myanmar', 'Cuba', 'Azerbaijan', 'Viet Nam', 'Armenia', 'Zimbabwe', 'Georgia', 'Dominican Republic', 'Palestine', 'Iceland',
                             'Honduras', 'Bahrain', 'Botswana', 'Namibia', 'Republic of Moldova', 'El Salvador', 'Rwanda', 'Trinidad and Tobago', 'Guinea', 'Zambia', 'Mali', 'Suriname',
                             'Benin', 'Guinea-Bissau', 'Djibouti', 'Madagascar', 'Burkina Faso', 'Saint Kitts and Nevis']

    rep_Frac_Dom_list = ['India', 'Japan', 'India', 'Jamaica', 'Turkiye', 'Thailand', 'Turkiye', 'South Africa', 'Turkiye', 'Jamaica', 'Jordan', 'United Kingdom of Great Britain and Northern Ireland',
                         'Jamaica', 'Qatar', 'South Africa', 'South Africa', 'Romania', 'Costa Rica', 'Somalia', 'Puerto Rico', 'Niger', 'Kenya', 'Algeria', 'Brazil', 'Niger', 'Niger', 'Somalia',
                         'South Africa', 'Niger', 'Puerto Rico']
    for i in range(len(no_data_Frac_Dom_list)):
        df_dom_gww.loc[no_data_Frac_Dom_list[i], 'Dom_Frac'] = df_dom_gww.loc[rep_Frac_Dom_list[i], 'Dom_Frac']
        for j in range(start_year, end_year + 1):
            df_dom_gww.loc[no_data_Frac_Dom_list[i], f'DomGW_{j}'] = df_dom_gww.loc[no_data_Frac_Dom_list[i], 'Dom_Frac'] * df_dom_gww.loc[no_data_Frac_Dom_list[i], f'TGWW_{j}']
  
    df_dom_gww.to_file(fn_Dom_GGW_country_Fillno_DomFrac, driver='ESRI Shapefile')

Fill_no_data_frac_dom(snakemake.input[0], snakemake.params[0], snakemake.params[1], snakemake.output[0])