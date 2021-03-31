import os

count = 0
l = []
for parent, dirnames, filenames in os.walk('.'):
    for dir in dirnames:
        for file in os.listdir(dir+'/'):
            if file.endswith('html'):
                with open(dir+'/'+file, 'r') as f:
                    f = f.read()
                if '<b>- Пераклады -</b>' in f:
                    l.append(dir)
                    count += 1
l.sort()
with open('translators.txt', 'a') as w:
    for i in l:
        w.write(i+'\n')
    w.write('Всего: '+str(count))
