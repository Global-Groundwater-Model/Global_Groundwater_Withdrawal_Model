#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 15 10:10:46 2024

@author: sara.nazari
"""

## ------------------------------------------------------------------------------------------------------- ##
#  Assign the representative countries annual per urban-mining grid industrial groundwater withdrawal      #
#                        to the countries that have no data from AQUASTAT                                  #
## ------------------------------------------------------------------------------------------------------- ##

import geopandas as gpd

def Fill_no_data_Grid_Ind_GWW (fn_Countries_Grid_Ind_GWW,start_year, end_year, fn_assigned_countries_Grid_Ind_GWW):
    
    No_data_list = ['Singapore','Isle of Man','Jersey','Guernsey','Andorra','Angola','Anguilla','Antigua and Barbuda','Aruba','Bahamas','Barbados','Belize','Democratic Republic of the Congo',
                    'Greenland','Sudan','Chad','Ethiopia','Bolivia (Plurinational State of)','Mauritania','United Republic of Tanzania','Venezuela (Bolivarian Republic of)','Nigeria',
                    'Mozambique','South Sudan','Central African Republic','Papua New Guinea','Cameroon','Iraq','Ivory Coast','Gabon','Ecuador','Uganda','Ghana',"Lao People's Democratic Republic",
                    'Guyana','Syrian Arab Republic','Cambodia','Nepal','Nicaragua','Eritrea',"Democratic People's Republic of Korea",'Malawi','Guatemala','Liberia','Panama','Sierra Leone','Sri Lanka',
                    'Togo','Bhutan','Lesotho','Solomon Islands','Burundi','Haiti','Equatorial Guinea','Fiji','New Caledonia','Eswatini','Timor-Leste','Montenegro','Vanuatu','Falkland Islands','Gambia',
                    'Brunei Darussalam','Comoros','Hong Kong','Dominica','Saint Lucia','Saint Vincent and the Grenadines','United States Virgin Islands','Grenada','Italy','Liechtenstein','Monaco','Norway',
                    'San Marino']
        
    Rep_list = ['Malaysia','United Kingdom of Great Britain and Northern Ireland','France','France','Spain','Zambia','Saint Kitts and Nevis','Saint Kitts and Nevis','Colombia',
                'Jamaica','Puerto Rico','Mexico','Congo','Iceland','Egypt','Niger','Somalia','Brazil','Senegal','Kenya','Brazil','Niger','South Africa','Kenya','Congo',
                'Indonesia','Congo','Iran (Islamic Republic of)','Burkina Faso','Congo','Peru','Kenya','Burkina Faso','Viet Nam','Brazil','Jordan','Viet Nam','India',
                'Honduras','Djibouti','China','Zambia','El Salvador','Guinea','Costa Rica','Guinea','India','Benin','India','South Africa','Indonesia','Rwanda',
                'Dominican Republic', 'Congo','Indonesia','New Zealand','South Africa','Indonesia','Albania','Indonesia','Argentina','Senegal','Malaysia','Madagascar',
                'China','Saint Kitts and Nevis','Saint Kitts and Nevis','Saint Kitts and Nevis','Puerto Rico','Trinidad and Tobago','Austria','Austria','France','Sweden','Austria']

    df_Ind_GWW_mining_GWdepth = gpd.read_file(fn_Countries_Grid_Ind_GWW)
    df_Ind_GWW_mining_GWdepth = df_Ind_GWW_mining_GWdepth.set_index('NAME_EN')

    for i in range(0,75):
        
        for j in range(start_year, end_year+1):
            
            df_Ind_GWW_mining_GWdepth.loc[No_data_list[i],'InGW_G'+str(j)] = df_Ind_GWW_mining_GWdepth.loc[Rep_list[i],'InGW_G'+str(j)] 
            
    df_Ind_GWW_mining_GWdepth.to_file(fn_assigned_countries_Grid_Ind_GWW,driver = 'ESRI Shapefile') 
    
Fill_no_data_Grid_Ind_GWW (snakemake.input[0],snakemake.params[0],snakemake.params[1],snakemake.output[0])