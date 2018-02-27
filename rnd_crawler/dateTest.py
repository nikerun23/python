import datetime

def validDateStr(date_str):
    date_str = date_str.strip()
    print('inString:', date_str)
    if date_str in ('', None):
        print('return CALL')
        return None
    date_str = date_str.replace(' ', '').replace(',', '-').replace('.', '-').replace('/', '-')

    if date_str[-1] == '-':
        date_str = date_str[:-1]

    # datetime 객체로 변환
    date_time_str = datetime.datetime.strptime(date_str, '%Y-%m-%d')
    result = datetime.date(date_time_str.year, date_time_str.month, date_time_str.day)
    print('outDate:', result)
    print('---------------------')
    return result

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
    date_time = validDateStr(dt)

