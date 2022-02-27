###### Unused code ######

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

def trash():
    '''
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
    '''
    pass
