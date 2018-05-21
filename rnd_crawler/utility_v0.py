# -*- coding: UTF-8 -*-

import datetime
import csv
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
import time
import re
import requests
from bs4 import BeautifulSoup as bs, Comment
import telegram
from multiprocessing import Pool
import cx_Oracle
import os
import sys
import logging
import urllib
import chardet
import cgi
import uuid

os.environ['NLS_LANG'] = '.UTF8'  # UnicodeEncodeError
global except_list
except_list = []

logger = logging.getLogger('utility')
logger.setLevel(logging.DEBUG)

streamHandler = logging.StreamHandler()
# fomatter = logging.Formatter('[%(levelname)s|%(filename)s:%(lineno)s] %(asctime)s > %(message)s')
# streamHandler.setFormatter(fomatter)

logger.addHandler(streamHandler)


# """ 날짜를 검증합니다 """
def valid_date(date_str, date_fm):
    if date_str is None or re.search('[0-9]+', date_str, re.DOTALL) is None:  # 숫자가 없으면 return None
        raise Exception('날짜에 숫자가 없습니다 : %s' % date_str)
        # logger.debug('########## 날짜에 숫자가 없습니다 : %s' % date_str)
    if date_fm in ('DD/nYY.MM', '|YYYY-MM-DD', '작성일YYYY-MM-DD'):  # 불규칙한 날짜를 보완 (과학기술정보통신부, 국가수리과학연구소)
        try:
            date_str = modify_date(date_str, date_fm)
        except Exception as e:
            raise Exception(e)
    else:
        date_str = date_str.strip().replace(',', '-').replace('.', '-').replace('/', '-')
        # 마지막 '-' 삭제
        if date_str.count('-') > 2:
            date_str = date_str[:date_str.rfind('-')]
        # '~'있을시에 앞 날짜만 추출
        if '~' in date_str:
            date_str = date_str[:date_str.find('~')].replace('\n', '').replace('\t', '').strip()
        if ':' in date_str:  # HH:MM 포함되어 있을 경우 제거
            date_str = date_str[:date_str.find(':')-2]
        if '시' in date_str:  # HH시 포함되어 있을 경우 제거
            date_str = date_str[:date_str.find('시')-2]
        date_str = date_str.strip().replace(' ', '')
    # datetime 객체로 변환
    try:
        date_time_str = datetime.datetime.strptime(date_str, '%Y-%m-%d')
    except:
        raise Exception('날짜 양식에 문제가 있습니다 : %s' % date_str)
    else:
        return datetime.date(date_time_str.year, date_time_str.month, date_time_str.day)


# """ 글제목을 검증합니다 """
def valid_title(title_str):
    if title_str is None:
        return ''
    try:
        title_str = title_str.replace('새글', '').replace('New', '')\
            .replace('[진행중]', '').replace('[입찰안내]', '').replace('[공고]', '').replace('[용역]', '') \
            .replace('[입찰]', '').replace('제　목', '').replace('새 글', '')
        title_str = title_str.strip()
        title_str = title_str.replace('  ', '').replace('\t', '').replace('\n', '')
    except:
        raise Exception('글제목을 정제하는데 실패하였습니다')
    else:
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

    logger.debug('전일 : %s %s' % (yesterday, day_of_week[yesterday.weekday()]))
    logger.debug('크롤링 날짜 : %s' % yesterday_list)
    logger.debug('-----------------------------------------------------------------------------------')
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
        url_field_names = csv_reader.fieldnames
        for row in csv_reader.reader:
            url_dict = {}
            for ii, h in enumerate(url_field_names):
                url_dict[h] = row[ii].strip()
            url_dict_list.append(url_dict)
    except Exception as e:
        raise Exception(e)
    else:
        return url_dict_list


