import pandas as pd
from urllib import request
from dateutil import parser
import json
import sys, os
from bs4 import BeautifulSoup
from pandas.core import api

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

    # Read raw json
    args = sys.argv
    if len(args) == 1 or (len(args) == 2 and args[1] == 'api'):
        apiurl = os.environ['DLL_API']
        headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'}
        print("Pulling raw json file from api", apiurl)
        req = request.Request(url = apiurl, headers=headers)
        new_article_list = json.loads(request.urlopen(req).read())['article_grid']
        
    else:
        localjson = './_jcr_content.articles.json'
        print("Reading json file", localjson)
        with open(localjson, 'r', encoding='utf-8') as f:
            new_article_list = json.load(f)['article_grid']

    # Read local table
    table_name = "articles.csv"
    prev_data = pd.read_csv(table_name, encoding='utf-8')
    last_titles = [prev_data.loc[x]["title"] for x in range(150)]
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


