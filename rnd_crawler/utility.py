import datetime

def valid_date(date_str):
    """날짜를 검증합니다"""
    print('inString:', date_str)
    if date_str in ('', None):
        print('return CALL')
        return None
    date_str = date_str.strip()
    date_str = date_str.replace(' ', '').replace(',', '-').replace('.', '-').replace('/', '-')
    print('replace:', date_str)
    # 마지막 '-' 삭제
    if date_str[-1] == '-':
        date_str = date_str[:-1]
    # '~'있을시에 앞 날짜만 추출
    if date_str.find('~') != -1:
        date_str = date_str[:date_str.find('~')]
        date_str = date_str.replace('\n', '').replace('\t', '').strip()
    # datetime 객체로 변환
    try:
        date_time_str = datetime.datetime.strptime(date_str, '%Y-%m-%d')
    except Exception:
        print('########## 날짜 양식에 문제가 있습니다 : ', date_str)
        return None
    else:
        result = datetime.date(date_time_str.year, date_time_str.month, date_time_str.day)
    print('outDate:', result)
    print('---------------------')
    print(type(result))
    return result