import requests
from bs4 import BeautifulSoup as bs
import csv
import datetime

# +++++++++++ Util Area start +++++++++++++++++++++++++++++++++
def validDateStr(dateStr):
    """날짜를 검증합니다"""
    print('inString:', dateStr)
    if dateStr in ('', None):
        print('return CALL')
        return None
    dateStr = dateStr.replace(' ', '').replace(',', '-').replace('.', '-').replace('/', '-')

    if dateStr[-1] == '-':
        dateStr = dateStr[:-1]

    # datetime 객체로 변환
    dateTimeStr = datetime.datetime.strptime(dateStr, '%Y-%m-%d')
    dateType = datetime.date(dateTimeStr.year, dateTimeStr.month, dateTimeStr.day)
    print('outDate:', dateType)
    print('---------------------')
    return dateType

def csvReadUrl(src):

    csv_reader = csv.DictReader(open(src, encoding='UTF8'))
    urlFieldNames = csv_reader.fieldnames
    urlDictList = []

    for row in csv_reader.reader:
        urlDict = {}
        for index, h in enumerate(urlFieldNames):
            urlDict[h] = row[index]

        urlDictList.append(urlDict)
    return urlDictList


# +++++++++++ Util Area end +++++++++++++++++++++++++++++++++

urlDictList = csvReadUrl('csv/url_list.csv')

def printRnD(csvInfo):
    print(csvInfo)

    url = csvInfo['URL']
    selectTR = csvInfo['TR']
    selectTitle = csvInfo['Title']
    selectDate = csvInfo['Date']

    req = requests.get(url)
    # req.encoding = 'utf-8'
    # req.encoding = 'euc-kr'
    html = req.text
    # print(html)
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

printRnD(urlDictList[5])

# for csvInfo in urlDictList:
#     printRnD(csvInfo)