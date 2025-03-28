#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May  3 14:59:45 2024

@author: sara.nazari
"""
## ------------------------------------------------------------------------------------------------------- ##
#           Assign the representative countries annual per person domestic groundwater withdrawal          #
#                                where groundwater level is less than 100m                                 #
#                       to the countries that have no data from AQUASTAT or igrac                          #
## ------------------------------------------------------------------------------------------------------- ##

import geopandas as gpd

def Fill_no_data_Person_Dom_GWW(fn_countries_Person_Dom_GWW_GWDepth, start_year, end_year, fn_assigned_countries_Person_Dom_GWW_GWDepth):

    df_dom_gww_gwdepth = gpd.read_file(fn_countries_Person_Dom_GWW_GWDepth)
    df_dom_gww_gwdepth = df_dom_gww_gwdepth.set_index('NAME_EN')
    no_data_list = ['Singapore','Isle of Man','Jersey','Guernsey','Andorra','Angola','Anguilla','Antigua and Barbuda','Aruba','Bahamas','Barbados','Belize','Democratic Republic of the Congo',
                    'Greenland','Sudan','Chad','Angola','Ethiopia','Bolivia (Plurinational State of)','Mauritania','United Republic of Tanzania','Venezuela (Bolivarian Republic of)','Nigeria',
                    'Mozambique','South Sudan','Central African Republic','Papua New Guinea','Cameroon','Iraq','Ivory Coast','Gabon','Ecuador','Uganda','Ghana',"Lao People's Democratic Republic",
                    'Guyana','Syrian Arab Republic','Cambodia','Nepal','Nicaragua','Eritrea',"Democratic People's Republic of Korea",'Malawi','Guatemala','Liberia','Panama','Sierra Leone','Sri Lanka',
                    'Togo','Bhutan','Lesotho','Solomon Islands','Burundi','Haiti','Equatorial Guinea','Fiji','New Caledonia','Eswatini','Timor-Leste','Montenegro','Vanuatu','Falkland Islands','Gambia',
                    'Brunei Darussalam','Comoros','Hong Kong','Dominica','Saint Lucia','Saint Vincent and the Grenadines','United States Virgin Islands','Grenada']

    rep_list = ['Malaysia','United Kingdom of Great Britain and Northern Ireland','France','France','Spain','Zambia','Saint Kitts and Nevis','Saint Kitts and Nevis','Colombia','Jamaica',
                'Puerto Rico','Mexico','Congo','Iceland','Egypt','Niger','Congo','Somalia','Brazil','Senegal','Kenya','Brazil','Niger','South Africa','Kenya','Congo','Indonesia','Congo',
                'Iran (Islamic Republic of)','Burkina Faso','Congo','Peru','Kenya','Burkina Faso','Viet Nam','Brazil','Jordan','Viet Nam','India','Honduras','Djibouti','China','Zambia',
                'El Salvador','Guinea','Costa Rica','Guinea','India','Benin','India','South Africa','Indonesia','Rwanda','Dominican Republic','Congo','Indonesia','New Zealand',
                'South Africa','Indonesia','Albania','Indonesia','Argentina','Senegal','Malaysia','Madagascar','China','Saint Kitts and Nevis','Saint Kitts and Nevis','Saint Kitts and Nevis',
                'Puerto Rico','Trinidad and Tobago']


    for i in range(len(no_data_list)):
        for year in range(start_year, end_year + 1):
            df_dom_gww_gwdepth.loc[no_data_list[i], f'DomGWP{year}'] = df_dom_gww_gwdepth.loc[rep_list[i], f'DomGWP{year}']

    df_dom_gww_gwdepth.to_file(fn_assigned_countries_Person_Dom_GWW_GWDepth, driver='ESRI Shapefile')

Fill_no_data_Person_Dom_GWW(snakemake.input[0],snakemake.params[0], snakemake.params[1], snakemake.output[0])