# -*- coding: utf-8 -*-
"""
Created on Thu May 17 13:34:07 2018

@author: ci
"""

import pandas as pd
import sys
source = pd.read_excel('mi-cdri-20180515.xlsx')
keyword = pd.read_excel('cdri-keyword.xlsx')


material_category = keyword.iloc[:,0].dropna().drop([0])
chain = keyword.iloc[:,3].dropna().drop([0])
field = keyword.iloc[:,4].dropna().drop([0])
product = keyword.iloc[:,5].dropna().drop([0])

#row
material_name = keyword.iloc[:,2].dropna().drop([0]) + ' ' + keyword.iloc[:,1].dropna().drop([0])

#column
column_name = material_category.append(chain).append(field).append(product)

step1 = source[source['matches'] > 1 ]
step2=step1.drop(['g_date'], axis=1).drop(['matches'], axis=1)

timezone = step2.sort_values('cdr')['cdr'].unique()

df = pd.DataFrame()  
        
'''
for time in timezone:
    small_df = step2[step2['cdr']== time]
    for material in material_name:
        small_df2 = small_df[small_df['a'] == material]
        row = pd.DataFrame()
        for  column in column_name:        
            small_df3 = small_df2[small_df2['b'] == column ]
            row.loc[material,column] = small_df3.shape[0]
        row.loc[material,'time'] = time    
        df = df.append(row)
'''

#semiconductor packaging 在column中出現兩次

total1=0
total2=0
total3=0

 
for material in material_name:
    small_df = step2[step2['a'] == material]
    #total1 += small_df.shape[0]
    for time in timezone:
        small_df2 = small_df[small_df['cdr']== time]
        total2 += small_df2.shape[0]
        row = pd.DataFrame()
        for column in column_name:        
            small_df3 = small_df2[small_df2['b'] == column ]
            total3 += small_df3.shape[0]
            
            row.loc[material,column] = small_df3.shape[0]
        row.loc[material,'time'] = time    
        df = df.append(row)
        print(total2)
        print(total3)
'''    
    
print(total1)
print(total2)
print(total3)

'''
    
print('done')
#df.to_excel('test2.xlsx')