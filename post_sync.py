import pandas as pd
from urllib import request
from bs4 import BeautifulSoup

url = "https://www.mcbbs.net/thread-823054-1-1.html"
page = BeautifulSoup(request.urlopen(url).read(),"html.parser")
spoilers = page.find_all("div", class_ = "spoilerbody")
sync_list = {}

# Pull table from mcbbs
for spoiler in spoilers:
    tablelist = spoiler.find_all("tr")
    for entry in tablelist:
        if entry.contents[0].text == "日期": continue
        src = entry.contents[1]
        tl = entry.contents[2]
        tlr = entry.contents[3]
        if tlr.text != "-":
            sync_list[src.a.attrs["href"].split("/")[-1]] = (tl.a.attrs["href"], tlr.text)

# Sync
table_name = "articles.csv"
table = pd.read_csv(table_name, encoding='utf-8')
for i in range(len(table)):
    entry = table.loc[i]
    link = entry["link"].split("/")[-1]
    tr_link = entry["tr_link"]
    if link in sync_list and tr_link == "-":
        entry["tr_link"] = sync_list[link][0]
        entry["tr_name"] = sync_list[link][1]
        print("Sync", entry["title"], "by", entry["tr_name"])

table.to_csv(path_or_buf=table_name, index=False, encoding='utf-8')

