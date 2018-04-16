import requests
from bs4 import BeautifulSoup as bs

url = 'http://www.ksafety.kr/community/announce_view.asp?page=1&no=11&bbs=tb_board'
req = requests.get(url)
# req = requests.get(url, verify=False)
# req.encoding = 'utf-8'
# req.encoding = 'euc-kr'
html = req.text

print(html)

# soup = bs(html, 'lxml')
# boardList = soup.select(
#     '#kboard-default-document div.content-view table:nth-of-type(2) tr a'
# )
#
# print(boardList)