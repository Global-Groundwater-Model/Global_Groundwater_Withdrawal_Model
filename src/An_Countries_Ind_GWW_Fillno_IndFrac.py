#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 12 21:13:38 2024

@author: sara.nazari
"""

## ------------------------------------------------------------------------------------------------------- ##
#         Assign the representative countries industrial fraction of the total groundwater withdrawal      #
#         to the countries that have the total groundwater withdrawal but not the industrial fraction      #
#                          and then calculate the industrial groundwater withdrawal                        #
## ------------------------------------------------------------------------------------------------------- ##

import geopandas as gpd

def Fill_no_data_frac_Ind(fn_Ind_GWW_country, start_year, end_year, fn_Ind_GGW_country_Fillno_IndFrac):
   
    No_data_frac_Ind_list = ['Pakistan','Republic of Korea','Myanmar','Cuba','Azerbaijan','Viet Nam','Armenia','Zimbabwe','Georgia','Dominican Republic','Palestine','Iceland',
                             'Honduras','Bahrain','Botswana','Namibia','Republic of Moldova','El Salvador','Rwanda','Trinidad and Tobago','Guinea','Zambia','Mali','Suriname',
                             'Benin','Guinea-Bissau','Djibouti','Madagascar','Burkina Faso','Saint Kitts and Nevis', 'Bosnia and Herzegovina', 'Bulgaria','Croatia','Czechia'
                             ,'Lithuania','Luxembourg','Latvia','North Macedonia','Serbia']
    
    Rep_frac_Ind_list = ['India','Japan','India','Jamaica','Turkiye','Thailand','Turkiye','South Africa','Turkiye','Jamaica','Jordan','United Kingdom of Great Britain and Northern Ireland',
                         'Jamaica','Qatar','South Africa','South Africa','Romania','Costa Rica','Somalia','Puerto Rico','Niger','Kenya','Algeria','Brazil','Niger','Niger','Somalia',
                         'South Africa','Niger','Puerto Rico', 'Hungary','Turkiye','Hungary','Hungary','Estonia','Germany','Estonia','Albania','Romania']
    
    df_Ind_GWW = gpd.read_file(fn_Ind_GWW_country)
    df_Ind_GWW = df_Ind_GWW.set_index('NAME_EN')

    for i in range(0,39):
        df_Ind_GWW.loc[No_data_frac_Ind_list[i],'Ind_Frac']= df_Ind_GWW.loc[Rep_frac_Ind_list[i],'Ind_Frac']
        for j in range(start_year, end_year+1):
            df_Ind_GWW.loc[No_data_frac_Ind_list[i],'IndGW_'+str(j)]= df_Ind_GWW.loc[No_data_frac_Ind_list[i],'Ind_Frac']*df_Ind_GWW.loc[No_data_frac_Ind_list[i],'TGWW_'+str(j)]
      
    df_Ind_GWW.to_file(fn_Ind_GGW_country_Fillno_IndFrac,driver = 'ESRI Shapefile') 
    
Fill_no_data_frac_Ind(snakemake.input[0], snakemake.params[0], snakemake.params[1], snakemake.output[0])