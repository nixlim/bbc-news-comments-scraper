#!/usr/bin/env python

import sqlite3
import requests
import re
from datetime import date, datetime
#import time
#import subprocess, os, random, sys
#import logging


# Connect to our comments database
conn = sqlite3.connect('brexit.sqlite3')
conn.execute("CREATE TABLE IF NOT EXISTS comment (user TEXT, datetime TEXT, comment TEXT, positive_rating INTEGER, negative_rating INTEGER, scraped INTEGER, article TEXT);")

# Some headers to keep the comments module happy.
request_headers = {

'accept' :           'application/json, text/javascript, */*; q=0.01',
'accept-encoding':   'gzip, deflate, br',
'accept-language':   'en-GB,en-US;q=0.9,en;q=0.8',
'cookie':            'BBC-UID=a51a082c978f09eac18dc4f881d8a5537a4eb7306704a466ca8047a226817c2c0Mozilla/5.0%20(Windows%20NT%206.1%3b%20Win64%3b%20x64)%20AppleWebKit/537.36%20(KHTML%2c%20like%20Gecko)%20Chrome/63.0.3239.132; ckns_orb_fig_cache={%22uk%22:1%2C%22ck%22:1%2C%22ad%22:0%2C%22ap%22:0%2C%22tb%22:0%2C%22mb%22:0%2C%22eu%22:1}; ckns_policy=111; ckns_policy_exp=1550693152125; ckpf_sa_labels_persist={}; s1=173.127.5A8C7F9F0044C3011FB3F42985; optimizelyEndUserId=oeu1519157197281r0.31467333209731074; BGUID=85da781cd76f8da59785cee38191739c839d3efdfe88c39983d50bb43c003618; ckps_onwardJourney=1',
'origin':            'http://www.bbc.co.uk',
'referer':           'http://www.bbc.co.uk/news/uk-politics-39136739',
'user-agent':        'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Mobile Safari/537.36'

}
comments_per_page = 10

articles = {    'UK and EU fail to strike Brexit talks deal' : '42217735',
                'Post-Brexit UK won\'t be like Mad Max, says David Davis' : '43120277',
                'EU referendum: Brexit \'would spark year-long recession\' - Treasury' : '36355564',     # http://www.bbc.co.uk/news/uk-politics-eu-referendum-36355564
                'EU referendum: Immigration target \'impossible\' in EU, Vote Leave says' : '36573220',  # http://www.bbc.co.uk/news/uk-politics-eu-referendum-36573220
                'Nigel Farage: Narrow Remain win may lead to second referendum' : '36306681',            # http://www.bbc.co.uk/news/uk-politics-eu-referendum-36306681
                'Brexit: David Cameron to quit after UK votes to leave EU' : '36615028', #http://www.bbc.co.uk/news/uk-politics-36615028
                'Theresa May: We\'re on course to deliver Brexit despite vote' : '42346898', # http://www.bbc.co.uk/news/uk-politics-42346898
           }

def get_article_comment_count(id):
    url = 'https://ssl.bbc.co.uk/modules/comments/ajax/comments/?siteId=newscommentsmodule&forumId=__CPS__' + str(id) + '&filter=none&sortOrder=Descending&sortBy=Created&mock=0&mockUser=&parentUri=http%3A%2F%2Fwww.bbc.co.uk%2Fnews%2Fuk-politics-39136739&loc=en-GB&preset=responsive&initial_page_size=10&transTags=0';
    request = requests.get(url, headers=request_headers)
    data = request.json()
    print(str(data['summary']['total']) + ' comments associated with this article.')
    return data['summary']['total']

def scrape_article_comments(article, id, page):
    url = 'https://ssl.bbc.co.uk/modules/comments/ajax/comments/?siteId=newscommentsmodule&forumId=__CPS__' + str(id) + '&filter=none&sortOrder=Descending&sortBy=Created&mock=0&mockUser=&parentUri=http%3A%2F%2Fwww.bbc.co.uk%2Fnews%2Fuk-politics-39136739&loc=en-GB&preset=responsive&initial_page_size=10&transTags=0&comments_page=' + str(page)
    print('Fetching from: ' + url)
    request = requests.get(url, headers=request_headers)
    data = request.json()

    # Simple BBC Brexit Comments Scraper Parsing
    p = re.compile(
        r'<a href="#" class="userId\d+">\n\s+(.*?)\s+</a>.*?<span class="cmt-time">(.*?)</span>.*?class="cmt-text">.*?(.*?)</p>.*?<span class="cmt-rating-positive-value cmt-rating-value">\n\s+(\d+)\s+</span>.*?<span class="cmt-rating-negative-value cmt-rating-value">\n\s+(\d+)\s+</span>',
        flags=re.IGNORECASE | re.DOTALL)
    res = p.findall(data['comments'])

    scraped_datetime = datetime.now()

    for comment in res:
        print('======================== comment ===')
        print(comment)
        conn.execute(
            'INSERT INTO `comment` (`user`, `datetime`, `comment`, `positive_rating`, `negative_rating`, `scraped`, `article`) VALUES (?, ?, ?, ?, ?, ?, ?)',
            (comment[0].strip(), comment[1], comment[2].replace('<BR />', "\n").strip(), comment[3], comment[4], scraped_datetime, article))
        conn.commit()


# Iterate and scrape!
for article, id in articles.items():
    page = 0

    number_of_comments = get_article_comment_count(id)
    #print(key, '=>', value)

    while (page * comments_per_page) < number_of_comments:
        print('Scraping page ' + str(page) + ' of comments for article ' + article + ' (ID = ' + id + ')')
        scrape_article_comments(article, id, page)
        page = page + 1

print('Completed...')
