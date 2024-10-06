import requests
import csv
import os
import time
import random
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime

def init():
    if not os.path.exists('commentsData.csv'):
        with open('commentsData.csv', 'w', encoding='utf8', newline='') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow([
                'articleId',
                'created_at',
                'like_counts',
                'region',
                'content',
                'authorName',
                'authorGender',
                'authorAddress',
                'authorAvatar'
            ])

def writerRow(row):
    with open('commentsData.csv', 'a', encoding='utf8', newline='') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(row)

def get_html(url, id):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
        'Cookie': '_s_tentry=www.google.com; UOR=www.google.com,open.weibo.com,www.google.com; Apache=3559150907852.8794.1719098909130; SINAGLOBAL=3559150907852.8794.1719098909130; ULV=1719098909132:1:1:1:3559150907852.8794.1719098909130:; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WhBxViFoc_E3.oxQeyezcfN5JpX5KzhUgL.Fo24She0e0.Xe0-2dJLoI7phqgpjT-fLT-D9T-et; SCF=Ag111R57w-us8G1uyjhnyBbEJssIFcS5yM7nIDrWdvxhmK6ePX89sgRrbLgHJ5W1zBHUxhHD_8U1EQ3jPLgD16c.; SUB=_2A25Lflo0DeRhGedH71ES8yfIyDmIHXVo8tP8rDV8PUNbmtB-LXfjkW1NUK1chDaHcL73-oJwG-aWohAZC8UTbAPX; ALF=02_1721874276; XSRF-TOKEN=_dBZovxSTAHxXXoPtecbRvPd; WBPSESS=GQiGXgyZrfS9YID0mLSfyumkbrGlVhrMt9VkwIXFqytFR5qJiT0d8amcEJbxPSAuoVw5-9aapc61L7pMgoDo6XFKKUG-4qe9OTrzqJnP64fwgCBWqvyekhneyQhBBEHzQyrDqFZm0qDhQ4ivVzT62w=='
    }
    params = {
        'is_show_bulletin': 2,
        'id': id
    }
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def parse_json(response, articleId):
    if response:
        commentList = response.get('data', [])
        for comment in commentList:
            created_at = datetime.strptime(comment['created_at'], "%a %b %d %H:%M:%S %z %Y").strftime("%Y-%m-%d")
            like_counts = comment['like_counts']
            authorName = comment['user']['screen_name']
            authorGender = comment['user']['gender']
            authorAddress = comment['user']['location'].split(' ')[0]
            authorAvatar = comment['user']['avatar_large']
            try:
                region = comment['source'].replace('来自', '')
            except:
                region = '无'
            content = comment['text_raw']
            writerRow([
                articleId,
                created_at,
                like_counts,
                region,
                content,
                authorName,
                authorGender,
                authorAddress,
                authorAvatar,
            ])

def fetch_comments(article):
    url = 'https://weibo.com/ajax/statuses/buildComments'
    articleId = article[0]
    print(f'Scraping article {articleId}')
    time.sleep(random.uniform(1, 2))  # Add random sleep to prevent triggering anti-scraping mechanisms
    response = get_html(url, articleId)
    parse_json(response, articleId)

def start():
    init()
    with open('./articleData.csv', 'r', encoding='utf8') as readerFile:
        reader = csv.reader(readerFile)
        next(reader)
        articles = [article for article in reader]

    with ThreadPoolExecutor(max_workers=16) as executor:
        futures = [executor.submit(fetch_comments, article) for article in articles]
        for future in as_completed(futures):
            future.result()

if __name__ == '__main__':
    start()
