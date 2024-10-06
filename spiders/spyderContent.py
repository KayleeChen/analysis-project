import time
import requests
import csv
import os
from _datetime import datetime

def init():
    if not os.path.exists('articleData.csv'):
        with open('articleData.csv','w',encoding='utf8',newline='') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow([
                'id',
                'likeNum',
                'commentsLen',
                'reposts_count',
                'region',
                'content',
                'contentLen',
                'created_at',
                'type',
                'detailUrl',# followBtnCode>uid + mblogid
                'authorAvatar',
                'authorName',
                'authorDetail',
                'isVip' # v_plus
            ])

def writerRow(row):
        with open('articleData.csv','a',encoding='utf8',newline='') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(row)

def get_json(url,params):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
        'Cookie': '_s_tentry=www.google.com; UOR=www.google.com,open.weibo.com,www.google.com; Apache=3559150907852.8794.1719098909130; SINAGLOBAL=3559150907852.8794.1719098909130; ULV=1719098909132:1:1:1:3559150907852.8794.1719098909130:; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WhBxViFoc_E3.oxQeyezcfN5JpX5KzhUgL.Fo24She0e0.Xe0-2dJLoI7phqgpjT-fLT-D9T-et; SCF=Ag111R57w-us8G1uyjhnyBbEJssIFcS5yM7nIDrWdvxhmK6ePX89sgRrbLgHJ5W1zBHUxhHD_8U1EQ3jPLgD16c.; SUB=_2A25Lflo0DeRhGedH71ES8yfIyDmIHXVo8tP8rDV8PUNbmtB-LXfjkW1NUK1chDaHcL73-oJwG-aWohAZC8UTbAPX; ALF=02_1721874276; XSRF-TOKEN=_dBZovxSTAHxXXoPtecbRvPd; WBPSESS=GQiGXgyZrfS9YID0mLSfyumkbrGlVhrMt9VkwIXFqytFR5qJiT0d8amcEJbxPSAuoVw5-9aapc61L7pMgoDo6XFKKUG-4qe9OTrzqJnP64fwgCBWqvyekhneyQhBBEHzQyrDqFZm0qDhQ4ivVzT62w=='
    }
    response = requests.get(url,headers=headers,params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def parse_json(response,type):
    for article in response:
        id = article['id']
        likeNum = article['attitudes_count']
        commentsLen = article['comments_count']
        reposts_count = article['reposts_count']
        try:
            region = article['region_name'].replace('发布于 ','')
        except:
            region = '无'
        content = article['text_raw']
        contentLen = article.get('textLength', 0)
        created_at = datetime.strptime(article['created_at'],"%a %b %d %H:%M:%S %z %Y").strftime("%Y-%m-%d")
        type = type
        try:
            detailUrl = 'https://weibo.com/' + str(article['user']['id']) +'/'+ str(article['mblogid'])
        except:
            detailUrl = '无'
        authorAvatar = article['user']['avatar_large']
        authorName = article['user']['screen_name']
        authorDetail = 'https://weibo.com' + article['user']['profile_url']
        if  article['user']['v_plus']:
            isVip = article['user']['v_plus']
        else:
            isVip = 0
        writerRow([
                id,
                likeNum,
                commentsLen,
                reposts_count,
                region,
                content,
                contentLen,
                created_at,
                type,
                detailUrl,
                authorAvatar,
                authorName,
                authorDetail,
                isVip
            ])

def start(typeNum=60,pageNum=10):
    articleUrl = 'https://weibo.com/ajax/feed/hottimeline'
    init()
    typeNumCount = 0
    with open('./navData.csv','r',encoding='utf8') as readerFile:
        reader = csv.reader(readerFile)
        next(reader)
        for nav in reader:
            if typeNumCount > typeNum:return
            for page in range(0,pageNum):
                time.sleep(1)
                print('Scraping type: ' + nav[0] + ', page ' + str(page + 1) + 'data')
                params = {
                    'group_id':nav[1],
                    'containerid':nav[2],
                    'max_id':page,
                    'count':10,
                    'extparam':'discover|new_feed'
                }
                response = get_json(articleUrl,params)
                parse_json(response['statuses'],nav[0])
            typeNumCount += 1

if __name__ == '__main__':
    start()