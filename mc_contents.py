from hashlib import new
import pandas as pd
import requests
from dateutil import parser
import json
import sys, os

def tagChecked(art):
    '''
        Some important tags may be missed in json, making auto-pulling failed.
        This function asserts that these tags exist. 
    '''
    return ("default_tile" in art
            and "publish_date" in art
            and  "primary_category" in art)

def attach_column(cat, title):
    '''
        Auto-labeling articles.
    '''
    patterns = {
        "block of the week": "botw",
        "block of the month": "botw",
        "taking inventory": "ti",
        "around the block": "atb",
        "minecraft snapshot": "version",
        "minecraft java edition": "version",
        "minecraft: java edition": "version",
        "pre-release": "version",
        "release candidate": "version",
        "minecraft beta": "be",
        "build challenge": "bc"
    }
    cat = cat.lower()
    title = title.lower()
    for p in patterns:
        if p in title:
            cat += ":"+patterns[p]
            #print("[attach_column]", title, "->", cat)
            return cat
    # special pattern for be
    if "1." in title and "bedrock" in title:
        return cat + ":be"
    # default
    return cat

def parse_entry(art):
    '''
        The format of an entry:
            {
                "default_tile": {
                    "title": "New on Java Realms Keepin Up With The Pillagers",
                    ... something we don't care
                },
                "primary_category": "News",
                "article_url": "/en-us/article/new-java-realms-keepin-up-with-the-pillagers",
                "publish_date": "30 August 2021 09:24:19 UTC",
                ... something we don't care
            }
        
        If you want more information, please check the raw json.
    '''
    # Article title.
    title = art["default_tile"]["title"]
    # Primary category. Some article may contain more than 1 category, but we don't care.
    cat = attach_column(art["primary_category"], title)
    # Link of the article.
    if "linkurl" in art["default_tile"]["image"]: 
        # if linkurl exists, then this article is from education.minecraft.com, which we don't care.
        link = 'edu' 
    else:
        link = 'https://www.minecraft.net' + art["article_url"]
    # Publish date
    pub = parser.parse(art["publish_date"]).replace(tzinfo=None)
    pub = str(pub.year) + "/" + str(pub.month) + "/" + str(pub.day)
    return pub, title, link, cat

def pull_article_list():
    '''
        Read raw json from Minecraft.net, and return article list.
        {
            "article_grid": [
                {
                "default_tile": {
                ...        
    '''
    args = sys.argv
    if len(args) == 1:
        print("API url is required!")
        exit()
    elif len(args) == 2 :
        apiurl = args[1]
        if args[1] == 'local':
            # Read from local file
            localjson = './_jcr_content.articles.json'
            print("Reading json file", localjson)
            with open(localjson, 'r', encoding='utf-8') as f:
                raw_json = json.load(f)
        else:
            # Read from url 
            if apiurl == 'api':
                apiurl = "https://www.minecraft.net/content/minecraft-net/_jcr_content.articles.grid?pageSize=100"
            headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'}
            print("Pulling raw json file from api", apiurl)
            try:
                req = requests.get(url = apiurl, headers=headers)
                raw_json = req.json()
            except Exception as e:
                print("Request Failed:", e)
                exit(1)
            
    return raw_json['article_grid']

def before_deadline(pub):
    '''
        Reject articles published before 2021.
        We used to reject articles under NEWS catagory, so if they pop up, we still reject them.
    '''
    return parser.parse(pub).year < 2021

if __name__ == "__main__":
    # Used in attach_column()  
    new_article_list = pull_article_list()

    # Read local table
    table_name = "articles.csv"
    prev_data = pd.read_csv(table_name, encoding='utf-8')
    prev_latest_titles = [prev_data.loc[x]["title"] for x in range(len(prev_data))]

    new_article_data = pd.DataFrame(columns=prev_data.columns)

    for entry in new_article_list:
        if tagChecked(entry):
            pub, title, link, cat = parse_entry(entry)
            if title in prev_latest_titles or title == 'edu' or before_deadline(pub) or title == "Minecraft":
                continue
            print("Adding new article:", title)
            new_article_data.loc[len(new_article_data)]=[pub, title, link, cat,'-', '-'] # tr_link, tr_name

    if len(new_article_data) != 0:
        pd.concat([new_article_data,prev_data]).to_csv(path_or_buf=table_name, index=False, encoding='utf-8')
        print("Successfully pulled.")
    else:
        print("Already up-to-date.")

    #tmp func
    # for i in range(200):
    #     try:
    #         entry = prev_data.loc[i]
    #         cat, title = entry["cat"], entry["title"]
    #         if ":" not in cat:
    #             new_cat = attach_column(cat, title)
    #             if new_cat != cat:
    #                 prev_data.loc[i]["cat"] = new_cat
    #                 print(title,"cat:", cat, "->", new_cat)
    #     except:
    #         print(i)
    #     pd.concat([new_article_data,prev_data]).to_csv(path_or_buf=table_name, index=False, encoding='utf-8')




