import googlesearch
import requests
from re import search,sub

reSubdivx = '(?i)(?<=.com/)\w{12}.+(?=\.html)'
reLink = 'http[s]?://www\.subdivx\.com/bajar\.php\?id=\d+(?:&u=\d+)?'

with open('lista.txt','r') as l:
    listaVids = [vid.strip() for vid in l.readlines()]

for vid in listaVids:
    vid = sub('(?i)\.(?:avi|mov|mkv|mp4|wmv)$','',vid)
    print(vid)
    s = googlesearch.search('subdivx {}'.format(vid))
    c = 0
    for resultado in s:
        if c == 5:
            print('No se encontraron subs para {}'.format(vid))
            break
        if search(reSubdivx, resultado):
            subPag = requests.get(resultado)
            try: subLink = search(reLink,subPag.text).group()
            except:
                c+=1 
                continue

            data = requests.get(subLink).content
            if data[:3] == b'Rar':
                ext = '.rar'
            elif data[:2] == b'PK':
                ext = '.zip'
            fileName = sub('\s','',vid.lower())+ext
            with open(fileName,'wb') as d:
                d.write(data)
                break
        else: c+=1
    else: print('No se encontraron subs para {}'.format(vid))