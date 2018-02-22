import requests
from bs4 import BeautifulSoup as bs

url = 'http://www.kei.re.kr/home/board/bidding/list.kei'
selectTR = 'table#dataList > tbody > tr'
selectTitle = 'td.tl a'
selectDate = 'td:nth-of-type(3)'

req = requests.get(url)
# req.encoding = 'utf-8'
# req.encoding = 'euc-kr'
html = req.text

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