# """" 타이틀 키워드 필터링 리스트 csv파일을 불러옵니다 """
def csv_read_keyword(src):
    keyword_list = {}
    try:
        csv_reader = csv.DictReader(open(src, encoding='UTF-8'))
        field_names = csv_reader.fieldnames

        for fn in field_names:
            result_list = []
            keyword_list[fn] = result_list
        for row in csv_reader.reader:
            for index, field_name in enumerate(field_names):
                if '' != row[index]:
                    keyword_list[field_name].append(row[index])
    except Exception as e:
        raise Exception(e)
    else:
        return keyword_list


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
            result = re.sub('[^0-9-]', '', date_str)
        # 한국항공우주연구원
        elif '작성일YYYY-MM-DD' == date_fm:
            result = re.sub('[^0-9-]', '', date_str)
        else:
            result = ''

    except Exception:
        raise Exception('날짜 수정에 실패 하였습니다 : %s' % result)
        # logger.error('########## 날짜 수정에 실패 하였습니다 : %s' % result)
        # except_list.append({result: '########## 날짜 수정에 실패 하였습니다'})
        # result = ''
        # print('result :', result)
    else:
        return result


# """ URL을 수정하고 호스트와 합쳐 반환합니다 """
def valid_a_href(url, href):
    href = href.replace(' ', '%20').replace('./', '/').replace('../', '/').replace('&amp;', '&')
    if 'http:' in href:
        result = href
    else:
        result = url + href

    return result


# """" 공고 게시판 내용을 가져옵니다 Dict 타입으로 반환 """
def get_board_content(content_url, csv_info, wc_company_dict, html=None):
    select_list = [
        csv_info['content_Title'],
        csv_info['content_WriteDate'],
        csv_info['content_StartDate'],
        csv_info['content_EndDate'],
        csv_info['content_Body'],
        csv_info['content_Files'],
        csv_info['SEED_ID']
    ]
    if html is None:
        print('html is None')
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

    # print(html)
    result_list = []
    for index, css_select in enumerate(select_list):
        try:
            if '' != css_select and 'NoData' != css_select:  # csv파일 공백
                # content_Title
                if index == 0:
                    if 'trTitle' != css_select:
                        html = soup.select_one(css_select).text
                    else:
                        html = csv_info['trTitle']
                        # content_StartDate, content_EndDate
                elif index in (2,3):
                    if 2 == index and 'content_WriteDate' == css_select:  # 공고일을 공고 시작일로 한다
                        html = csv_info['content_WriteDate']
                    else:
                        date_str = soup.select_one(css_select).text
                        html = valid_start_end_date(index, date_str, csv_info['content_DateFormat'])
                # content_Body
                elif index == 4:
                    # html = soup.select_one(s).contents  # list로 반환
                    if 'emptyBody' == css_select:
                        html = result_list[0]  # 내용 없을 시 제목을 추가
                    else:
                        # html = ''.join(str(item) for item in soup.select_one(s).contents)  # list로 반환된 body를 str로 변환
                        for element in soup(text=lambda text: isinstance(text, Comment)):  # 주석은 제거한다.
                            element.extract()

                        html = soup.select_one(css_select).prettify(formatter="None")  # 글내용
                        html = re.sub('<script.*?>.*?</script>', '', html, 0, re.I | re.DOTALL)  # <script>태그를 글내용에서 제거한다. 0=모두삭제 re.I=대소문자모두 re.DOTALL=여러줄탐색
                        # html = soup.select_one(s).get_text()  # (str)글내용
                        html = html.replace('\n','').replace('\r','').replace('\t','').replace('\xad','').replace('\xa0','').replace('\u200b','').replace("\'",'`')  # 유니코드 제거
                        if 'src="/' in html:
                            logger.debug('+++++++++ src="/ 수정 되었습니다 +++++++++')
                            src = 'src="' + csv_info['content_File_url'] + '/'
                            html = html.replace('src="/', src)
                # content_Files
                elif index == 5:
                    if 'onclick' != css_select and 'ajax' != css_select and 'javascript' != css_select:
                        file_list = soup.select(css_select)
                        # print('file_list css_select :',css_select)
                        # print('file_list :',file_list)
                        for i2, f in enumerate(file_list):
                            file_dict = {'file_name': f.text.strip(), 'url': valid_a_href(csv_info['content_File_url'], f.get('href'))}
                            file_list[i2] = file_dict
                    else:
                        file_list = []
                    html = file_list
            else:
                html = 'NoData'
        except Exception as e:
            logger.error(e)
            logger.error('########## get_board_content 예외발생 !! : %s' % index)
            html = ''
            raise Exception(e)
        finally:
            result_list.append(html)

    # print(result_list)
    content = {'seed_id': csv_info['SEED_ID'],
               'title': valid_title(result_list[0]),
               'url': content_url,
               'dept_cd': csv_info['부처'],
               'wc_company_name': csv_info['부처'],
               'wc_ro_dpt_name': csv_info['기관'],
               'write_date': csv_info['content_WriteDate'],
               'start_date': result_list[2],
               'end_date': result_list[3],
               'body': result_list[4],
               'files': result_list[5]}
    return content


