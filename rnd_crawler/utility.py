import datetime
import csv
from selenium import  webdriver

def valid_date(date_str):
    """날짜 양식을 검증합니다"""
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
        print('########## 날짜 양식에 문제가 있습니다 :', date_str)
        return None
    else:
        result = datetime.date(date_time_str.year, date_time_str.month, date_time_str.day)
    print('outDate:', result)
    print('---------------------')
    print(type(result))
    return result


def valid_title(title_str):
    """ 글제목을 검증합니다 """
    if title_str is None:
        return ''
    title_str = title_str.strip()
    title_str = title_str.replace('  ', '').replace('\t', '').replace('\n', '')
    return title_str


def get_yesterday_list():
    """ 전일 날짜를 구합니다 """
    yesterday = datetime.date.today() - datetime.timedelta(days=1)
    day_of_week = ['월', '화', '수', '목', '금', '토', '일']
    yesterday_list = [yesterday]

    # yesterday가 일요일 경우 전 주 금요일까지 조회
    if '일' == day_of_week[yesterday.weekday()]:
        yesterday_list.append(yesterday - datetime.timedelta(days=1))
        yesterday_list.append(yesterday - datetime.timedelta(days=2))

    print('전일 :', yesterday, day_of_week[yesterday.weekday()])
    print('크롤링 날짜 :', yesterday_list)
    print('-----------------------------------------------------------------------------------')
    return yesterday_list


def yesterday_check(day_list, board_date):
    """ 글의 등록일을 이전일과 비교합니다 """
    if board_date is None:
        return False
    result = False
    for yesterday in day_list:
        if yesterday == board_date:
            result = True
    return result


def csv_read_url(src):
    """ csv파일을 읽습니다 """
    url_dict_list = []
    try:
        csv_reader = csv.DictReader(open(src, encoding='UTF8'))
    except FileNotFoundError:
        print('########## 파일을 찾을 수 없습니다 :', src)
    else:
        url_field_names = csv_reader.fieldnames
        for row in csv_reader.reader:
            url_dict = {}
            if 'X' == row[7]:  # Crawler
                continue
            for ii, h in enumerate(url_field_names):
                url_dict[h] = row[ii].strip()
            url_dict_list.append(url_dict)
    return url_dict_list

def selenium_read_board(csv_info):
    driver = webdriver.Chrome('./chromedriver')
    driver.get(csv_info.url)
    driver.find_element_by_css_selector(csv_info.click_css).click()

    html = driver.page_source
    driver.quit()
    return html

