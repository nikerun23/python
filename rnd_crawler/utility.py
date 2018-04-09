import datetime
import csv
from selenium import webdriver
import time
import re
import requests
from bs4 import BeautifulSoup as bs, Comment
import telegram
from multiprocessing import Pool

global except_list
except_list = []


# """ 날짜를 검증합니다 """
def valid_date(date_str, date_fm):
    if date_str in ('', None):
        return None
    if date_fm in ('DD/nYY.MM', '|YYYY-MM-DD', '작성일YYYY-MM-DD'):  # 불규칙한 날짜를 보완 (과학기술정보통신부, 국가수리과학연구소)
        date_str = modify_date(date_str, date_fm)
    else:
        date_str = date_str.strip()
        date_str = date_str.replace(' ', '').replace(',', '-').replace('.', '-').replace('/', '-')
        # 마지막 '-' 삭제
        if date_str[-1] == '-':
            date_str = date_str[:-1]
        # '~'있을시에 앞 날짜만 추출
        if '~' in date_str:
            date_str = date_str[:date_str.find('~')]
            date_str = date_str.replace('\n', '').replace('\t', '').strip()
        if ':' in date_str:  # HH:MM 포함되어 있을 경우 제거
            date_str = date_str[:10]
    # datetime 객체로 변환
    try:
        date_time_str = datetime.datetime.strptime(date_str, '%Y-%m-%d')
    except Exception:
        print('########## 날짜 양식에 문제가 있습니다 :\n', date_str)
        except_list.append({date_str: '########## 날짜 양식에 문제가 있습니다'})
        result = None
    else:
        result = datetime.date(date_time_str.year, date_time_str.month, date_time_str.day)
    finally:
        return result


# """ 글제목을 검증합니다 """
def valid_title(title_str):
    if title_str is None:
        return ''
    title_str = title_str.replace('새글', '').replace('New', '')\
        .replace('[진행중]', '').replace('[입찰안내]', '').replace('[공고]', '').replace('[용역]', '')\
        .replace('[입찰]', '')
    title_str = title_str.strip()
    title_str = title_str.replace('  ', '').replace('\t', '').replace('\n', '')
    return title_str


# """ 전일 날짜를 구합니다 """
def get_yesterday_list():
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


# """ 글의 등록일을 이전일과 비교합니다 """
def yesterday_check(day_list, board_date):
    if board_date is None:
        return False
    result = False
    for yesterday in day_list:
        if yesterday == board_date:
            result = True
    return result


# """ csv파일을 읽습니다 """
def csv_read_url(src):
    url_dict_list = []
    try:
        csv_reader = csv.DictReader(open(src, encoding='UTF8'))
    except FileNotFoundError:
        print('########## 파일을 찾을 수 없습니다 :', src)
    else:
        url_field_names = csv_reader.fieldnames
        for row in csv_reader.reader:
            url_dict = {}
            for ii, h in enumerate(url_field_names):
                url_dict[h] = row[ii].strip()
            url_dict_list.append(url_dict)
    finally:
        return url_dict_list


# """" Selenium을 이용하여 (str)Html 반환 """
def selenium_read_board(csv_info):
    try:
        options = webdriver.ChromeOptions()
        options.add_argument("--disable-extensions")
        options.add_argument("--start-maximized")
        driver = webdriver.Chrome('./chromedriver', chrome_options=options)

        driver.get(csv_info['URL'])
        time.sleep(5)
        click_css_list = {}
        if ',' in csv_info['ClickCSS']:
            click_css_list = csv_info['ClickCSS'].split(',')
        for css in click_css_list:
            driver.find_element_by_css_selector(css).click()
            time.sleep(5)
        html = driver.page_source
    except Exception:
        print('########## Selenium 작동이 중지 되었습니다')
        except_list.append({csv_info['기관']: '########## Selenium 작동이 중지 되었습니다'})
        html = ''
    finally:
        driver.quit()
        return html


# """" 부처별 불규칙한 날짜를 보완하여 (str)Date 반환 """
def modify_date(date_str, date_fm):
    result = ''
    try:
        # 과학기술정보통신부
        if 'DD/nYY.MM' == date_fm:
            date_str = date_str.replace('\n','').replace(' ','')
            dd = date_str[-7:-5].strip()
            mm = date_str[-2:].strip()
            yy = date_str[-5:-3].strip()
            yyyy = datetime.date.today().strftime('%Y')[:2] + yy
            result = yyyy + '-' + mm + '-' + dd
        # 국가수리과학연구소
        elif '|YYYY-MM-DD' == date_fm:
            date_str = date_str.replace('\n', '').replace('\t', '').strip()
            date_str = date_str.split(' ')  # ['경영관리팀', '|', '2018-02-26']
            # print('date_str split : ',date_str)
            result = date_str[-1]
        # 한국항공우주연구원
        elif '작성일YYYY-MM-DD' == date_fm:
            result = date_str.replace(' ', '').replace('\t', '').strip()[3:]
        else:
            result = ''

    except Exception:
        print('########## 날짜 수정에 실패 하였습니다 :', result)
        except_list.append({result: '########## 날짜 수정에 실패 하였습니다'})
        result = ''
    # print('result :', result)
    finally:
        return result


def valid_a_href(url, href):
    domain_name = url[:url.find('.kr') + 3].replace(' ', '')
    href = href.replace(' ', '').replace('&amp;', '&')
    result = domain_name + href
    return result