# """" Selenium을 이용하여 (str)Html 반환 """
def get_board_content_selenium(board_url, onclick, csv_info, wc_company_dict):
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-extensions")
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome('./chromedriver', chrome_options=options)
    driver.set_page_load_timeout(60)  # selenium timeout 60초
    try:

        driver.get(board_url)
        time.sleep(5)
        if 'onclickCSSClick' == csv_info['content_url']:
            click_css_list = []
            if ',' in csv_info['ClickCSS']:
                click_css_list = csv_info['ClickCSS'].split(',')
            else:
                click_css_list.append(csv_info['ClickCSS'])
            for css in click_css_list:
                driver.find_element_by_css_selector(css).click()
                time.sleep(5)

        logger.debug('onclick : %s' % onclick)
        css_click = 'a[onclick="%s"' % onclick
        logger.debug('css_click : %s' % css_click)
        driver.find_element_by_css_selector(css_click).click()
        logger.debug('driver.current_url : %s' % driver.current_url)
        time.sleep(5)

        html = driver.page_source
        rnd_content = get_board_content(driver.current_url, csv_info, wc_company_dict, html)
        logger.debug(rnd_content)
    except TimeoutException as e:
        logger.error('########## Selenium 작동이 중지 되었습니다 : %s' % e)
        html = ''
    except Exception as e:
        logger.error('########## Selenium 작동이 중지 되었습니다 : %s' % e)
        html = ''
    finally:
        driver.close()
        return html


def sselenium_headless_read_board(csv_info):
    # 크롬 옵션 추가하기
    logger.debug('--- sselenium_headless START !! ---')
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # 헤드리스모드
    options.add_argument('--disable-gpu')  # 호환성용 (필요없는 경우도 있음)
    options.add_argument('--window-size=1920x1080')  # (가상)화면 크기 조절
    # 크롬 모바일 버전으로 User Agent 설정하기
    options.add_argument("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36")
    # 크롬 Options를 넣어준 Headless 모드 크롬
    driver = webdriver.Chrome('./chromedriver', chrome_options=options)
    driver.set_page_load_timeout(60)  # selenium timeout 60초

    try:
        driver.get(csv_info['URL'])
        time.sleep(5)
        click_css_list = []
        if ',' in csv_info['ClickCSS']:
            click_css_list = csv_info['ClickCSS'].split(',')
        else:
            click_css_list.append(csv_info['ClickCSS'])
        for css in click_css_list:
            driver.find_element_by_css_selector(css).click()
            time.sleep(5)
        html = driver.page_source
    except TimeoutException as e:
        # logger.error('########## Selenium 작동이 중지 되었습니다 : %s' % e)
        # except_list.append({csv_info['기관']: '########## Selenium 작동이 중지 되었습니다 %s' % e})
        # html = ''
        driver.quit()
        raise Exception('########## Selenium 작동이 중지 되었습니다')
    except Exception as e:
        # logger.error('########## Selenium 작동이 중지 되었습니다 : %s' % e)
        # except_list.append({csv_info['기관']: '########## Selenium 작동이 중지 되었습니다 %s' % e})
        # html = ''
        driver.quit()
        raise Exception('########## Selenium 작동이 중지 되었습니다')


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


