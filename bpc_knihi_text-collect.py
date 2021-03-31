import requests
import re
import os
from datetime import datetime, timedelta
import time
import csv
from bs4 import BeautifulSoup, Comment

start = datetime.now()
print('Начало: ', start)

headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Max-Age': '3600',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
    }

csvlist = '205_links.csv'
loc = './'
timer = 1

with open(csvlist, 'r', encoding='utf-8-sig') as l:
    l = l.readlines()

tdict = {}

for row in l[1:5]:
    row = row.split(',')
    if row[2] == 'epub':
        if row[5]:
            if row[1] == 'Пераклады':
                tdict[row[0]]= row[7].strip()
        else:
            tdict[row[0]]= row[7].strip()

for i, url in tdict.items():
    textId = i
    authorId = '205'

    url = 'https://knihi.com/'+url

    req = requests.get(url, headers)
    soup = BeautifulSoup(req.content, 'html.parser')

    main = soup.find_all(lambda tag: tag.name == 'div' and tag.get('class') == ['container'])

    textHtml = textId + '.html'
    with open(textHtml, 'w') as fw:
        fw.write(str(main)[1:-1])
    print(textHtml, 'сохранен')
    time.sleep(timer)

end = datetime.now()
print('Начало: ', end)
elTime = end - start
elTimeMin = round(elTime / timedelta(minutes=1), 2)
elTimeSec = round(elTime / timedelta(seconds=1), 2)

if elTimeMin > 1:
    print('Длительность в минутах: ', elTimeMin)
else:
    print('Длительность в секундах: ', elTimeSec)

print('Перерыв перед запросом: ', timer, 'секунд')
