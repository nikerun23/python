import requests
from bs4 import BeautifulSoup as bs

url = 'http://www.keri.re.kr/_prog/_board/?code=sub0501&site_dvs_cd=kr&menu_dvs_cd=0501'
selectTR = 'div.board_list table > tbody > tr'
selectTitle = 'td.title a'
selectDate = 'td:nth-of-type(3)'

req = requests.get(url)
req.encoding = 'utf-8'
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

