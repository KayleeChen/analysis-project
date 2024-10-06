import requests
import csv
import numpy as np
import os

def init():
    if not os.path.exists('navData.csv'):
        with open ('navData.csv', 'w', encoding='utf-8',newline='') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow([
                'typeName',
                'gid',
                'containerid'
            ])
def writerRow(row):
    with open('navData.csv', 'a', encoding='utf-8', newline='') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(row)

def get_data(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
        'Cookie': '_s_tentry=www.google.com; UOR=www.google.com,open.weibo.com,www.google.com; Apache=3559150907852.8794.1719098909130; SINAGLOBAL=3559150907852.8794.1719098909130; ULV=1719098909132:1:1:1:3559150907852.8794.1719098909130:; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WhBxViFoc_E3.oxQeyezcfN5JpX5KzhUgL.Fo24She0e0.Xe0-2dJLoI7phqgpjT-fLT-D9T-et; SCF=Ag111R57w-us8G1uyjhnyBbEJssIFcS5yM7nIDrWdvxhmK6ePX89sgRrbLgHJ5W1zBHUxhHD_8U1EQ3jPLgD16c.; SUB=_2A25Lflo0DeRhGedH71ES8yfIyDmIHXVo8tP8rDV8PUNbmtB-LXfjkW1NUK1chDaHcL73-oJwG-aWohAZC8UTbAPX; ALF=02_1721874276; XSRF-TOKEN=_dBZovxSTAHxXXoPtecbRvPd; WBPSESS=GQiGXgyZrfS9YID0mLSfyumkbrGlVhrMt9VkwIXFqytFR5qJiT0d8amcEJbxPSAuoVw5-9aapc61L7pMgoDo6XFKKUG-4qe9OTrzqJnP64fwgCBWqvyekhneyQhBBEHzQyrDqFZm0qDhQ4ivVzT62w=='
    }
    params = {
        'is_new_segment': 1,
        'fetch_hot': 1
    }
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def parse_json(response):
    seen_gids = set()
    navList = np.append(response['groups'][3]['group'],response['groups'][4]['group'])
    for nav in navList:
        gid = nav['gid']
        if gid in seen_gids:
            continue
        seen_gids.add(gid)
        navName = nav['title']
        containerid = nav['containerid']
        writerRow([navName,gid,containerid])

if __name__ == '__main__':
    init()
    url = 'https://weibo.com/ajax/feed/allGroups'
    response = get_data(url)
    if response:
        parse_json(response)
    else:
        print("Failed to fetch data")