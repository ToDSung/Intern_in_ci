import pandas as pd


source1 = pd.read_csv('./MI_1.csv')
source1 = source1.drop(columns = ['Unnamed: 5'])
source1 = source1.loc[1:]
source1.columns = ['keyworld1','keyworld2','keyworld3','search_time','counts_result',]

source2 = pd.read_csv('./MI_2.csv')
source2 = source2.drop(columns = ['Unnamed: 5'])
#source2 = source2.loc[1:]
source2.columns = ['keyworld1','keyworld2','keyworld3','search_time','counts_result',]

source3 = pd.read_csv('./MI_3.csv')
source3 = source3.drop(columns = ['Unnamed: 5'])
source3 = source3.loc[1:]
source3.columns = ['keyworld1','keyworld2','keyworld3','search_time','counts_result',]

source4 = pd.read_csv('./MI_4.csv')
source4 = source4.drop(columns = ['Unnamed: 5'])
source4 = source4.loc[1:]
source4.columns = ['keyworld1','keyworld2','keyworld3','search_time','counts_result',]

source5 = pd.read_csv('./MI_5.csv')
source5 = source5.drop(columns = ['Unnamed: 5'])
source5.columns = ['keyworld1','keyworld2','keyworld3','search_time','counts_result',]

source6 = pd.read_csv('./MI_6.csv')
source6 = source6.drop(columns = ['Unnamed: 5'])
source6.columns = ['keyworld1','keyworld2','keyworld3','search_time','counts_result',]

source7 = pd.read_csv('./MI_7.csv')
source7 = source7.drop(columns = ['Unnamed: 5'])
source7 = source7.loc[1:]
source7.columns = ['keyworld1','keyworld2','keyworld3','search_time','counts_result',]

source8 = pd.read_csv('./MI_8.csv')
source8 = source8.drop(columns = ['Unnamed: 5'])
source8 = source8.loc[1:]
source8.columns = ['keyworld1','keyworld2','keyworld3','search_time','counts_result',]

source9 = pd.read_csv('./MI_9.csv')
source9 = source9.drop(columns = ['Unnamed: 5'])
source9 = source9.loc[1:]
source9.columns = ['keyworld1','keyworld2','keyworld3','search_time','counts_result',]

source10 = pd.read_csv('./MI_10.csv')
source10 = source10.drop(columns = ['Unnamed: 5'])
source10 = source10.loc[1:]
source10.columns = ['keyworld1','keyworld2','keyworld3','search_time','counts_result',]


def strip2(a):
    return a.strip('“').strip('”').strip('"')

all_source = pd.concat([source1, source2, source3, source4, source5, source6, source7, source8, source9, source10])

#'green energy_class', 'high-tech_class', 'military_class', 'smart machinery_class', 'medical industry_class', 'agriculture_class', 'circular economy_class',
#column_name = ['production','packaging', 'process', 'distributing', 'marketing', 'end-user',
#               'green energy', 'high-tech', 'military', 'smart machinery', 'medical industry', 'agriculture', 'circular economy',
#               'timezone']
timezone = ['2016/4/1-2016/9/30', '2016/10/1-2017/3/31', '2017/4/1-2017/9/30','2017/10/1-2018/3/31']

all_source = all_source.drop_duplicates()
all_source = all_source.applymap(str).applymap(strip2)
all_source['counts_result'] = all_source['counts_result'].map(float)

all_df = pd.DataFrame(columns=['Abb', 'Product', '2016/4/1-2016/9/30', '2016/10/1-2017/3/31', '2017/4/1-2017/9/30','2017/10/1-2018/3/31'])
df = pd.DataFrame(columns=['Abb', 'Product', '2016/4/1-2016/9/30', '2016/10/1-2017/3/31', '2017/4/1-2017/9/30','2017/10/1-2018/3/31'])
keyworld_list = all_source.loc[:,'keyworld1'].map(strip2).unique()

chain_product_list = ['production','packaging','process','distributing','marketing','end-user',
                      #'green energy', 'high-tech', 'military', 'smart machinery', 'medical industry','agriculture', 'circular economy',
                      'wind turbine blades', 'turbine blades', 'oil seal', 'drive belt', 'led package', 
                      'weathering resistant coating', 'light guide plate', 'lens', 'optical film',
                      'flexible display', 'touch panel', 'semiconductor packaging', 'communication antenna', 
                      'high frequency substrate', 'wafer tray', 'electrical connector',  
                      'seal component', 'drone lightweight component',
                      'aviation seat', 'transmission shaft seal kit', 'missile power', 
                      'lightweight bearings ', 'lightweight gear', 'temperature resistant cable', 'mechanical structure',
                      'spinning intelligent monitoring system', 'robotic lightweight component', 'oil resistant cable', 
                      'walker', 'wheelchair', 'cane', 'drainage bag', 'dialysis media', 'antibacterial cotton swab',
                      'antibacterial gauze', 'antibacterial bandage', '3D printing material', 
                      'geomembrane film', 'silage film', 'greenhouse covering film', 'bulk bag', 'bulk container', 
                      'corrugated fiberboard', 'clamshell packaging', 'stretch film', 'filter media', 'water absorbing material', 'led light', 
                      'plastic bottle', 'tires', 'clothes','safe toys', 'cosmetics', 'shoes']
#print(chain_product_list)
#print(keyworld_list)

for each_keyworld in keyworld_list:
    all_source2 = all_source[all_source['keyworld1'] == each_keyworld]
    for chain_product in chain_product_list:
        all_source3 = all_source2[all_source2['keyworld3'] == chain_product]
        df.loc[0,'Abb'] = each_keyworld
        df.loc[0,'Product'] = chain_product
        for time in timezone:
            all_source4 = all_source3[all_source3['search_time'] == time]

            #print(all_source4.iloc[0,4])
            try:
                df.loc[0, time] = all_source4.iloc[0,4]
            except:
                df.loc[0, time] = 0
                print(each_keyworld)
                print(chain_product)
                print(time)
        all_df = all_df.append(df, ignore_index=True)


all_df.loc[:,'TOTAL'] = all_df[['2016/4/1-2016/9/30', '2016/10/1-2017/3/31', '2017/4/1-2017/9/30','2017/10/1-2018/3/31']].sum(axis=1)
print('done')
# number will be cut
#all_df.to_csv('matrial_output.csv', index=False, encoding='utf_8_sig')

#integrity data 
#all_df.to_excel('matrial_output.xlsx', index=False, encoding='utf_8_sig')
    
    