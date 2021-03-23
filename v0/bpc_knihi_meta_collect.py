import requests
import re
import os
from datetime import datetime
from bs4 import BeautifulSoup, Comment

print('Начало: ', datetime.now())

headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Max-Age': '3600',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
    }

csvlist = 'bpc_authors_v1.csv'
loc = './'

with open(csvlist) as l:
    l = l.readlines()

adict = {}

for row in l:
    row = row.split(';')
    row[15] = row[15].strip()
    if row[15]:
        adict[row[0]] = {'name':row[1], 'path':row[15]}

allurls = []

for i,row in adict.items():
    id = i
    name = row['name']
    path = row['path']
    url = 'https://knihi.com/'+path
    folder = id + '_' + name

    req = requests.get(url, headers)
    soup = BeautifulSoup(req.content, 'html.parser')

    result = soup.prettify()
    main = soup.find_all(lambda tag: tag.name == 'div' and tag.get('class') == ['container'])
    hrefs = re.findall('(?<=href=\")[^\"]*(?=\")', str(main))

    links = [i for i in hrefs]
    htmls = []

    for i in links:
        if i.endswith('.html') and i.startswith('/'+path):
            htmls.append(i)
            allurls.append('https://knihi.com'+i)

with open('bpc_knihi_urllist.csv', 'w') as fw:
    for l in allurls:
        fw.write(str(l)+'\n')

print('Собраны ссылки: ', datetime.now())
allmeta = []

for i, u in enumerate(allurls):
    req2 = requests.get(u, headers)
    soup2 = BeautifulSoup(req2.content, 'html.parser')
    main2 = soup2.find_all(lambda tag: tag.name == 'div' and tag.get('class') == ['container'])
    meta = re.findall('(?<=<!-- HEADER_FIELD ).+(?= -->)', str(main2))

    if '<!-- BOOK_BEGIN -->' in str(main2):
        meta.append('AvailableText: True')
    else:
        meta.append('AvailableText: False')

    metadict = {}
    for m in meta:
        metadict[m.split(':',1)[0]] = m.split(':',1)[1].lstrip()

    metadict['textUrl'] = u
    metadict['textId'] = i
    allmeta.append(metadict)

with open('bpc_knihi_worklist.txt', 'w') as fw:
    fw.write(str(allmeta))

print('Собраны метаданные: ', datetime.now())
