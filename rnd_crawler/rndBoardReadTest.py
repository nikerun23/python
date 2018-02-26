import requests
from bs4 import BeautifulSoup as bs

url = 'http://dsmi.re.kr/notice01?bc_seq=1'
selectTR = 'table.board-list > tbody > tr'
selectTitle = 'td.tdleft a'
selectDate = 'td:nth-of-type(4)'

req = requests.get(url)
# req.encoding = 'utf-8'
# req.encoding = 'euc-kr'
html = req.text
# print(html)
soup = bs(html, 'lxml')
boardList = soup.select(
    selectTR
)
# print(boardList)
for i in boardList:

    title = ''
    dateStr = ''
    boardNo = ''
    titleList = i.select(selectTitle)
    title = titleList[0].text
    boardNo = ''
    dateList = i.select(selectDate)
    dateStr = dateList[0].text

    print(boardNo, title, dateStr)

