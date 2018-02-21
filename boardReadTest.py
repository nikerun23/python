import requests
from bs4 import BeautifulSoup as bs

csvDict = {'url': 'http://www.mof.go.kr/article/list.do?boardKey=9&currentPageNo=1&menuKey=375&recordCountPerPage=10&searchEtc1=&searchEtc2=&searchEtc3=&searchEtc4=&searchEtc5=&searchDeptName=&searchStartDate=&searchEndDate=&searchSelect=title&searchValue='
            , 'selectTR': 'div.board_body > table.board_list > tbody > tr'
            , 'selectTitle': 'td.tx_al > a'
            , 'selectDate': 'td:nth-of-type(5)'
            ,'linkUrl': 'http://www.mof.go.kr/article/view.do?articleKey=18821&searchSelect=title&boardKey=9&menuKey={boardNo}&currentPageNo=1'}

url = csvDict['url']
selectTR = csvDict['selectTR']
selectTitle = csvDict['selectTitle']
selectDate = csvDict['selectDate']
linkUrl = csvDict['linkUrl']

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

    print(boardNo, title, dateStr,'\n',linkUrl.format(boardNo=boardNo))