# """" 공고 게시판 내용을 가져옵니다 Dict 타입으로 반환 """
def get_board_content(content_url, csv_info):
    select_list = [
        csv_info['content_Title'],
        csv_info['content_WriteDate'],
        csv_info['content_StartDate'],
        csv_info['content_EndDate'],
        csv_info['content_Body'],
        csv_info['content_Files']
    ]
    if 'verify=False' == csv_info['etc_2']:
        req = requests.get(content_url, verify=False)
    else:
        req = requests.get(content_url)
    # etc_1 열
    if 'utf-8' == csv_info['etc_1']:
        req.encoding = 'utf-8'
    elif 'euc-kr' == csv_info['etc_1']:
        req.encoding = 'euc-kr'
    html = req.text

    soup = bs(html, 'lxml')

    # print(req.text)
    result_list = []
    for index,s in enumerate(select_list):
        try:
            if '' != s and 'NoData' != s:  # csv파일 공백
                if index == 0:  # content_Title
                    html = soup.select_one(s).text
                elif index in (2,3):  # content_StartDate, content_EndDate
                    date_str = soup.select_one(s).text
                    html = valid_start_end_date(index, date_str, csv_info['content_DateFormat'])
                elif index == 4:  # content_Body
                    # html = soup.select_one(s).contents  # list로 반환
                    if 'emptyBody' == s:
                        html = result_list[0]  # 내용 없을 시 제목을 추가
                    else:
                        # html = ''.join(str(item) for item in soup.select_one(s).contents)  # list로 반환된 body를 str로 변환
                        for element in soup(text=lambda text: isinstance(text, Comment)):  # 주석은 제거한다.
                            element.extract()
                        html = soup.select_one(s).prettify(formatter="None")  # 글내용
                        # html = html.replace('\n','')  # 유니코드 제거
                        html = html.replace('\n','').replace('\r','').replace('\t','').replace('\xad','').replace('\xa0','').replace('\u200b','')  # 유니코드 제거
                        if 'src="/' in html:
                            print('+++++++++ src="/ 수정 되었습니다 +++++++++')
                            src = 'src="' + csv_info['content_File_url'] + '/'
                            html = html.replace('src="/', src)

                elif index == 5:  # content_Files
                    if 'onclick' != s and 'ajax' != s and 'javascript' != s:
                        file_list = soup.select(s)
                        for i2, f in enumerate(file_list):
                            file_list[i2] = csv_info['content_File_url'] + f.get('href').replace(' ', '%20')
                    else:
                        file_list = []
                    html = file_list
            else:
                html = 'NoData'
        except Exception as e:
            print(e)
            print('########## get_board_content 예외발생 !!')
            html = 'NoData'
        finally:
            result_list.append(html)

    # print(result_list)
    content = {'title': valid_title(result_list[0]),
               'url': content_url,
               'dept_cd': csv_info['부처'],
               'wc_company_name': csv_info['기관'],
               'write_date': csv_info['content_WriteDate'],
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


# """" 타이틀 키워드를 필터링 합니다 """
def get_keyword_title(title, keyword_list):
    result = False

    search_keywords = keyword_list['search_keyword']
    ignore_keywords = keyword_list['ignore_keyword']

    for k in search_keywords:
        if k in title:
            result = True
    for ik in ignore_keywords:
        if ik in title:
            result = False
    return result


# """" 타이틀 키워드 필터링 리스트 csv파일을 불러옵니다 """
def csv_read_keyword(src):
    try:
        csv_reader = csv.DictReader(open(src, encoding='UTF-8'))
        field_names = csv_reader.fieldnames

        keyword_list = {}
        for fn in field_names:
            result_list = []
            keyword_list[fn] = result_list

        for row in csv_reader.reader:
            for index, field_name in enumerate(field_names):
                if '' != row[index]:
                    keyword_list[field_name].append(row[index])
    except FileNotFoundError:
        print('########## 파일을 찾을 수 없습니다 :', 'search_keyword.csv')
    return keyword_list


# """" 텔레그램 봇 """
def send_telegram_bot():
    bot = telegram.Bot(token='594957094:AAG2amlQoS-enenuId2brtRhN4aXqLJH0bw')
    result_text = '안녕하세요 !!'
    bot.sendMessage(chat_id=568182246, text=result_text)


# """" multiprocessing """
def multiprocessing():
    pool = Pool(processes=2)
    # pool = pool.map('함수명', '인자값')


# """" 공고 게시판 내용을 가져옵니다 Dict 타입으로 반환 """
def get_board_content_selenium(title, url, select_title):
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome('./chromedriver', chrome_options=options)
    driver.get(url)
    title_list = driver.find_elements_by_css_selector(select_title)
    for tr in title_list:
        # if tr.get_attribute('onclick') == onclick:
        if title in tr.text:
            print(tr.text)
            # title.click()
            # time.sleep(2)


def get_except_list():
    return except_list


# """" 공고 시작일, 마감일을 정제하여 반환합니다 """
def valid_start_end_date(date_type, date_str, content_DateFormat):
    date_str = date_str.strip().replace(' ','').replace('.','-')
    date_str = re.sub('[^0-9~-]', '', date_str)  # 2017-12-29~2018-01-03
    if 'YYYY-MM-DD~YYYY-MM-DD' == content_DateFormat:
        if 2 == date_type:  # content_StartDate : 2
            date_str = date_str[:10]
        elif 3 == date_type:  # content_EndDate : 3
            date_str = date_str[date_str.find('~')+1:date_str.find('~')+11]
    return valid_date(date_str, None).strftime('%Y-%m-%d')

