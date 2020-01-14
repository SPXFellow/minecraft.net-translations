import pandas as pd
from urllib import request
from dateutil import parser
import json
import sys, os

def pull():
    apiurl = 'https://www.minecraft.net/content/minecraft-net/_jcr_content.articles.grid?tagsPath=minecraft:article/insider,minecraft:article/culture&lang=/content/minecraft-net/language-masters/zh-hans&pageSize=100'
    
    print("Pulling raw json file...")
    prev_data = pd.read_csv("rawtable.csv", encoding='utf-8')
    last_5_titles = [prev_data.loc[x]["title"] for x in range(5)]
    last_pub = parser.parse(prev_data.loc[0]["published"])

    new_article_list = json.loads(request.urlopen(apiurl).read())['article_grid']
    new_article_data = pd.DataFrame(columns=prev_data.columns)


    for art in new_article_list:
        title = art["default_tile"]["title"]
        pub = parser.parse(art["publish_date"]).replace(tzinfo=None)
        
        if title in last_5_titles or pub < last_pub:
            break
        
        print("Adding new article:", title)
        link = 'https://www.minecraft.net' + art["article_url"]
        pub = str(pub.year) + "/" + str(pub.month) + "/" + str(pub.day)
        cat = art["primary_category"].lower()
        new_article_data.loc[len(new_article_data)]=[pub,title,link,'-','-','-','0',cat] # tr title, tr link, tr uid
    
    pd.concat([new_article_data,prev_data]).to_csv(path_or_buf="rawtable.csv", index=False, encoding='utf-8')
    print("Successfully pulled.")

def render():
    with open("config.json") as f:
        cats = json.loads(f.read())
    with open("uid.json") as f:
        uid = json.loads(f.read())

    tables = {}
    for cat in cats:
        tables[cat] = pd.DataFrame(columns=["发布日期","原文标题","原文链接","译文标题","译文链接","译者","认证"])
    data = pd.read_csv("rawtable.csv", encoding='utf-8')
    
    for i in range(len(data)):
        thiscat = data.iloc[i]["cat"]
        rec = data.iloc[i][:-1]
        rec[""]
        tables[thiscat].loc[len(tables[thiscat])] = data.iloc[i][:-1]
    
    for t in tables:



def bbcode():
    print("Not support now")


def showHelp():
    print("Usage: mcContent.py <pull|render|bbcode>")
    print("\tpull - Get latest articles and write to rawtable.csv")
    print("\trender - Divide rawtable.csv into different files according to config.json")
    print("\tbbcode - Output bbcode table with articles in corresponding category")

if __name__ == "__main__":
    for i in sys.argv[1:]:
        if i not in ["pull", "render", "bbcode"]:
            showHelp()
            exit()
    for opr in sys.argv[1:]:
        if opr == "pull":
            pull()
        elif opr == "render":
            render()
        elif opr == "bbcode":
            bbcode()
