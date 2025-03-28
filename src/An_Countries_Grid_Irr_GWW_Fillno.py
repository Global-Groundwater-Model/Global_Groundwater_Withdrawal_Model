#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 15 17:19:17 2024

@author: sara.nazari
"""

## --------------------------------------------------------------------------------------------------------- ##
#  Assign the representative countries annual per irrigated area grid irrigation groundwater withdrawal      #
#                        to the countries that have no data from AQUASTAT                                    #
## --------------------------------------------------------------------------------------------------------- ##

import geopandas as gpd
def Fill_no_data_Irr_Grid_Irr_GWW(fn_countries_Grid_Irr_GWW, start_year, end_year, fn_assigned_countries_Irr_Grid_Irr_GWW):

    No_data_list = ['Andorra','Angola','Barbados','Antigua and Barbuda','Belize','Bolivia (Plurinational State of)','Burundi','Cameroon','Chad',"Democratic People's Republic of Korea",'Ecuador','Eritrea','Eswatini','Ethiopia',
                    'Fiji','Guatemala','Guyana','Haiti','Iraq','Italy','Lesotho','Liberia','Liechtenstein','Malawi','Mauritania','Monaco','Montenegro','Mozambique','Nepal','Nicaragua','Nigeria','Panama','San Marino','Sierra Leone',
                    'South Sudan','Sri Lanka','Sudan','Syrian Arab Republic','Timor-Leste','Togo','Uganda','United Republic of Tanzania','United States Virgin Islands','Venezuela (Bolivarian Republic of)']
    
    
    Rep_list = ['France','Namibia','Puerto Rico','Saint Kitts and Nevis','Honduras','Chile','Rwanda','Central African Republic','Niger','Republic of Korea','Colombia','Djibouti','South Africa','Kenya','Solomon Islands','Honduras','Suriname','Cuba',
                'Iran (Islamic Republic of)','Austria','South Africa','Guinea','Austria','Zambia','Mali','France','Serbia','Zimbabwe','India','Costa Rica','Burkina Faso','Costa Rica','Austria','Guinea','Kenya','India','Niger',
                'Lebanon','Indonesia','Ghana','Democratic Republic of the Congo','Kenya','Saint Kitts and Nevis','Colombia']
    
    df_Irr_GWW = gpd.read_file(fn_countries_Grid_Irr_GWW)
    df_Irr_GWW = df_Irr_GWW.set_index('NAME_EN')  
    
    for i in range(0,44):
        
        for j in range(start_year, end_year+1):

            df_Irr_GWW.loc[No_data_list[i],'IrrGWG'+str(j)] = df_Irr_GWW.loc[Rep_list[i],'IrrGWG'+str(j)] 
            
    df_Irr_GWW.to_file(fn_assigned_countries_Irr_Grid_Irr_GWW, driver = 'ESRI Shapefile') 
    
Fill_no_data_Irr_Grid_Irr_GWW(snakemake.input[0], snakemake.params[0],snakemake.params[1],snakemake.output[0])