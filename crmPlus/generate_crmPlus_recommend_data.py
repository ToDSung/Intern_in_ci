import pandas as pd
import json
import numpy as np

client_info = pd.read_csv('client.csv')
with open('crmPlus.json', 'r') as js:
    recommend_data = json.load(js)

#SM = recommend_data[80]
#SM2 = recommend_data[81]
#SM3 = recommend_data[82]
SM4 = recommend_data[83]
#first writting method

'''
customer_num = []
revenue = []
industry_zhtw = []
related_customer1 = []
related_customer2 = []
related_customer3 = []
'''

# third writting method

customer_num = []
related_customer1 = []
related_customer2 = []
related_customer3 = []


all_target = pd.DataFrame(columns=['客戶代號', '客戶等級', '成立年限', '年營業額', '登記資本額', '購買四大ERP', '公司創立時間', '上市櫃', '負責人', '組織型態', '地區代號', '校正號行業代號', '校正號行業中文', '主要產品'])
#all_target2 = pd.DataFrame(columns=['客戶代號', '客戶等級', '成立年限', '年營業額', '登記資本額', '購買四大ERP', '公司創立時間', '上市櫃', '負責人', '組織型態', '地區代號', '校正號行業代號', '校正號行業中文', '主要產品'])


for index, target in enumerate(SM4['targetList']):
    
    # first writting method
    ''' 
    each_target = client_info[client_info['客戶代號'] == target['targetCustomer'] ]
    customer_num.append(str(target['targetCustomer']))
    revenue.append(each_target.loc[:,'年營業額'].values)
    industry_zhtw.append(each_target.loc[:,'校正號行業中文'].values) 
    related_customer1.append(target['relatedCustomers'][0])
    related_customer2.append(target['relatedCustomers'][1])
    related_customer3.append(target['relatedCustomers'][2])
    '''
    
    # second writting method but append realated_customers are very slow
    '''
    each_target = client_info[client_info['客戶代號'] == target['targetCustomer']]
    #each_target.loc[:, 'related_customer1'] = target['relatedCustomers'][0]
    #each_target.loc[:, 'related_customer2'] = target['relatedCustomers'][1]
    #each_target.loc[:, 'related_customer3'] = target['relatedCustomers'][2]
    
    
    # two append one row function are similar
    all_target = pd.concat([all_target, each_target], ignore_index = True)
    #all_target2 = all_target2.append(each_target, ignore_index = True)
    '''
    # third writting method combine first and second function
   
    
    customer_num.append(target['targetCustomer'])
    related_customer1.append(target['relatedCustomers'][0])
    related_customer2.append(target['relatedCustomers'][1])
    related_customer3.append(target['relatedCustomers'][2])
    


# first writting method    
    
'''
output_dict = {'customer_num': customer_num,
               'revenue': revenue,
               'industry_zhtw': industry_zhtw,
               'related_customer1': related_customer1,
               'related_customer2': related_customer2,
               'related_customer3': related_customer3
        }

output_df = pd.DataFrame(output_dict, dtype=str)
'''
# second writting method 
'''
output_df = all_target[['客戶代號', '年營業額', '校正號行業中文', 'related_customer1' , 'related_customer2' , 'related_customer3']]
'''

# third writting method

output_dict = {'客戶代號': customer_num,
               'related_customer1': related_customer1,
               'related_customer2': related_customer2,
               'related_customer3': related_customer3
        }
    
output_df = pd.DataFrame(output_dict)




# use pd.merge to compare column values
output_df = pd.merge(output_df, client_info, how = 'inner')
output_df= output_df[(output_df['購買四大ERP'] == 'e-Go 賣斷           ') | (output_df['購買四大ERP'].isnull())]

'''
output_df = output_df[['購買四大ERP']]
count = output_df.dropna()
count2 = count[count['購買四大ERP'] == 'e-Go 賣斷           ']

print(output_df.shape[0]-count.shape[0]+count2.shape[0])
'''

output_df2 = output_df[['客戶代號', '客戶等級','年營業額', '校正號行業中文', 'related_customer1' , 'related_customer2' , 'related_customer3']]

# for caculate customer rank counts
'''
customer_ranks = client_info.loc[:,'客戶等級'].unique()
print(customer_ranks)

for rank in customer_ranks:
    output_df3 = output_df2[output_df2['客戶等級'] == rank]
    print(rank, end = ': ')
    print(output_df3.shape[0])
'''
#output_df['related_customer1'].apply(lambda x: '{:.0f}'.format(x))

# number will be cut
#output_df2.to_csv('crmPlusOutput_cutERP.csv', index=False, encoding='utf_8_sig')

#integrity data 
#output_df2.to_excel('crmPlusOutput_cutERP.xlsx', index=False, encoding='utf_8_sig')