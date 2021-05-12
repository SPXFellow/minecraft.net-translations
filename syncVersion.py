import pandas as pd
from urllib import request
from dateutil import parser
from bs4 import BeautifulSoup
import json, sys, os, re


def parseTitle(title):
    snapshot = "[1-2][0-9]w[0-9][0-9][a-z]"
    pre = "(1\.[1-9][0-9]*\.[0-9]+)-pre([0-9]+)"
    rc = "(1\.[1-9][0-9]*\.[0-9]+)-rc([0-9]+)"
    release = "1\.[1-9][0-9]*\.[0-9]+"
    
    res = re.search(snapshot, title)
    if res:
        return res.group(0)
    
    res = re.search(pre, title)
    if res:
        rel = res.group(1) # 1.2.3
        ind = res.group(2) # pre4
        return rel + " Release Candidate " + ind
    
    res = re.search(rc, title)
    if res:
        rel = res.group(1) # 1.2.3
        ind = res.group(2) # rc4
        return rel + " Pre-Release " + ind
    
    res = re.search(release, title)
    if res:
        return res.group(0)
    
    return title

if __name__ == "__main__":
    table_name = "articles.csv"
    url = "https://www.mcbbs.net/forum.php?mod=forumdisplay&fid=139&filter=typeid&typeid=204"
    site = "https://www.mcbbs.net/thread-{}-1-1.html"
    
    # load page
    soup = BeautifulSoup(request.urlopen(url).read(),"html.parser")
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

    # load and update table
    table = pd.read_csv(table_name, encoding='utf-8')
    newsind = 0
    for i in range(50):
        entry = table.loc[i]
        if "version" in entry["cat"].split(":") and entry["tr_link"] == "-":
            for newsitem in newslist[newsind:]:
                if newsitem[0] in entry["title"]:
                    entry["tr_link"] = newsitem[1]
                    entry["tr_name"] = newsitem[2]
                    newsind += 1
                    break
                
        if newsind == len(newslist):
            break

    table.to_csv(path_or_buf=table_name, index=False, encoding='utf-8')
