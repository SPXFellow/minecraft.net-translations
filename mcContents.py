import pandas as pd
from urllib import request
import json
import calendar

def update(cate: str):
    # 根据分类确定api
    apiurl = 'https://www.minecraft.net/content/minecraft-net/_jcr_content.articles.grid?tagsPath=minecraft:article/' + cate + '&lang=/content/minecraft-net/language-masters/zh-hans&pageSize=100'

    # 获取之前的记录
    prev_data = pd.read_csv(cate+"_gb.csv", encoding='gb18030')
    last_title = prev_data.loc[0]["Article Title"]

    # 获取新的数据，建立空表
    print("Loading info of", cate + "...")
    new_article_list = json.loads(request.urlopen(apiurl).read())['article_grid']
    new_article_data = pd.DataFrame(columns=prev_data.columns)

    print("Updating csv...")
    for art in new_article_list:
        title = art['default_tile']['title']
        if title == last_title: # 在比对到原有的记录时退出
            break
        art_url = 'https://www.minecraft.net' + art['article_url']
        pub_date = art['publish_date'].split()
        pub_date = pub_date[2]+'/'+str(list(calendar.month_name).index(pub_date[1]))+'/'+pub_date[0]

        # 往空表追加新行
        new_article_data.loc[len(new_article_data)]=[title,pub_date,art_url,'-','-']

    # 合并新旧表，保存
    pd.concat([new_article_data,prev_data]).to_csv(path_or_buf=cate+".csv", index=False, encoding='utf-8')
    pd.concat([new_article_data,prev_data]).to_csv(path_or_buf=cate+"_gb.csv", index=False, encoding='gb18030')
    print("Saving", cate + ".")

# 更新csv
update('insider')
update('culture')
