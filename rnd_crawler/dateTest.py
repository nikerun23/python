import datetime

def validDateStr(dateStr):
    print('inString:',dateStr)
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

dateTemp = [
    '2017-01-01',
    '2017/01/01',
    '2017-01-01',
    '2017,01,01',
    '2017.01.01',
    '2017.01.01.',
    '2017. 01. 01.',
    '2017. 01.01',
    '2017. 1.01.',
    '2017.1.1',
    '',
    None
    ]

for dt in dateTemp:
    dateTime = validDateStr(dt)

