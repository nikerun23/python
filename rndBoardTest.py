import requests
from bs4 import BeautifulSoup as bs

req = requests.get('http://www.nipa.kr/biz/bizNotice.it?menuNo=18&page=1')
html = req.text

print(html)

soup = bs(html, 'lxml')
boardList = soup.select(
    'table tbody > tr'
)

print(boardList)