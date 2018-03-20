import datetime
import csv
from selenium import webdriver
import time
import requests
from bs4 import BeautifulSoup as bs

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
        if date_str.find(':') > -1:  # HH:MM 포함되어 있을 경우 제거
            date_str = date_str[:10]
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


def valid_a_href(url, href):
    domain_name = url[:url.find('.kr') + 3].replace(' ', '')
    href = href.replace(' ', '').replace('&amp;', '&')
    result = domain_name + href
    return result


def get_board_content(url, csv_info):
    select_list = [
        csv_info['content_Title'],
        csv_info['content_WriteDate'],
        csv_info['content_StartDate'],
        csv_info['content_EndDate'],
        csv_info['content_Body'],
        csv_info['content_Files']
    ]
    req = requests.get(url)
    soup = bs(req.text, 'lxml')

    # print(req.text)
    result_list = []
    try:
        for index,s in enumerate(select_list):
            if 'NoDate' != s and '' != s:
                if 4 == index:  # csv_info['content_Body']
                    html = soup.select_one(s).contents
                elif index in (1, 2, 3):  # Date
                    html = valid_date(soup.select_one(s).text, None).strftime('%Y-%m-%d')
                else:
                    html = soup.select_one(s).text
            else:
                html = 'NoDate'
            result_list.append(html)
    except Exception as e:
        print(e)
        print('########## get_board_content 예외발생 !!')

    # print(result_list)
    content = {'title': valid_title(result_list[0]),
               'url': url,
               'dept_cd': csv_info['부처'],
               'wc_company_name': csv_info['기관'],
               'write_date': valid_date(result_list[1],'').strftime('%Y-%m-%d'),
               'start_date': result_list[2],
               'end_date': result_list[3],
               'body': result_list[4],
               'files': result_list[5]}

    # print(content)
    return content


def get_headless(csv_info):
    # 크롬 옵션 추가하기
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # 헤드리스모드
    options.add_argument('--disable-gpu')  # 호환성용 (필요없는 경우도 있음)
    options.add_argument('--window-size=1920x1080')  # (가상)화면 크기 조절
    # 크롬 모바일 버전으로 User Agent 설정하기
    options.add_argument("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36")
    # 크롬 Options를 넣어준 Headless 모드 크롬
    driver = webdriver.Chrome('./chromedriver', chrome_options=options)
    # 구글에서 'my user agent' 검색 하기
    driver.get('https://www.google.com/search?q=my+user+agent')
    # User Agent 결과값 가져오기
    # User Agent 가 잘못 설정되면 .xpdopen 요소를 셀렉트 할 수 없다.
    my_user_agent = driver.find_element_by_css_selector('.xpdopen').text
    print(my_user_agent)
    # 브라우저 및 드라이버 종료
    driver.quit()


def write_board_selenium(content):
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome('./chromedriver', chrome_options=options)

    driver.get('http://www.ntis.go.kr/ThMain.do')
    driver.find_element_by_name('userid').send_keys('hoon1234')
    driver.find_element_by_name('password').send_keys('gate4fkd!!')
    driver.find_element_by_name('password').submit()

    driver.get('http://www.ntis.go.kr/rndgate/eg/un/ra/createForm.do')
    time.sleep(3)

    dept_cd = content['dept_cd']  # 부처명
    wc_company_name = content['wc_company_name']  # 공고기관명
    wc_title = content['title']
    wc_url = content['url']
    wc_dt = content['write_date']
    ro_strt_dt = content['start_date']
    ro_end_dt = content['end_date']
    body = content['body']

    driver.find_element_by_css_selector('#roFormCd > option[value="28802"]').click()  # 공고형태
    el = driver.find_element_by_name('deptCd')
    for option in el.find_elements_by_tag_name('option'):
        if dept_cd == option.text:
            option.click()  # select() in earlier versions of webdriver
            break
    driver.find_element_by_name('wcCompanyName').send_keys(wc_company_name)
    driver.find_element_by_name('wcTitle').send_keys(wc_title)
    driver.find_element_by_name('wcUrl').send_keys(wc_url)
    driver.execute_script('document.getElementsByName("wcDt")[0].removeAttribute("readonly")')
    driver.find_element_by_name('wcDt').send_keys(wc_dt)
    driver.execute_script('document.getElementsByName("roStrtDt")[0].removeAttribute("readonly")')
    driver.find_element_by_name('roStrtDt').send_keys(ro_strt_dt)
    driver.execute_script('document.getElementsByName("roEndDt")[0].removeAttribute("readonly")')
    driver.find_element_by_name('roEndDt').send_keys(ro_end_dt)
    time.sleep(2)
    driver.execute_script('document.getElementById("#smart_editor2_content")')
    driver.find_element_by_css_selector('#smart_editor2_content body').send_keys(body)
    driver.find_element_by_css_selector('#smart_editor2_content body').send_keys(body)
# document.getElementById('smart_editor2_content')

