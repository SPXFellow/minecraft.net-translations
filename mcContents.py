import pandas as pd
from urllib import request
from dateutil import parser
import json
import sys, os
from bs4 import BeautifulSoup

if __name__ == "__main__":
    # Used in addSeries()
    patterns = {
        "block of the week": "botw",
        "taking inventory": "ti",
        "around the block": "atb",
        "minecraft snapshot": "version",
        "minecraft java edition": "version",
        "pre-release": "version",
        "release candidate": "version"
    }

    def tagChecked(art):
        '''
            Some tag may be missed in article json, making auto-pulling failed.
            This function asserts that some vital tags exist. 
        '''
        return ("default_tile" in art
                and "publish_date" in art
                and  "primary_category" in art)

    def addSeries(cat, title):
        '''
            For columns by Duncan Geere and new version post.
        '''
        cat = cat.lower()
        title = title.lower()
        for p in patterns:
            if p in title:
                cat += ":"+patterns[p]
                print("[addSeries] ->", cat)
                break
        return cat

    apiurl = 'https://www.minecraft.net/content/minecraft-net/_jcr_content.articles.grid?pageSize=30'
    table_name = "articles.csv"

    print("Pulling raw json file from api", apiurl)
    new_article_list = json.loads(request.urlopen(apiurl).read())['article_grid']

    # Read local table
    prev_data = pd.read_csv(table_name, encoding='utf-8')
    last_titles = [prev_data.loc[x]["title"] for x in range(50)]
    new_article_data = pd.DataFrame(columns=prev_data.columns)

    for art in new_article_list:
        if tagChecked(art):
            title = art["default_tile"]["title"]
            pub = parser.parse(art["publish_date"]).replace(tzinfo=None)
            
            # Ignore existing article
            if title in last_titles:
                continue
            
            print("Adding new article:", title)
            if "linkurl" in art["default_tile"]["image"]:
                link = art["default_tile"]["image"]["linkurl"]
            else:
                link = 'https://www.minecraft.net' + art["article_url"]
            pub = str(pub.year) + "/" + str(pub.month) + "/" + str(pub.day)
            cat = addSeries(art["primary_category"], title)

            # Add new line to dataframe
            new_article_data.loc[len(new_article_data)]=[pub, title, link, cat,'-', '-'] # tr_link, tr_name

    if len(new_article_data) != 0:
        pd.concat([new_article_data,prev_data]).to_csv(path_or_buf=table_name, index=False, encoding='utf-8')
        print("Successfully pulled.")
    else:
        print("Already up-to-date.")


