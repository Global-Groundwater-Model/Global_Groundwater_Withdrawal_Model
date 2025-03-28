#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 15 15:13:15 2024

@author: sara.nazari
"""

## ------------------------------------------------------------------------------------------------------- ##
#         Assign the representative countries irrigation fraction of the total groundwater withdrawal      #
#         to the countries that have the total groundwater withdrawal but not the irrigation fraction      #
#                         and then calculate the irrigatioon groundwater withdrawal                        #
## ------------------------------------------------------------------------------------------------------- ##


import geopandas as gpd
def Fill_no_data_frac_Irr(fn_Irr_GWW_Eu_World,start_year, end_year, fn_Irr_GWW_country_Fillno_IrrFrac):
     
    No_data_frac_Irr_list = ['Palestine','Namibia','Viet Nam','Azerbaijan','Armenia','Zambia','Djibouti','Botswana','Zimbabwe','Dominican Republic',
                             'El Salvador','Myanmar','Cuba','Honduras','Burkina Faso','Guinea-Bissau','Trinidad and Tobago','Saint Kitts and Nevis','Bahrain','Mali','Rwanda']
    
    Rep_frac_Irr_list = ['Jordan','South Africa','Thailand','Turkiye','Turkiye','Kenya','Somalia','South Africa','South Africa','Jamaica','Costa Rica','India',
                         'Jamaica','Jamaica','Niger','Niger','Puerto Rico','Puerto Rico','Qatar','Algeria','Niger']
    
    df_Irr_GWW = gpd.read_file(fn_Irr_GWW_Eu_World)
    df_Irr_GWW = df_Irr_GWW.set_index('NAME_EN')
    
    for i in range (0, end_year-start_year+1):#(0,21):
        df_Irr_GWW.loc[No_data_frac_Irr_list[i],'Irr_Frac']= df_Irr_GWW.loc[Rep_frac_Irr_list[i],'Irr_Frac']
        for j in range(start_year, end_year+1):
            df_Irr_GWW.loc[No_data_frac_Irr_list[i],'IrrGW_'+str(j)]= df_Irr_GWW.loc[No_data_frac_Irr_list[i],'Irr_Frac']*df_Irr_GWW.loc[No_data_frac_Irr_list[i],'TGWW_'+str(j)]
      
    df_Irr_GWW.to_file(fn_Irr_GWW_country_Fillno_IrrFrac,driver = 'ESRI Shapefile') 

Fill_no_data_frac_Irr(snakemake.input[0],snakemake.params[0], snakemake.params[1],snakemake.output[0])