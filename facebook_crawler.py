# -*- coding: utf-8 -*-

import facebook
import requests
from bs4 import BeautifulSoup
from dateutil.parser import parse
import pandas as pd


token='EAACEdEose0cBAEwsSkb1wcaZBUfWUS04KzI3ttdZB15OPx42VxkqpxsjYytZA5wXjLD6YHhUWnYILLZCZChLnAAgFDZCSrTZCTtIU7irLnVMCayj2b43tYZCVdsWtBTjY2LyLtlZBZCF0HZBdOFOEi4lkDqJDobU5wyRqm1hPIWZB2cpXTr10wqX3DrtC8xAKUywkRPp0EubYfcTbbhRMA5vLezLQ0dYjjy5IlEZD'

graph=facebook.GraphAPI(access_token=token)

fanpage_info = graph.get_object('CCUCNA', filed='id')

fanpages = { fanpage_info['id']: fanpage_info['name']}
# 建立一個空的list        

information_list = []

# 使用for迴圈依序讀取粉絲頁的資訊，並使用format將id與token傳入{}裡

for fanpage_id in fanpages:
    res = requests.get('https://graph.facebook.com/v2.12/{}/posts?limit=100&access_token={}'.format(fanpage_id, token))
    
    # API最多一次呼叫100筆資料，因此使用while迴圈去翻頁取得所有的資料
    
    pages = 1  # 初始化爬取頁數
    
    while pages < 10: 
        print('目前正在爬取 {} {} 第{}頁'.format(fanpage_id, fanpages[fanpage_id], pages))
        for information in res.json()['data']:
            if 'message' in information:
                
                res2=requests.get('https://graph.facebook.com/{}/likes?summary=true&access_token={}'.format(information['id'], token))
                article_likes=res2.json()['summary']['total_count']
                
                information_list.append([fanpages[fanpage_id], information['message'], parse(information['created_time']).date(), article_likes])
        # 若有下一頁，則繼續爬取，否則跳出While迴圈

        if 'next' in res.json()['paging']:
            res = requests.get(res.json()['paging']['next'])
            pages += 1
        else:
            print('{} {} 已爬取完成! \n'.format(fanpage_id, fanpages[fanpage_id]))
            break
    
# 最後將list轉換成dataframe，並輸出成Excel檔

#information_df = pd.DataFrame(information_list, columns=['粉絲專頁', '發文內容', '發文時間'])
#information_df.to_excel('Data Visualization Information.xlsx', index=False)  