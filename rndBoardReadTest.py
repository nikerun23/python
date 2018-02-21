import requests
from bs4 import BeautifulSoup as bs

url = 'https://www.kofac.re.kr/?page_id=1672'
selectTR = 'div.kboard-list table.list > tbody > tr'
selectTitle = 'td.kboard-list-title a'
selectDate = 'td.kboard-list-date'

req = requests.get(url)
html = req.text
soup = bs(html, 'lxml')
boardList = soup.select(
    selectTR
)

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

