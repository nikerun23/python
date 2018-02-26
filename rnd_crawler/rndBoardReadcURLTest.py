import requests
from bs4 import BeautifulSoup as bs

url = 'https://www.nrf.re.kr/tender/list?menu_no=57'
selectTR = 'div.board_list tbody > tr'
selectTitle = 'td a.ntsviewBtn'
selectDate = 'td:nth-of-type(5)'

headers = {
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Referer': 'https://www.nrf.re.kr/index',
    'Connection': 'keep-alive',
}

ss = requests.Session()
ss.headers = headers
res = ss.get(url)
# res = requests.get(url)
# res.encoding = 'utf-8'
# res.encoding = 'euc-kr'
# print(res.text)
soup = bs(res.text, 'lxml')
boardList = soup.select(
    selectTR
)
# print(boardList)
for i in boardList:

    title = ''
    dateStr = ''
    boardNo = ''
    titleList = i.select_one(selectTitle)
    if titleList is not None:
        title = titleList.text
    else:
        title = '<제목 정보를 읽어올 수 없습니다>'
    boardNo = ''
    dateList = i.select_one(selectDate)
    if dateList is not None:
        dateStr = dateList.text
    else:
        dateStr = '<날짜 정보를 읽어올 수 없습니다>'
    print(boardNo, title, dateStr)

