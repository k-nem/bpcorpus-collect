import requests
import re
import os
from datetime import datetime, timedelta
import time
import csv
from bs4 import BeautifulSoup, Comment
import bpc_knihi_author_url_collect as makecsv

csvlist = 'bpc_authors_v1.csv'
apage = '0_author_page.html'
csvResult = '0_links.csv'
loc = './'

with open(csvlist, 'r', encoding='utf-8-sig') as l:
    l = l.readlines()

adict = {}

for row in l[1:]:
    row = row.split(';')
    row[15] = row[15].strip()
    if row[15]:
        adict[row[0]] = {'name':row[1], 'path':row[15]}


for i,row in adict.items():
    id = i
    name = row['name']
    folname = id+'_'+name

    folder = os.path.join(loc, folname)

    if os.path.isdir(folder):
        with open(folder+'/'+apage, 'r', encoding='utf-8-sig') as p:
            p = p.read()

        soup = BeautifulSoup(p, 'html.parser')

        allLinksInfo = []
        linkNum = 1

        for i,li in enumerate(soup.find_all('li')):
            linkId = linkNum
            res = str(li)

            # текст в скобках
            blank = re.search('(?<=>)\s*\(.*\)(?=\s*<)', res)
            if blank:

                blank = str(blank.group(0))
                hasBlank = True
                blText = re.search('(?<=>).*(?=</a>\))', blank)
                if blText:
                    blText = blText.group(0)
                else:
                    continue
                blHref = re.search('(?<=href=\")[^\"]*(?=\")', blank)
                if blHref:
                    blHref = blHref.group(0)
                else:
                    continue
            else:
                hasBlank = False

            # основные ссылки
            if hasBlank == True:
                mcode = res.replace(blank,'')

                # ссылки на других людей (перевод, биография)
                dots = re.search('<a.*/a>.', mcode)
                if dots:
                    dots = dots.group(0)
                    otherPersonName = re.search('(?<=>)[^>]*(?=</a>)', dots).group(0)
                    otherPersonHref = re.search('(?<=href=\")[^\"]*(?=\")', dots).group(0)

                    work = mcode.replace(dots,'')
                    workName = re.search('(?<=>)[^>]*(?=</a>)', work).group(0)
                    workHref = re.search('(?<=href=\")[^\"]*(?=\")', work).group(0)

                else:
                    wlinks = re.findall('<a.*/a>', mcode)
                    wlinks = wlinks[0] # берем только первую ссылку после скобок
                    workName = re.search('(?<=>)[^>]*(?=</a>)', wlinks).group(0)
                    workHref = re.search('(?<=href=\")[^\"]*(?=\")', wlinks).group(0)
                    otherPersonName = ''
                    otherPersonHref = ''

            linkInfo = [linkId, blText, blHref, otherPersonName, otherPersonHref, workName, workHref]
            allLinksInfo.append(linkInfo)

            linkNum += 1


        with open(folder+'/'+csvResult, 'w') as fw:
            fw = csv.writer(fw, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            fw.writerow(['linkId', 'blText', 'blHref', 'otherPersonName', 'otherPersonHref', 'workName', 'workHref'])
            for link in allLinksInfo:
                fw.writerow(link)

        print('Ссылки сохранены в', folder, '/', csvResult)