def get_except_list():
    return except_list


# """" 공고 시작일, 마감일을 정제하여 반환합니다 """
def valid_start_end_date(date_type, date_str, content_DateFormat):
    # date_str = date_str.replace('\n','')
    if re.search('[0-9]+', date_str, re.DOTALL) is None:  # 숫자가 없으면 return ''
        raise Exception('날짜에 숫자가 없습니다 : %s' % date_str)
        # logger.debug('########## 숫자가 없습니다 : %s' % date_str)
        # return ''
    try:
        date_str = date_str.strip().replace('.','-').replace('/','-')
        date_str = re.sub('[^0-9~/시:\s-]', '', date_str)  # 2017-12-29~2018-01-03
        if 'YYYY-MM-DD~YYYY-MM-DD' == content_DateFormat:
            if 2 == date_type:  # content_StartDate : 2
                date_str = date_str[:date_str.find('~')]
            elif 3 == date_type:  # content_EndDate : 3
                end_str = date_str[date_str.find('~') + 1:].strip()
                if re.search('\d{4}', end_str):  # 마감일에 연도가 없으면 시작일의 연도를 가져온다
                    year_str = end_str[:end_str.find('-')].strip()
                else:
                    year_str = date_str[:date_str.find('-')].strip()
                date_str = date_str[date_str.find('~')+1:]
                if year_str not in date_str:  # 마감일에 연도 없을 경우 시작일의 연도를 붙여준다
                    date_str = year_str + '-' + date_str.strip()
        logger.debug('date_str : %s %s' % (date_str, '시작일' if date_type == 2 else '마감일'))
        logger.debug('result : %s' % valid_date(date_str, None).strftime('%Y-%m-%d'))
        result = valid_date(date_str, None).strftime('%Y-%m-%d')
    except Exception as e:
        raise Exception(e)
    else:
        return result


def insert_table_WC_CONTENT(rnd_content_list, db_info):
    conn = cx_Oracle.connect(db_info['ID'], db_info['PWD'], db_info['IP'] + ':' + db_info['PORT'] + '/' + db_info['SID'])
    cursor = conn.cursor()

    insert_count = 0
    for rnd_content in rnd_content_list:

        # UID를 시퀀스로 조회한다
        UID_QUERY = "SELECT WC_CONTENT_PYTHON_SEQ.NEXTVAL FROM DUAL"
        cursor.execute(UID_QUERY)

        WA_UID = cursor.fetchone()[0]
        WA_BBS_UID = rnd_content['seed_id']  # 마스터UID
        WC_TITLE = rnd_content['title']  # 제목
        WC_WRITER = ''  # 작성자
        WC_URL = rnd_content['url']  # URL
        WC_DT = '' if 'NoData' == rnd_content['write_date'] else rnd_content['write_date']  # 고유작성일 (공고등록일)
        # WC_COLL_DT = 'SYSDATE'  # 수집일자
        WC_P_CONTENT = rnd_content['body']  # 내용
        WC_KEYWORD_CODE = '402001'  # 마스터분류코드 (공고 402001)
        WC_COMPANY_NAME = rnd_content['wc_company_name']  # 공고기관명(부처ID)
        COL3 = '' if 'NoData' == rnd_content['start_date'] else rnd_content['start_date']  # 공고일(접수 시작일)
        COL4 = '' if 'NoData' == rnd_content['end_date'] else rnd_content['end_date']  # 접수마감일
        TEXT_UID = WA_UID  # TEXT_UID
        WA_DB_VIEW = 'Y'  # Y
        WC_MEM_ID = '파이썬'  # 파이썬
        WC_RO_DPT_NAME = rnd_content['wc_ro_dpt_name']  # 기관

        insert_item = (WA_BBS_UID, WA_UID, WC_TITLE, WC_WRITER, WC_URL, WC_DT, WC_P_CONTENT, WC_KEYWORD_CODE, WC_COMPANY_NAME, COL3, COL4, TEXT_UID, WA_DB_VIEW, WC_MEM_ID, WC_RO_DPT_NAME)

        INSET_QUERY = "insert into WC_CONTENT " \
                      "(WA_BBS_UID, WA_UID, WC_TITLE, WC_WRITER, WC_URL, WC_DT, WC_COLL_DT, WC_P_CONTENT, WC_KEYWORD_CODE, WC_COMPANY_NAME, COL3, COL4, TEXT_UID, WA_DB_VIEW, WC_MEM_ID, WC_RO_DPT_NAME) " \
                      "values (:1,:2,:3,:4,:5,TO_DATE(:6,'YYYY-MM-DD'),SYSDATE,:7,:8,:9,TO_DATE(:10,'YYYY-MM-DD'),TO_DATE(:11,'YYYY-MM-DD'),:12,:13,:14,:15)"
        try:
            cursor.execute(INSET_QUERY, insert_item)
        except:
            raise Exception('# Query failed : %s' % INSET_QUERY)
        else:
            insert_count += 1
            conn.commit()
            # logger.debug('info commit()')
            # print(rnd_content['files'])
            if rnd_content['files']:
                insert_table_WC_FILE(rnd_content['files'], WA_UID, conn, WA_BBS_UID)

    logger.debug('%s개의 공고가 성공적으로 INSERT 되었습니다.' % insert_count)
    cursor.close()
    # print('cursor.close()')
    conn.close()
    # print('conn.close()')
    return insert_count


