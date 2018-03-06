import datetime
import csv
from selenium import webdriver
import time

def valid_date(date_str, date_fm):
    """ 날짜를 검증합니다 """
    if date_str in ('', None):
        return None
    if date_fm in ('DD/nYY.MM', '|YYYY-MM-DD'):  # 불규칙한 날짜를 보완 (과학기술정보통신부, 국가수리과학연구소)
        date_str = modify_date(date_str, date_fm)
    else:
        date_str = date_str.strip()
        date_str = date_str.replace(' ', '').replace(',', '-').replace('.', '-').replace('/', '-')
        # 마지막 '-' 삭제
        if date_str[-1] == '-':
            date_str = date_str[:-1]
        # '~'있을시에 앞 날짜만 추출
        if date_str.find('~') > -1:
            date_str = date_str[:date_str.find('~')]
            date_str = date_str.replace('\n', '').replace('\t', '').strip()
    # datetime 객체로 변환
    try:
        date_time_str = datetime.datetime.strptime(date_str, '%Y-%m-%d')
    except Exception:
        print('########## 날짜 양식에 문제가 있습니다 :\n', date_str)
        result = None
    else:
        result = datetime.date(date_time_str.year, date_time_str.month, date_time_str.day)
    finally:
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
    finally:
        return url_dict_list


def selenium_read_board(csv_info):
    """" Selenium을 이용하여 (str)Html 반환 """
    try:
        options = webdriver.ChromeOptions()
        options.add_argument("--disable-extensions")
        options.add_argument("--start-maximized")
        driver = webdriver.Chrome('./chromedriver', chrome_options=options)

        driver.get(csv_info['URL'])
        time.sleep(5)

        click_css_list = csv_info['ClickCSS'].split(',')
        for css in click_css_list:
            driver.find_element_by_css_selector(css).click()
            time.sleep(5)
        html = driver.page_source
    except Exception:
        print('########## Selenium 작동이 중지 되었습니다')
        html = ''
    finally:
        driver.quit()
        return html


def modify_date(date_str, date_fm):
    """" 부처별 불규칙한 날짜를 보완하여 (str)Date 반환 """
    result = ''
    try:
        # 과학기술정보통신부
        if ('DD/nYY.MM' == date_fm):
            index = 0
            if (date_str.find('작성일') > -1):  # 작성일 엾을경우 대비
                index = 1
            date_str = date_str.split('\n')  # ['작성일 : ', '        26', '        18.02', '        ']
            print('date_str split : ',date_str)
            dd = date_str[index].strip()
            mm = date_str[index+1].strip()[3:]
            yy = date_str[index+1].strip()[:2]
            yyyy = datetime.date.today().strftime('%Y')[:2] + yy
            result = yyyy + '-' + mm + '-' + dd
        # 국가수리과학연구소
        elif ('|YYYY-MM-DD' == date_fm):
            date_str = date_str.replace('\n', '').replace('\t', '').strip()
            date_str = date_str.split(' ')  # ['경영관리팀', '|', '2018-02-26']
            # print('date_str split : ',date_str)
            result = date_str[-1]
        else:
            result = ''

    except Exception:
        print('########## 날짜 수정에 실패 하였습니다 :', result)
        result = ''
    # print('result :', result)
    finally:
        return result

