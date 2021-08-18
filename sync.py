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

def parseTitle(title):
    snapshot = "[1-2][0-9]w[0-9][0-9][a-z]"
    pre = "(1\.[1-9][0-9]*(\.[0-9]+)?)-pre([0-9]+)"
    rc = "(1\.[1-9][0-9]*(\.[0-9]+)?)-rc([0-9]+)"
    release = "1\.[1-9][0-9]*\.[0-9]+"
    
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
        return res.group(0)
    
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

def sync_version():
    '''
        Sync Minecraft version posts
    '''
    # There are about 28 threads per page, so don't leave the table too long. (> 6 months)
    news_url = "https://www.mcbbs.net/forum.php?mod=forumdisplay&fid=139&filter=typeid&typeid=204"
    
    soup = BeautifulSoup(request.urlopen(news_url).read(),"html.parser")
    newslist = []
    for t in soup.find_all("tbody"):
        tr = t.tr
        xst = tr.th.find("a", class_="xst")
        by = tr.find("td", class_="by")
        if xst:
            version = parseTitle(xst.text)
            link = site.format(t.attrs["id"][13:])
            name = by.cite.a.text if by.cite.a else "匿名"
            item = (version, link, name)
            if item not in newslist:
                newslist.append(item)
    return newslist

def sync_emerald():
    '''
        Sync Minecraft.net posts
    '''
    trs_url = 'https://www.mcbbs.net/forum.php?mod=forumdisplay&fid=1015&orderby=dateline&typeid=2390&orderby=dateline&typeid=2390&filter=author&page='
    greens = {}
    failed = []
    check_pages = 2
    for page in range(1, check_pages + 1):
        print("=====================\n  dealing page", page)
        # load page
        link = trs_url + str(page)
        soup = BeautifulSoup(request.urlopen(link).read(),"html.parser")
        t = soup.find('table', id = "threadlisttableid")

        # iterate thread list
        for tbody in t.find_all('tbody'):
            # skip separate line
            if not tbody.attrs or "separatorline" in tbody["id"]:
                continue

            # find author's uid
            uid = tbody.find('td', class_= "by").a["href"].split('&')[-1][4:]

            # find tid
            a = tbody.find('a', class_ = "xst")
            tid = a.attrs["href"].split('&')[1][4:]

            # open thread
            thread_url = site.format(tid)
            thsoup = BeautifulSoup(request.urlopen(thread_url).read(),"html.parser")

            # see if it's emeralded
            green = False
            ratl = thsoup.find('table', class_='ratl') 
            if ratl:
                for rate in ratl.find_all('th', class_='xw1'):
                    if "宝石" in rate.text:
                        green = True
                        break
            
            # find source article (SPX format required)
            srcget = False
            for atag in thsoup.find_all('a'):
                if '发布的' in atag.text:
                    srcget = True
                    srcart = atag["href"].split('/')[-1]
                    break

            # pack up info
            info = {"uid": uid, "tid": tid}
            print("uid",uid,"// tid", tid, "// green", green, "//", a.text)
            if not ratl: 
                print(tid, "is not yet rated")
                continue
            
            # record threads state
            if green:
                if srcget:
                    print(tid, "is emeralded for", srcart)
                    greens[srcart] = info
                else:
                    print(tid, "is emeralded but not using SPX format")
                    failed.append(info)
            else:
                print(tid, "is rated, but not emeralded")

    return greens, failed

###### Merge synced information ######

if __name__ == "__main__":
    table_name = "articles.csv"
    table = pd.read_csv(table_name, encoding='utf-8')
    
    # load news
    newslist = sync_version()

    # update version posts
    newsind = 0
    for i in range(50):
        entry = table.loc[i]
        if "version" in entry["cat"].split(":") and entry["tr_link"] == "-":
            for newsitem in newslist[newsind:]:
                if newsitem[0] in entry["title"]:
                    entry["tr_link"] = newsitem[1]
                    entry["tr_name"] = newsitem[2]
                    newsind += 1
                    print(newsitem[0] ,"is synced.")
                    break
                
        if newsind == len(newslist):
            break

    # load minecraft.net translations
    greens, failed = sync_emerald()

    # update emeralded translations
    for i in range(len(table)):
        if table.loc[i, "tr_link"] != '-':
            continue
        link = table.loc[i, "link"].split('/')[-1]
        if link in greens:
            trlink = site.format(greens[link]["tid"])
            trname = nameGet(greens[link]["uid"])
            table.iloc[i]["tr_link"] = trlink
            table.iloc[i]["tr_name"] = trname
            print("Add", greens[link]["tid"], "for", link)

    # add failed posts to faillog
    fail_log = "failed.txt"
    with open(fail_log, "w") as f:
        for item in failed:
            f.write(item["tid"]+"\n")
    print("\nThere are", len(fail_log), " threads that failed to process. See tids in", fail_log)

    # save table
    table.to_csv(path_or_buf=table_name, index=False, encoding='utf-8')