def insert_table_WC_FILE(file_list, WA_UID, conn, WA_BBS_UID2):
    # print('=== insert_table_WC_FILE ==========================================')
    # print(file_list)
    cursor = conn.cursor()

    insert_items = []
    for index, file in enumerate(file_list):
        # UID를 시퀀스로 조회한다
        UID_QUERY = "SELECT WC_FILE_PYTHON_SEQ.NEXTVAL FROM DUAL"
        cursor.execute(UID_QUERY)

        download_path = 'upload/boardun/'
        uid_file_name = str(uuid.uuid4())
        file['uid_file_name'] = uid_file_name

        file_size = file_download(file, download_path)  # 물리파일 다운로드

        # 파일명 확장자 이후 데이터 정제
        file_name = file['file_name']
        for k in ('.hwp','.hml','.zip','.pdf','.jpg','.png','.gif','.hwt'):
            if file_name.find(k) > 2:
                file_name = file_name[:file_name.find(k) + 4]
        if '' == file_name:
            file_name = 'download'

        WF_UID = cursor.fetchone()[0]
        WA_BBS_PHY_NUM = WA_UID  # WC_CONTENT 테이블의 WA_UID 컬럼과 동일
        WF_BBS_PHY_TYPE = 1  # 타입 : 1
        WF_FILE_NUM = index + 1  # 파일순서
        WF_FILE_PATH = uid_file_name  # 난수의 파일명
        WF_FILE_DIRE = download_path + uid_file_name  # 저장된 경로+파일명 upload/boardun/931565f7-74c7-4efb-83e3-eafe832504cb(WF_FILE_PATH값과동일)
        WA_BBS_UID = WA_BBS_UID2  # 999 Master코드
        WF_FILE_NAME = file_name  # 원본 파일명 (3.+과업설명서.hwp)
        TEXT_UID = WF_UID  # 첨부문서UID
        WF_SIZE = file_size  # 파일사이즈

        insert_items.append((WF_UID, WA_BBS_PHY_NUM, WF_BBS_PHY_TYPE, WF_FILE_NUM, WF_FILE_PATH, WF_FILE_DIRE, WA_BBS_UID, WF_FILE_NAME, TEXT_UID, WF_SIZE))

    # print(insert_items)
    INSET_QUERY = "insert into WC_FILE " \
                  "(WF_UID, WA_BBS_PHY_NUM, WF_BBS_PHY_TYPE, WF_FILE_NUM, WF_FILE_PATH, WF_FILE_DIRE, WA_BBS_UID, WF_FILE_NAME, TEXT_UID, WF_SIZE) " \
                  "values (:1,:2,:3,:4,:5,:6,:7,:8,:9,:10)"

    insert_count = 0
    for row in insert_items:
        try:
            # cursor.bindarraysize = len(insert_items)
            # cursor.executemany(INSET_QUERY, insert_items)
            cursor.execute(INSET_QUERY, row)
            insert_count += 1
        except:
            raise Exception('# Query failed : %s' % INSET_QUERY)
        finally:
            conn.commit()
            # logger.debug('file commit()')
    logger.debug('%s개의 파일 정보가 성공적으로 INSERT 되었습니다.' % insert_count)
    # print('cursor.close()')
    cursor.close()


