import requests
import re
import os
from datetime import datetime, timedelta
import time
import csv
from bs4 import BeautifulSoup, Comment

csvlist = 'bpc_authors_v1.csv'
masterCsv = 'bpc_alllinks.csv'
loc = './'

with open(csvlist, 'r', encoding='utf-8-sig') as l:
    l = l.readlines()

adict = {}

for row in l[1:]:
    row = row.split(';')
    row[15] = row[15].strip()
    if row[15]:
        adict[row[0]] = {'name':row[1], 'path':row[15]}

with open(masterCsv, 'w') as fw:
    fw = csv.writer(fw, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    fw.writerow(['authorId', 'authorName', 'authorPath', 'linkId', 'heading', 'blText', 'blHref', 'otherPersonName', 'otherPersonHref', 'workName', 'workHref'])

for i,row in adict.items():
    authorId = i
    if len(str(authorId)) == 1:
        authorId = '00'+str(authorId)
    elif len(str(authorId)) == 2:
        authorId = '0'+str(authorId)
    else:
        authorId = str(authorId)

    authorName = row['name']
    authorPath = row['path']
    folname = authorId+'_'+authorName

    folder = os.path.join(loc, folname)

    if os.path.isdir(folder):
        aPage = authorId + '_page.html'
        with open(folder+'/'+aPage, 'r', encoding='utf-8-sig') as p:
            p = p.read()

        soup = BeautifulSoup(p, 'html.parser')

        allLinksInfo = []
        linkNum = 1

        for i,li in enumerate(soup.find_all('li')):
            if len(str(linkNum)) == 1:
                linkId = authorId+'_000'+str(linkNum)
            elif len(str(linkNum)) == 2:
                linkId = authorId+'_00'+str(linkNum)
            elif len(str(linkNum)) == 3:
                linkId = authorId+'_0'+str(linkNum)
            elif len(str(linkNum)) == 4:
                linkId = authorId+'_'+str(linkNum)

            # заголовок списка
            heading = li.parent.find_previous('b')
            if heading:
                heading = re.search('(?<=<b>).*(?=<\/b>)', str(heading))
                heading = str(heading.group(0))
                heading = heading.strip('-')
                heading = heading.strip()

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

            linkInfo = [linkId, heading, blText, blHref, otherPersonName, otherPersonHref, workName, workHref]
            allLinksInfo.append(linkInfo)

            with open(masterCsv, 'a') as fw:
                fw = csv.writer(fw, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                fw.writerow([authorId, authorName, authorPath, linkId, heading, blText, blHref, otherPersonName, otherPersonHref, workName, workHref])

            linkNum += 1

        csvResult = authorId + '_links.csv'
        with open(folder+'/'+csvResult, 'w') as fw:
            fw = csv.writer(fw, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            fw.writerow(['linkId', 'heading', 'blText', 'blHref', 'otherPersonName', 'otherPersonHref', 'workName', 'workHref'])
            for link in allLinksInfo:
                fw.writerow(link)

        print('Ссылки сохранены в', folder, '/', csvResult)
