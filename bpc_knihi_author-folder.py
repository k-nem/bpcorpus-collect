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

csvlist = 'bpc_authors_v1.csv'
loc = './'

with open(csvlist, 'r', encoding='utf-8-sig') as l:
    l = l.readlines()

adict = {}

for row in l[1:]:
    row = row.split(';')
    row[15] = row[15].strip() # исправить в самой таблице
    if row[15]:
        adict[row[0]] = {'name':row[1], 'path':row[15]}

linksinfo = []
timer = 1

for i,row in adict.items():
    authorId = i
    if len(str(authorId)) == 1:
        authorId = '00'+str(authorId)
    elif len(str(authorId)) == 2:
        authorId = '0'+str(authorId)
    else:
        authorId = str(authorId)

    name = row['name']
    path = row['path']
    url = 'https://knihi.com/'+path
    folname = authorId+'_'+name

    req = requests.get(url, headers)
    soup = BeautifulSoup(req.content, 'html.parser')

    result = soup.prettify()
    main = soup.find_all(lambda tag: tag.name == 'div' and tag.get('class') == ['container'])

    folder = os.path.join(loc, folname)
    print(folder)
    if not os.path.isdir(folder):
        os.makedirs(folder)

    aPage = authorId + '_page.html'
    with open(folder+'/'+aPage, 'w') as fw:
        fw.write(str(main)[1:-1])

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
