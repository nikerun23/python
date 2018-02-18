import requests
from bs4 import BeautifulSoup as bs
import datetime

def findTitle(title):
    findList = ['연구', '사업']
    result = False
    for t in findList:
        if title.find(t) >= 0:
            return True
    return result


def getYesterdayList():
    yesterday = datetime.date.today() - datetime.timedelta(days=5)
    dayOfWeek = ['월', '화', '수', '목', '금', '토', '일']
    yesterdayList = [yesterday]

    # yesterday가 일요일 경우 전 주 금요일까지 조회
    if '일' == dayOfWeek[yesterday.weekday()]:
        yesterdayList.append(yesterday - datetime.timedelta(days=1))
        yesterdayList.append(yesterday - datetime.timedelta(days=2))

    print('전일 :', yesterday, dayOfWeek[yesterday.weekday()])
    print('크롤링 날짜 :', yesterdayList)
    print('------------------------------------------------------------------------------------------------')
    return yesterdayList

def yesterdayCheck(dayList, boardDay):
    result = False
    dateTimeStr = datetime.datetime.strptime(boardDay, '%Y-%m-%d')
    dateType = datetime.date(dateTimeStr.year, dateTimeStr.month, dateTimeStr.day)
    for yesterday in dayList:
        if yesterday == dateType:
            result = True
    return result




yesterdayList = getYesterdayList()

url = 'https://www.nrf.re.kr/biz/notice/list?menu_no=44'
selectTR = 'div.board_list tbody > tr'
selectTitle = 'a.ntsviewBtn'
selectDate = 'td:nth-of-type(4)'
linkUrl = 'https://www.nrf.re.kr/biz/notice/view?nts_no={boardNo}&menu_no=44&biz_no=&search_type=&search_keyword=&page='

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
    dateList = i.select(selectDate)
    ##print(aList)
    for y in titleList:
        title = y.text
        boardNo = y.get('data-nts_no')

    for z in dateList:
        dateStr = z.text
    if not findTitle(title):
        continue

    if yesterdayCheck(yesterdayList, dateStr):
        print(boardNo, title, dateStr,'\n',linkUrl.format(boardNo=boardNo))