def get_WC_COMPANY_NAME(db_info):
    try:
        conn = cx_Oracle.connect(db_info['ID'], db_info['PWD'], db_info['IP'] + ':' + db_info['PORT'] + '/' + db_info['SID'])
        cursor = conn.cursor()

        SELECT_QUERY = "select CD_DTL_ID, CD_NM from TCO_CD_DTL where CD_ID = 400"
        cursor.execute(SELECT_QUERY)

        select_list = cursor.fetchall()
        wc_company_list = {}

        for item in select_list:
            wc_company_list[item[1]] = item[0]
    except:
        raise Exception('WC_COMPANY_NAME Query failed : %s' % SELECT_QUERY)
    else:
        return wc_company_list
    finally:
        cursor.close()
        conn.close()
        logger.debug('cursor.close() conn.close()')


def insert_table_WC_LOG(seed_id, rnd_count, db_info):
    conn = cx_Oracle.connect(db_info['ID'], db_info['PWD'], db_info['IP'] + ':' + db_info['PORT'] + '/' + db_info['SID'])
    cursor = conn.cursor()

    try:
        UID_QUERY = "SELECT WC_LOG_PYTHON_SEQ.NEXTVAL FROM DUAL"
        cursor.execute(UID_QUERY)

        WM_BBS_UID = cursor.fetchone()[0]
        WL_URL = seed_id
        WL_LOGS = ''  # 첨부문서UID
        WL_INS_COUNT = rnd_count

        insert_item = (WM_BBS_UID, WL_URL, WL_LOGS, WL_INS_COUNT)
        INSET_QUERY = "insert into WC_LOG " \
                      "(WM_BBS_UID, WL_URL, WL_LOGS, WL_INS_DT, WL_INS_COUNT) " \
                      "values (:1,:2,:3,SYSDATE, :4)"
        cursor.execute(INSET_QUERY, insert_item)
        conn.commit()
    except:
        raise Exception('insert_table_WC_LOG Query failed : %s' % INSET_QUERY)
    finally:
        cursor.close()
        conn.close()
        logger.debug('cursor.close() conn.close()')


# """ 물리 파일을 저장한다 """
def file_download(file_info,download_path):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
    }

    url = file_info['url'].replace('%20', ' ')
    print('file_download url :',url)

    response = requests.get(url, stream=True)

    file_name = file_info['uid_file_name']
    file_path = download_path + file_name

    print('file_path :', file_path)

    directory = os.path.dirname(file_path)  # 폴더경로만 반환한다
    if not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)  # exist_ok=True 상위 경로도 생성한다

    f = open(file_path, "wb")

    for chunk in response.iter_content(chunk_size=1024):
        if chunk:
            f.write(chunk)
    f.close()
    time.sleep(1)
    file_size = os.path.getsize(file_path)

    return file_size


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

    # driver.find_element_by_css_selector('.se2_inputarea').send_keys('send_keys')  # 공고형태
    driver.find_element_by_css_selector('#smart_editor2_content .se2_to_html').click()  # 공고형태

    # driver.execute_script('document.getElementById("#smart_editor2_content")')
    # driver.find_element_by_css_selector('#smart_editor2_content body').send_keys(body)
    # driver.find_element_by_css_selector('#smart_editor2_content body').send_keys(body)