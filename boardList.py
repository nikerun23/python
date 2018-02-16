import requests
from bs4 import BeautifulSoup as bs
import datetime

def getYesterdayList():
    yesterday = datetime.date.today() - datetime.timedelta(days=1)
    dayOfWeek = ['월', '화', '수', '목', '금', '토', '일']
    yesterdayList = [yesterday]

    # yesterday가 일요일일 경우 전 주 금요일까지 조회
    if '일' == dayOfWeek[yesterday.weekday()]:
        yesterdayList.append(yesterday - datetime.timedelta(days=1))
        yesterdayList.append(yesterday - datetime.timedelta(days=2))

    print(yesterday, dayOfWeek[yesterday.weekday()])
    print(yesterdayList)
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
selectStr = 'div.board_list tbody > tr'
req = requests.get(url)
html = req.text
soup = bs(html, 'lxml')
boardList = soup.select(
    selectStr
)

for i in boardList:
    title = ''
    dateStr = ''
    titleList = i.select('a.ntsviewBtn')
    dateList = i.select('td:nth-of-type(4)')
    for y in titleList:
        title = y.text
    for z in dateList:
        dateStr = z.text

    if yesterdayCheck(yesterdayList, dateStr):
        print(title, dateStr)
