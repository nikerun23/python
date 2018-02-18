import requests
from bs4 import BeautifulSoup as bs
import datetime
import csv

def getCSV():
    csv_reader = csv.DictReader(open('csv/url_list.csv'))
    csvList = []
    for row in csv_reader.reader:
        if row[2] == 'URL': continue
        if row[2] == '': break
        csvDict = {'department': row[1]
            , 'url': row[2]
            , 'selectTR': row[3]
            , 'selectTitle': row[4]
            , 'selectDate': row[5]
            ,'linkUrl': row[6]}
        csvList.append(csvDict)
    print(csvList)
    print('csvList :',len(csvList))
    return csvList

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

def getBoardNo(siteName, tr):
    result = ''
    if '한국연구재단' == siteName:
        titleList = tr.select('a.ntsviewBtn')
        result = titleList[0].get('data-nts_no')
        return result
    else: return result

def printBoard(csvList):
    for csvDict in csvList:
        department = csvDict['department']
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

        for tr in boardList:

            title = ''
            dateStr = ''
            boardNo = ''
            titleList = tr.select(selectTitle)
            title = titleList[0].text
            ##boardNo = titleList[0].get('data-nts_no')
            boardNo = getBoardNo(department,tr)
            dateList = tr.select(selectDate)
            dateStr = dateList[0].text

            if not findTitle(title):
                continue

            if yesterdayCheck(yesterdayList, dateStr):
                print(boardNo, title, dateStr,'\n',linkUrl.format(boardNo=boardNo))

## ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
## ++++++++++++++++++++++++++++++++++++++++++++++++++++++++

yesterdayList = getYesterdayList()
csvList = getCSV()
printBoard(csvList)