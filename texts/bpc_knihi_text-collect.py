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

loc = './'
timer = 1
dirlist = []

for parent, dirs, files in os.walk('.'):
    for dir in dirs:
        adir = re.search('\d{1,3}_', dir)
        if adir:
            dirlist.append(dir)

dirlist = sorted(dirlist)

for dir in dirlist:
    authorId = dir.split('_')[0]

    alist = authorId + '_links.csv'
    loc = './'
    folder = loc + dir

    if os.path.isdir(folder):

        with open(folder+'/'+alist, 'r', encoding='utf-8-sig') as l:
            l = l.readlines()

        tdict = {}

        for row in l[1:]:
            row = row.split(',')
            if row[2] == 'epub':
                if row[5]:
                    if row[1] == 'Пераклады':
                        tdict[row[0]]= row[7].strip()
                else:
                    tdict[row[0]]= row[7].strip()

        for i, url in tdict.items():
            textId = i

            textUrl = 'https://knihi.com/'+url

            req = requests.get(textUrl, headers)
            soup = BeautifulSoup(req.content, 'html.parser')

            main = soup.find_all(lambda tag: tag.name == 'div' and tag.get('class') == ['container'])

            textHtml = textId + '.html'
            with open(folder+'/'+textHtml, 'w') as fw:
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
