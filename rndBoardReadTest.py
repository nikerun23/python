import requests
from bs4 import BeautifulSoup as bs

csvDict = {'url': 'http://www.nipa.kr/biz/bizNotice.it?menuNo=18&page=1'
            , 'selectTR': 'table.boardList > tbody > tr'
            , 'selectTitle': 'td.title > a'
            , 'selectDate': 'td.date'}

url = csvDict['url']
selectTR = csvDict['selectTR']
selectTitle = csvDict['selectTitle']
selectDate = csvDict['selectDate']

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

