import requests
from bs4 import BeautifulSoup as bs

url = 'https://www.kista.re.kr/usr/'
req = requests.get(url, verify=False)
# req.encoding = 'utf-8'
# req.encoding = 'euc-kr'
html = req.text

print(html)

# soup = bs(html, 'lxml')
# boardList = soup.select(
#     'div.contentDetail form table.tableBoard > tbody > tr'
# )
#
# print(boardList)