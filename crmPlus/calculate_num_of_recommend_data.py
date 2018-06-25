import pandas as pd
import json

client_info = pd.read_csv('client.csv')
with open('crmPlus.json', 'r') as js:
    recommend_data = json.load(js)

each_product_name = []
each_limit_factor = []
each_num_tareget = []
for each in recommend_data:
    each_product_name.append(each['productCatName'])
    each_limit_factor.append(each['limitFactor'])
    each_num_tareget.append(len(each['targetList']))
    
output_dict = {'product_cat_name' : each_product_name,
               'limit_factor' : each_limit_factor,
               'num_target' : each_num_tareget
               }

output_df = pd.DataFrame(output_dict)
output_df = output_df[['product_cat_name', 'limit_factor', 'num_target']]
output_df.to_excel('crm_num_statistical.xlsx', index=False, encoding='utf_8_sig')
    