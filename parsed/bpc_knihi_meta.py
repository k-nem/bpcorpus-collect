import re
import os
import csv
from bs4 import BeautifulSoup, Comment
from datetime import datetime, timedelta
import time

loc = './'
metafile = 'meta.csv'
dirlist = []

print(datetime.now())

for parent, dirs, files in os.walk('.'):
    for dir in dirs:
        adir = re.search('\d{1,3}_', dir)
        if adir:
            dirlist.append(dir)

dirlist = sorted(dirlist)

head = []
mdict = []

for dir in dirlist:
    folder = loc + dir
    if os.path.isdir(folder):
        for parent, dirs, files in os.walk(folder):
            for file in sorted(files):
                if file.endswith('html') and 'page' not in file:
                    with open(folder+'/'+file, 'r', encoding='utf-8-sig') as l:
                        l = l.read()
                        metadict = {}
                        metadict['linkId'] = file.split('.')[0]
                        soup = BeautifulSoup(l, 'html.parser')
                        meta = re.findall('(?<=<!-- HEADER_FIELD ).+(?= -->)', str(soup))

                        if meta:
                            metadict['hasMeta'] = True
                        else:
                            metadict['hasMeta'] = False

                        for m in meta:
                            metadict[m.split(':',1)[0]] = m.split(':',1)[1].lstrip()

                        mdict.append(metadict)
                        ks = list(metadict.keys())
                        for k in ks:
                            if k not in head:
                                head.append(k)

res = []

for m in mdict:
    fullmeta = {}
    for h in head:
        if h in m.keys():
            fullmeta[h] = m[h]
        else:
            fullmeta[h] = ''
    res.append(fullmeta)

with open(metafile, 'w') as fw:
    fw = csv.writer(fw, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    fw.writerow(head)

for i in res:
    with open(metafile, 'a') as fw:
        fw = csv.writer(fw, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        fw.writerow(i.values())

print(len(res), 'строк записано в', metafile)
print(datetime.now())
