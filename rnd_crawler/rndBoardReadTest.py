import requests
from bs4 import BeautifulSoup as bs

url = 'https://plus.auri.go.kr/post/support-business'
selectTR = 'table.list > tbody > tr'
selectTitle = 'td.subject a'
selectDate = 'td:nth-of-type(5)'

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

