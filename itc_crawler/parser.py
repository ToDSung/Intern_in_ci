
# coding: utf-8

# In[101]:


import pandas as pd
from pyquery import PyQuery

file = pd.read_pickle('test.pickle')
html_source = file[2]
#print(html_source)

dom = PyQuery(html_source)
table = dom('#ctl00_ContentPlaceHolder1_grdProductView_ctl00 > tbody > tr')
#print(table)

row_list = []

for tr in table.items('tr'):
    
    # 註解處 為 較快速取得<tr>內全部text並逐行轉換成list的方法，但遇到空值時，list 會出現缺少的情況，不利於轉成 dataframe 的格式
    '''
    each_row = tr.text().splitlines()
    row_list.append(each_row)
    print(each_row)
print(row_list)
'''
    # 取代下面三行
    each_row = [ td.html() for td in tr.items('td')]
    '''
    for td in tr.items('td'):
        print(td.html())
        each_row.append(td.html())
    print(each_row)
    '''
    row_list.append(each_row)
labels = ['hscode', 'product description', 'tariff', 'tariff_lines_num']
df = pd.DataFrame.from_records(data = row_list, columns=labels)

print(df)
df.to_csv('test.csv', index=False, encoding='utf-8')

