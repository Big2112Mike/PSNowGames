import requests
import json
import html
from html2json import collect
from bs4 import BeautifulSoup
from bs2json import bs2json
import csv
import ast
import time
import unicodedata
import os

os.system('python app2.py')

# US
url = "https://www.playstation.com/en-us/explore/playstation-now/games/"

payload = {}
headers = {
    'authority': 'www.playstation.com',
    'cache-control': 'max-age=0',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-user': '?1',
    'sec-fetch-dest': 'document',
    'referer': 'https://www.playstation.com/en-us/explore/playstation-now/?smcid=pdc%3Aen-us%3Anetwork-store%3Aprimary%2520nav%3Amsg-services%3Aps-now',
    'accept-language': 'de-DE,de;q=0.9,ja-JP;q=0.8,ja;q=0.7,en-US;q=0.6,en;q=0.5,fr;q=0.4',
    'cookie': 'AKA_A2=A; sat_track=true; check=true; at_check=true; AMCVS_BD260C0F53C9733E0A490D45%40AdobeOrg=1; psvisitM=w; s_ecid=MCMID%7C64190044543703684361397487015065795629; mboxEdgeCluster=35; s_cc=true; AMCV_BD260C0F53C9733E0A490D45%40AdobeOrg=-408604571%7CMCIDTS%7C18418%7CMCMID%7C64190044543703684361397487015065795629%7CMCAAMLH-1591887612%7C6%7CMCAAMB-1591887612%7C6G1ynYcLPuiQxYZrsz_pkqfLG9yMXBpb2zX5dvJdYQJzPXImdj0y%7CMCOPTOUT-1591290017s%7CNONE%7CMCAID%7CNONE%7CMCSYNCSOP%7C411-18425%7CvVersion%7C4.6.0; sbPlatformPrivacyLevel=minimal; s_fid=67827CAEBEBE6BF2-39AB96BCE688D504; ps-utid=pdc%253Aen-us%253Anetwork-store%253Aprimary%252520nav%253Amsg-services%253Aps-now; ps-utparam=smcid; mbox=session#d3ccddd3f0c247bfb8e9626a9cf8762a#1591284744|PC#d3ccddd3f0c247bfb8e9626a9cf8762a.35_0#1654527619; JSESSIONID=node0hnzykseaumpk6w4age3vvus8261095.node0; s_sq=%5B%5BB%5D%5D',
    'connection': 'close'
}
with requests.Session() as response:
    response = requests.request("GET", url, headers=headers, data=payload)
r = response.text.encode('utf8')
response.close()

soup = BeautifulSoup(r, "lxml")
converter = bs2json()
usgames = []
# print(soup.find('li',class_='game-title'))
allgames = []

region = 'US'
for s in soup.findAll('li', class_='game-title'):
    m = s.extract()
    extracter = converter.convert(m)
    gametitle = extracter['li']['text']
    console = 'unknown'
    game = [gametitle, console, region]
    #         print(gametitle)
    usgames.append(game)

with open('psnowgamelist3-1.csv', mode='r', encoding="utf-8") as europe_file:
    csv_reader = csv.reader(europe_file, delimiter=',')
    for row in csv_reader:
        #         print(row)
        included = 0
        for l in usgames:
            #             print(l[0])
            importgame = ''.join(e for e in str(row[0]) if e.isalnum()).upper()
            #             print(importgame)
            usgame = ''.join(f for f in str(l[0]) if f.isalnum()).upper()
            #             print(usgame)
            if importgame == usgame:
                allgames.append([row[0], row[1], 'yes', 'yes'])
                l.append(True)
                print(l)
                included = 1
        if included == 0:
            allgames.append([row[0], row[1], 'yes', 'no'])

# for i in allgames:
#     print(i)
for l in usgames:
    if len(l) == 3:
        allgames.append([l[0], l[1], 'no', 'yes'])

with open('psnowgamelist3-2.csv', mode='w', encoding="utf-8", newline='') as gamelist_file:
    fieldname = ['Game', 'Console', 'Until', 'Europe', 'US']
    gamelist = csv.DictWriter(gamelist_file, fieldnames=fieldname)
    gamelist.writeheader()
    allgames.sort()
    for i in allgames:
        gametitle = unicodedata.normalize("NFKD", i[0])
        if gametitle != " ":
            console = i[1]
            europe = i[2]
            us = i[3]
            gamelist.writerow({'Game': gametitle, 'Console': console, 'Until': 'TBD', 'Europe': europe, 'US': us})
