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
    titleList = i.select_one(selectTitle)
    title = titleList.text
    boardNo = ''
    dateList = i.select_one(selectDate)
    dateStr = dateList.text

    print(boardNo, title, dateStr)

