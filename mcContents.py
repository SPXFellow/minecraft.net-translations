import pandas as pd
from urllib import request
from dateutil import parser
import json
import sys, os
from bs4 import BeautifulSoup

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
    catPath = "config.json"
    uidPath = "uid.json"
    with open(catPath, "r", encoding="utf-8") as f:
        cats = json.loads(f.read())
    with open(uidPath, "r", encoding="utf-8") as f:
        uid2name = json.loads(f.read())
        
    
    def uidUpdate():
        '''
            将uid.json中已有的uid项目进行全部的更新。
        '''
        pass
    
    def nameGet(uid):
        '''
            返回对应uid的用户名，如果遇到未缓存的uid，则添加到uid.json中。
        '''
        if uid not in uid2name:
            assert(int(uid) > 0)
            usrUrl = 'https://www.mcbbs.net/home.php?mod=space&uid=' + uid
            usrName = BeautifulSoup(request.urlopen(usrUrl).read(),"html.parser").find("title").text[:-len("的个人资料 -  Minecraft(我的世界)中文论坛 - ")]
            uid2name[uid] = usrName
            with open(uidPath, "w", encoding="utf-8") as f:
                json.dump(uid2name, f, ensure_ascii=False, indent=4)


            
        return uid2name[uid]
    
    def toMarkdownTable(table, filename):
        '''
            将处理好的表格转换成markdown表格，便于阅读。
        '''
        yes = "![](https://www.mcbbs.net/static/image/smiley/mcitem/emerald.png)|"
        no = "![](https://www.mcbbs.net/static/image/smiley/ornaments/barrier.png)|"
        with open(filename+".md", "w", encoding="utf-8") as f:
            strs = []



            header = "|日期|原文|译文|译者|认证|"
            splitter = "|---|---|---|---|---|"
            strs += [header, splitter]

            for _, rec in table.iterrows():
                try:
                    thisstr = "|"
                    thisstr += rec["发布日期"] + "|"
                    thisstr += "[" + rec["原文标题"] + "]("+ rec["原文链接"] + ")|"
                    thisstr += "[" + rec["译文标题"] + "]("+ rec["译文链接"] + ")|" if rec["译文标题"] != "-" else "-|"
                    thisstr += rec["译者"] + "|"
                    thisstr += yes if rec["认证"] else no
                    strs.append("".join(thisstr))
                except TypeError:
                    print(rec)
                    


            strs = [s + "\n" for s in strs]
            f.writelines(strs)

    data = pd.read_csv("rawtable.csv", encoding='utf-8')
    tables = {}
    for cat in cats:
        tables[cat] = pd.DataFrame(columns=["发布日期","原文标题","原文链接","译文标题","译文链接","译者","认证"])
    
    for i, rec in data.iterrows():
        thiscat = rec["cat"]
        tr_name = nameGet(rec["tr_uid"])
        emeralded = True if int(rec["emeralded"]) == 1 else False
        tables[thiscat].loc[len(tables[thiscat])]= list(data.iloc[i][:-3])+[tr_name, emeralded] # rawtable[:-3]的记录顺序和输出表一致
    
    for cat in cats:
        print("making", cat)
        toMarkdownTable(tables[cat], cats[cat])
    
    pass

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
