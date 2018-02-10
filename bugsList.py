import requests
from bs4 import BeautifulSoup as bs

req = requests.get('https://music.bugs.co.kr/chart')
req.encoding = 'utf-8'
html = req.text

soup = bs(html, 'lxml')
bugsList = soup.select(
    'table.trackList > tbody > tr > th > p.title > a'
)

rank = 1
for i in bugsList :
    print('순위',rank, '제목:',i.text)
    rank += 1
