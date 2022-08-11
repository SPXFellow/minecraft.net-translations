import pandas as pd
from urllib import request
from dateutil import parser
from bs4 import BeautifulSoup
import json, sys, os, re

uid2name = {
    "-": "-",
    "0": "MCBBS"
}
site = "https://www.mcbbs.net/thread-{}-1-1.html"

###### Utils ######

def parseJavaTitle(title):
    '''
        Parse title in mcbbs to title in Minecraft.
        Specifically, return the corresponding minecraft post title of the original mcbbs post title
    '''
    snapshot = "[1-2][0-9]w[0-9][0-9][a-z]"
    pre = "(1\.[1-9][0-9]*(\.[0-9]+)?)-pre([0-9]+)"
    rc = "(1\.[1-9][0-9]*(\.[0-9]+)?)-rc([0-9]+)"
    release = "Java版 (1\.[1-9][0-9]*\.[0-9]+)"
    
    res = re.search(snapshot, title)
    if res:
        return res.group(0)
    
    res = re.search(pre, title)
    if res:
        rel = res.group(1) # 1.2.3
        ind = res.group(3) # pre4
        return rel + " Pre-Release " + ind
    
    res = re.search(rc, title)
    if res:
        rel = res.group(1) # 1.2.3
        ind = res.group(3) # rc4
        return rel + " Release Candidate " + ind
    
    res = re.search(release, title)
    if res:
        rel = res.group(1) # 1.2.3
        return "Java Edition " + res.group(1)
    
    return title

def parseBETitle(title):
    beta = "Beta (1\.[1-9][0-9]*\.[0-9]+\.[0-9]+)"
    preview = "(1\.[1-9][0-9]*\.[0-9]+\.[0-9]+/[0-9]+)"
    preview2 = "Beta & Preview (1\.[1-9][0-9]*\.[0-9]+\.[0-9]+)"
    release = "基岩版 (1\.[1-9][0-9]*\.[0-9]+)" # not sure yet

    res = re.search(beta, title)
    if res:
        return res.group(0)

    res = re.search(preview, title)
    if res:
        return res.group(0)

    res = re.search(preview2, title)
    if res:
        return res.group(0)

    res = re.search(release, title)
    if res:
        return res.group(1) # 1.2.3

    return title

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
        #print("Welcome new translator:", usrName)
        #with open(uidPath, "w", encoding="utf-8") as f:
        #    json.dump(uid2name, f, ensure_ascii=False, indent=4)
    return uid2name[uid]

###### sync functions ######

def make_newslist(url, parser):
    soup = BeautifulSoup(request.urlopen(url).read(),"html.parser")
    newslist = []
    for t in soup.find_all("tbody"):
        tr = t.tr
        xst = tr.th.find("a", class_="xst")
        by = tr.find("td", class_="by")
        if xst:
            version = parser(xst.text)
            link = site.format(t.attrs["id"][13:])
            name = by.cite.a.text if by.cite.a else "匿名"
            item = (version, link, name)
            if item not in newslist:
                newslist.append(item)
    return newslist

def sync_version():
    '''
        Sync Minecraft version posts
    '''
    # There are about 28 threads per page, so don't leave the table too long. (> 6 months)
    java_url = 'https://www.mcbbs.net/forum.php?mod=forumdisplay&fid=139&filter=typeid&typeid=204'
    be_url = 'https://www.mcbbs.net/forum.php?mod=forumdisplay&fid=139&filter=typeid&typeid=2400'
    je_news_list = make_newslist(java_url, parseJavaTitle)
    be_news_list = make_newslist(be_url, parseBETitle)
    return je_news_list, be_news_list

###### Merge synced information ######

if __name__ == "__main__":
    table_name = "articles.csv"
    table = pd.read_csv(table_name, encoding='utf-8')
    
    # load news
    je, be = sync_version()

    # update version posts
    newsind = 0
    for i in range(200):
        entry = table.loc[i]
        if type(entry["cat"]) is str and ("version" in entry["cat"].split(":") or "be" in entry["cat"].split(":")) and entry["tr_link"] == "-":
            if "version" in entry["cat"].split(":"):
                newslist = je
            else:
                newslist = be
            for newsitem in newslist:
                if newsitem[0] in entry["title"]:
                    entry["tr_link"] = newsitem[1]
                    entry["tr_name"] = newsitem[2]
                    newsind += 1
                    print(newsitem[0] ,"is synced.")
                    break
                
        if newsind == len(je) + len(be):
            break

    # save table
    table.to_csv(path_or_buf=table_name, index=False, encoding='utf-8')

