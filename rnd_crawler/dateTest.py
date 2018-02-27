import datetime

def validDateStr(date_str):
    print('inString:', date_str)
    if date_str in ('', None):
        print('return CALL')
        return None
    date_str = date_str.strip()
    date_str = date_str.replace(' ', '').replace(',', '-').replace('.', '-').replace('/', '-')
    print('replace:',date_str)
    # 마지막 '-' 삭제
    if date_str[-1] == '-':
        date_str = date_str[:-1]
    # '~'있을시에 앞 날짜만 추출
    if date_str.find('~') != -1:
        date_str = date_str[:date_str.find('~')]
        date_str = date_str.replace('\n', '').replace('\t', '').strip()
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
    '2017-1-1 ~ 2017-2-2',
    '2018.02.20~2018.03.19',
    '''2018-02-20 ~ 2018-02-27
                
                / 오늘 마감''',
    '''2017-12-07
       ~
       2018-12-31''',
    '',
    None
    ]

for dt in dateTemp:
    date_time = validDateStr(dt)

