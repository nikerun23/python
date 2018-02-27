import requests
from bs4 import BeautifulSoup as bs
import csv
import datetime

# +++++++++++ Util Area start +++++++++++++++++++++++++++++++++
def getYesterdayList():
    yesterday = datetime.date.today() - datetime.timedelta(days=1)
    dayOfWeek = ['월', '화', '수', '목', '금', '토', '일']
    yesterdayList = [yesterday]

    # yesterday가 일요일 경우 전 주 금요일까지 조회
    if '일' == dayOfWeek[yesterday.weekday()]:
        yesterdayList.append(yesterday - datetime.timedelta(days=1))
        yesterdayList.append(yesterday - datetime.timedelta(days=2))

    print('전일 :', yesterday, dayOfWeek[yesterday.weekday()])
    print('크롤링 날짜 :', yesterdayList)
    print('-----------------------------------------------------------------------------------')
    return yesterdayList

def yesterdayCheck(dayList, boardDate):
    if boardDate is None:
        return False
    result = False
    for yesterday in dayList:
        if yesterday == boardDate:
            result = True
    return result

def validDate(dateStr):
    """날짜를 검증합니다"""
    dateStr = dateStr.strip()
    if dateStr in ('', None):
        return None
    dateStr = dateStr.replace(' ', '').replace(',', '-').replace('.', '-').replace('/', '-')

    if dateStr[-1] == '-':
        dateStr = dateStr[:-1]

    # datetime 객체로 변환
    dateTimeStr = datetime.datetime.strptime(dateStr, '%Y-%m-%d')
    dateType = datetime.date(dateTimeStr.year, dateTimeStr.month, dateTimeStr.day)

    return dateType

def validTitle(titleStr):
    """글제목을 검증합니다"""
    titleStr = titleStr.strip()
    titleStr = titleStr.replace('  ', '').replace('\t', '').replace('\n', '')
    return titleStr

def csvReadUrl(src):

    csv_reader = csv.DictReader(open(src, encoding='UTF8'))
    urlFieldNames = csv_reader.fieldnames
    urlDictList = []

    for row in csv_reader.reader:
        urlDict = {}
        if 'X' == row[7]:  # Crawler
            continue
        for index, h in enumerate(urlFieldNames):
            urlDict[h] = row[index].strip()
        urlDictList.append(urlDict)
    return urlDictList


# +++++++++++ Util Area end +++++++++++++++++++++++++++++++++
rowNum = 10 - 2 # index 값 보정
urlDictList = csvReadUrl('csv/url_list.csv')
print(urlDictList[rowNum])
yesterdayList = getYesterdayList()

def printRnD(csvInfo):
    print(csvInfo['부처'],'---',csvInfo['기관'],'---------------------------------------')
    print(csvInfo['URL'])
    url = csvInfo['URL']
    selectTR = csvInfo['TR']
    selectTitle = csvInfo['Title']
    selectDate = csvInfo['Date']
    etcStr = csvInfo['etc']

    req = requests.get(url)
    if 'utf-8' == etcStr:
        req.encoding = 'utf-8'
    elif 'euc-kr' == etcStr:
        req.encoding = 'euc-kr'

    html = req.text
    # print(html)
    soup = bs(html, 'lxml')
    boardList = soup.select(
        selectTR
    )
    # print(boardList)
    for i in boardList:
        title = ''
        boardNo = ''
        titleList = i.select_one(selectTitle)
        title = validTitle(titleList.text)
        boardNo = ''
        dateList = i.select_one(selectDate)
        boardDate = validDate(dateList.text) # datetime객체로 반환
        # 전일 공고만 출력
        if yesterdayCheck(yesterdayList, boardDate):
            print(boardNo, title, boardDate)
    print('-----------------------------------------------------------------------')

for index, info in enumerate(urlDictList):
    print('csv Row Num :',index + 2)
    printRnD(info)

# printRnD(urlDictList[rowNum])
print('++++++++++++++++++++++ 조회 완료 ++++++++++++++++++++++')

# for csvInfo in urlDictList:
#     printRnD(csvInfo)