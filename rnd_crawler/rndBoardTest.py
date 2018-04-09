import requests
from bs4 import BeautifulSoup as bs

url = 'https://www.kofac.re.kr/?page_id=1673&uid=9618&mod=document'
req = requests.get(url)
# req = requests.get(url, verify=False)
# req.encoding = 'utf-8'
# req.encoding = 'euc-kr'
html = req.text

# print(html)

soup = bs(html, 'lxml')
boardList = soup.select(
    '#kboard-default-document div.content-view table:nth-of-type(2) tr a'
)

print(boardList)