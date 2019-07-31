import pandas as pd
from urllib import request
import json
import calendar

apiurl = 'https://www.minecraft.net/content/minecraft-net/_jcr_content.articles.grid?tagsPath=minecraft:article/culture&lang=/content/minecraft-net/language-masters/zh-hans&pageSize=100'

prev_data = pd.read_csv("culture.csv")
last_title = prev_data.loc[0]["Article Title"]

new_article_list = json.loads(request.urlopen(apiurl).read())['article_grid']
new_article_data = pd.DataFrame(columns=prev_data.columns)

for art in new_article_list:
    title = art['default_tile']['title']
    if title == last_title:
        break
    art_url = 'https://www.minecraft.net' + art['article_url']
    pub_date = art['publish_date'].split()
    pub_date = pub_date[2]+'/'+str(list(calendar.month_name).index(pub_date[1]))+'/'+pub_date[0]
    new_article_data.loc[len(new_article_data)]=[title,pub_date,art_url,'-','-']

pd.concat([new_article_data,prev_data]).to_csv(path_or_buf="culture.csv", index=False)