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
        "minecraft preview": "be",
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
    pub = '-'
    return pub, title, link, cat

def pull_article_list(latest_title: str) -> list:
    '''
        Read raw json from Minecraft.net, and return article list.
        {
            "article_grid": [
                {
                "default_tile": {
                ...        
    '''
    apiurl = "https://www.minecraft.net/content/minecraftnet/language-masters/en-us/_jcr_content.articles.page-{}.json"
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'}
    
    print("Pulling raw json file from api", apiurl)
    new_article_list = []
    for page in range(1, 100):
        current_url = apiurl.format(page)
        try:
            response = requests.get(current_url, headers=headers, timeout=5)
            response.raise_for_status()
            
            data = response.json()
            curr_list = data['article_grid']
            for article in curr_list:
                if article['default_tile']['title'] == latest_title:
                    print(f"✅ Page {page} saved and job done.")
                    return new_article_list
                else:
                    new_article_list.append(article)
                        
            print(f"✅ Page {page} saved.")

        except Exception as e:
            print(f"❌ Failed to save page {page}: {e}")
            exit()

    # Reverse the list since it's appeneded in reverse order.
    return new_article_list[::-1]


if __name__ == "__main__":
    # Check local latest title
    table_name = "articles.csv"
    prev_data = pd.read_csv(table_name, encoding='utf-8')
    prev_latest_titles = [prev_data.loc[x]["title"] for x in range(len(prev_data))]

    # Used in attach_column()  
    new_article_list = pull_article_list(prev_latest_titles[0])

    new_article_data = pd.DataFrame(columns=prev_data.columns)

    for entry in new_article_list:
        if tagChecked(entry):
            pub, title, link, cat = parse_entry(entry)
            if title == 'edu' or title == "Minecraft":
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




