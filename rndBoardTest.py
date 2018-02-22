import requests
from bs4 import BeautifulSoup as bs

req = requests.get('http://www.kei.re.kr/home/board/notice/list.kei')
# req.encoding = 'utf-8'
html = req.text

print(html)

# soup = bs(html, 'lxml')
# boardList = soup.select(
#     'div.contentDetail form table.tableBoard > tbody > tr'
# )
#
# print(boardList)