import requests
from bs4 import BeautifulSoup as bs

req = requests.get('http://www.kfi.or.kr/home/brd/brd230/brd230_Type4_Lis.do?board_seq=14')
# req.encoding = 'utf-8'
html = req.text

print(html)

# soup = bs(html, 'lxml')
# boardList = soup.select(
#     'div.contentDetail form table.tableBoard > tbody > tr'
# )
#
# print(boardList)