import os
import csv

loc  = './'
dlist = []

for parent, dirs, files in os.walk('.'):
    for dir in dirs:
        dlist.append(dir)

dlist = sorted(dlist)
badfiles = []

for dir in dlist:
    folder = loc + dir
    if os.path.isdir(folder):
        for parent, dirs, files in os.walk(folder):
            for file in files:
                if file.endswith('html'):
                    if 'page' not in file:
                        with open(folder+'/'+file, 'r', encoding='utf-8-sig') as l:
                            l = l.read()

                        if 'Запатрабаваная старонка ня знойдзеная на нашым сайце.' in l:
                            badfiles.append(file)

badfiles = sorted(badfiles)
print(len(badfiles))

flist = []

for file in badfiles:
    for dir in dlist:
        if file.split('_')[0] == dir.split('_')[0]:
            flist.append([file.split('.')[0], dir])

ldict = {}
with open('bpc_alllinks.csv', newline='') as f:
    reader = csv.reader(f)
    allLinksInfo = list(reader)

with open('errors.csv', 'w') as fw:
    fw = csv.writer(fw, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    fw.writerow(['linkId', 'dir', 'workHref'])


for f in flist:
    for link in allLinksInfo:
        if link[3] == f[0]:
            f.append(link[10])
            with open('errors.csv', 'a') as fw:
                fw = csv.writer(fw, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                fw.writerow(f)
