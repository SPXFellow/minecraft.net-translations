import pandas as pd
from urllib import request
from dateutil import parser
import json
import sys, os
from bs4 import BeautifulSoup

def pull():
    categories = [
        "minecraft:article/insider",
        "minecraft:article/culture",
        "minecraft:stockholm/news",
        "minecraft:stockholm/guides",
        "minecraft:stockholm/events",
        "minecraft:stockholm/minecraft-builds",
        "minecraft:stockholm/marketplace",
        "minecraft:stockholm/deep-dives",
        "minecraft:stockholm/merch"
    ]
    #catestr = ",".join(categories)
    #apiurl = 'https://www.minecraft.net/content/minecraft-net/_jcr_content.articles.grid?tagsPath=' + catestr + '&lang=/content/minecraft-net/language-masters/zh-hans&pageSize=100'
    apiurl = 'https://www.minecraft.net/content/minecraft-net/_jcr_content.articles.grid?pageSize=30'
    
    print("Pulling raw json file from api", apiurl)
    prev_data = pd.read_csv("rawtable.csv", encoding='utf-8')
    last_titles = [prev_data.loc[x]["title"] for x in range(50)]

    new_article_list = json.loads(request.urlopen(apiurl).read())['article_grid']
    new_article_data = pd.DataFrame(columns=prev_data.columns)

    for art in new_article_list:
        title = art["default_tile"]["title"]
        pub = parser.parse(art["publish_date"]).replace(tzinfo=None)
        
        if title in last_titles:
            continue
        
        print("Adding new article:", title)
        if "linkurl" in art["default_tile"]["image"]:
            link = art["default_tile"]["image"]["linkurl"]
        else:
            link = 'https://www.minecraft.net' + art["article_url"]
        pub = str(pub.year) + "/" + str(pub.month) + "/" + str(pub.day)
        cat = art["primary_category"].lower()
        new_article_data.loc[len(new_article_data)]=[pub,title,link,'-','-','-','0',cat] # tr title, tr link, tr uid
    
    pd.concat([new_article_data,prev_data]).to_csv(path_or_buf="rawtable.csv", index=False, encoding='utf-8')
    if len(new_article_data) != 0:
        print("Successfully pulled.")
    else:
        print("Already up-to-date.")
    pass

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

    def uidGet(link:str):
        '''
            获取指定链接的发帖者 uid。
        '''
        return BeautifulSoup(request.urlopen(link).read(),"html.parser").find("div",class_="authi").a.attrs["href"][len("home.php?mod=space&uid="):]
    
    def nameGet(uid):
        '''
            返回对应uid的用户名，如果遇到未缓存的uid，则添加到uid.json中。
        '''
        if uid not in uid2name:
            assert(int(uid) > 0)
            usrUrl = 'https://www.mcbbs.net/home.php?mod=space&uid=' + uid
            usrName = BeautifulSoup(request.urlopen(usrUrl).read(),"html.parser").find("title").text[:-len("的个人资料 -  Minecraft(我的世界)中文论坛 - ")]
            uid2name[uid] = usrName
            print("Welcome new translator:", usrName)
            with open(uidPath, "w", encoding="utf-8") as f:
                json.dump(uid2name, f, ensure_ascii=False, indent=4)
        return uid2name[uid]
    
    def toMarkdownTable(table, filename):
        '''
            将处理好的表格转换成markdown表格，便于阅读。
        '''
        no = "![barrier](https://user-images.githubusercontent.com/15277496/76684847-3c2d4900-65dd-11ea-8d91-c7be623cf3d2.png)|"
        yes = "![emerald](https://user-images.githubusercontent.com/15277496/76684841-320b4a80-65dd-11ea-8206-e766bbbd3b7d.png)|"
        with open("./contents/"+filename+".md", "w", encoding="utf-8") as f:
            strs = []
            header = "|日期|原文|译文|译者|认证|"
            splitter = "|---|---|---|---|---|"
            strs += [header, splitter]

            for _, rec in table.iterrows():
                try:
                    thisstr = "|"
                    thisstr += rec["发布日期"] + "|"
                    thisstr += "[" + rec["原文标题"] + "]("+ rec["原文链接"] + ")|"
                    if rec["译文链接"] != "-":
                        thisstr += "[" + rec["译文标题"] + "]("+ rec["译文链接"] + ")|"
                    else:
                        thisstr += rec["译文标题"] + "|"
                    thisstr += rec["译者"] + "|"
                    thisstr += yes if rec["认证"] else no
                    strs.append("".join(thisstr))
                except TypeError:
                    print(rec)
                    
            strs = [s + "\n" for s in strs]
            f.writelines(strs)
        pass

    data = pd.read_csv("rawtable.csv", encoding='utf-8')
    needUpdateRaw = False
    
    # 把各专栏和分类分别新建表格
    tables = {}
    for cat in cats:
        tables[cat] = pd.DataFrame(columns=["发布日期","原文标题","原文链接","译文标题","译文链接","译者","认证"])
    
    # 把记录添加到对应的表格中
    for i, rec in data.iterrows():
        recCats = rec["cat"].split(":") # if the category amount of an articles is more than 2, then use : to divide 

        if rec["tr_link"] not in ["-","不收录"] and rec["tr_uid"] == "-": # 未填写uid
            rec["tr_uid"] = uidGet(rec["tr_link"])
            print("Auto-filled uid", rec["tr_uid"], "for", rec["tr_link"])
            data.loc[i,"tr_uid"] = rec["tr_uid"]
            needUpdateRaw = True
        
        tr_name = nameGet(rec["tr_uid"])
        emeralded = True if int(rec["emeralded"]) == 1 else False
        
        for thiscat in recCats:
            tables[thiscat].loc[len(tables[thiscat])]= list(data.iloc[i][:-3])+[tr_name, emeralded] # rawtable[:-3]的记录顺序和输出表一致
    
    # 输出 markdown 表格
    for cat in cats:
        print("making", cat)
        toMarkdownTable(tables[cat], cats[cat])
    
    # 如果自动更新了 uid，那么相应地更新 rawtable
    if needUpdateRaw:
        data.to_csv(path_or_buf="rawtable.csv", index=False, encoding='utf-8')

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
        errorTimes = 0
        MAX_ERROR_TIME = 3
        while True:
            try:
                if opr == "pull":
                    pull()
                elif opr == "render":
                    render()
                elif opr == "bbcode":
                    bbcode()
            except Exception as e:
                print("An error occured when tring to", opr, "- total try:", errorTimes + 1)
                print("Error info:", e)
                errorTimes += 1
                if errorTimes == MAX_ERROR_TIME:
                    raise e
            else:
                break

