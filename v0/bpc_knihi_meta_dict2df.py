import pandas as pd
import re
import ast

urlfile = 'bpc_knihi_urllist.csv'
metafile = 'bpc_knihi_worklist.txt'

with open(urlfile, 'r') as ou:
  ou = ou.readlines()

urls = [url.strip() for url in ou]
#print('Ссылок в списке: ', len(urls))

with open(metafile, 'r') as om:
  om = om.read()

dm = ast.literal_eval(om)
for i, d in enumerate(dm):
    d['URL'] = urls[i]
    d['id'] = i

col = list(set(val for dic in dm for val in dic.keys()))
#for c in col:
#    print(c)

df = pd.DataFrame(dm,columns=col)
df.drop(['texturl'], axis=1)
df.to_csv('metadf.csv')
