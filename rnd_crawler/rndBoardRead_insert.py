# -*- coding: UTF-8 -*-
import requests
from bs4 import BeautifulSoup as bs
import rnd_crawler.utility as util
import logging.handlers
from rnd_crawler import ColoredFormatter
import http

def print_RnD(csv_info, yesterday_list, keyword_list, wc_company_dict):
    print(csv_info['SEED_ID'], '-', csv_info['부처'], '---', csv_info['기관'], '---------------------------------------')
    print(csv_info['URL'])
    if 'X' == csv_info['Crawler']:  # Crawler
        print('X --- 크롤링 제외 ------------------------')
        rnd_content_list = []
        return rnd_content_list
    seed_id = csv_info['SEED_ID']
    url = csv_info['URL']
    select_tr = csv_info['TR']
    select_title = csv_info['Title']
    select_date = csv_info['Date']
    etc_1_str = csv_info['etc_1']
    etc_2_str = csv_info['etc_2']
    date_format = csv_info['DateFormat']
    content_url = csv_info['a_href']
    html = ''

    if 'Ajax' == etc_1_str:  # Selenium
        # html = util.selenium_read_board(csv_info)
        html = util.sselenium_headless_read_board(csv_info)
    else:
        try:
            # etc_2 열
            if 'verify=False' == etc_2_str:
                req = requests.get(url, verify=False)
            else:
                req = requests.get(url)
        except ConnectionRefusedError as e:
            print(e)
            print('########## req.get ConnectionRefusedError 예외발생 !!')
        except http.client.RemoteDisconnected as e:
            logger.error(e)
            logger.error('########## req.get RemoteDisconnected 예외발생 !!')
        except ConnectionError as e:
            print(e)
            print('########## req.get ConnectionError 예외발생 !!')
        except Exception as e:
            print(e)
            print('########## req.get Exception 예외발생 !!')
        else:
            # etc_1 열
            if 'utf-8' == etc_1_str:
                req.encoding = 'utf-8'
            elif 'euc-kr' == etc_1_str:
                req.encoding = 'euc-kr'
            html = req.text
    # print(html)
    if '' == html:
        print('########## HTML에 정보가 없습니다 !!')
        return None

    soup = bs(html, 'lxml')
    board_list = soup.select(select_tr)
    # print(board_list)

    rnd_content_list = []
    for tr in board_list:
        try:
            title_list = tr.select_one(select_title)
            title = util.valid_title(title_list.text)
            date_list = tr.select_one(select_date)
            board_date = util.valid_date(date_list.text, date_format)  # datetime객체로 반환
            # 전일 공고만 출력
            # if util.yesterday_check(yesterday_list, board_date):
            #     if util.get_keyword_title(title, keyword_list):
            #         print(title.replace(u'\xa0', u' '), board_date)  # 결과 데이터 라인
            # util.get_board_content_selenium(title,url,select_title)

            # if util.yesterday_check(yesterday_list, board_date):
            if util.get_keyword_title(title, keyword_list):
                if 'href' in title_list.attrs and board_date is not None:  # 제목 링크에 href가 존재할 경우만
                    if 'http' in content_url[:7]:
                        title_url = util.valid_a_href(content_url,title_list.get('href'))
                        # print('href 가 있습니다 =',title_url)
                        csv_info['content_WriteDate'] = board_date.strftime('%Y-%m-%d')
                        rnd_content = util.get_board_content(title_url, csv_info, wc_company_dict)
                        print(rnd_content)
                        print('============================================================')
                        rnd_content_list.append(rnd_content)
            # if 'onclick' in title_list.attrs:  # 제목 링크에 onclick 존재할 경우만
            #     onclick = title_list.attrs['onclick']
            #     print('onclick 가 있습니다 = ', title_list.attrs['onclick'])
            #     title_href = onclick[onclick.find("'")+1:onclick.rfind("'")]
            #     print(content_url+title_href)
            #
            # print(board_no, title, board_date, '\n',content_url+title_href)
        except AttributeError as e:
            print(e)
            print('########## Attribute Error PASS !!')
            pass
    return rnd_content_list
    print('-----------------------------------------------------------------------')


# +++++++++++ Main start +++++++++++++++++++++++++++++++++

if __name__ == '__main__':

    logger = logging.getLogger('rndBoardRead')
    logger.setLevel(logging.DEBUG)
    streamHandler = logging.StreamHandler()
    # log_format = '[%(asctime)s]:%(levelname)-7s:%(message)s'
    # time_format = '%H:%M:%S'
    # formatter = ColoredFormatter.ColoredFormatter(log_format, datefmt=time_format)
    # streamHandler.setFormatter(formatter)
    logger.addHandler(streamHandler)

    url_dict_list = util.csv_read_url('csv/url_list - google.csv')
    keyword_list = util.csv_read_keyword('csv/search_keyword.csv')
    db_info = util.csv_read_url('csv/DB_info.csv')[1]  # DB 접속 정보 0: 운영, 1: dev
    wc_company_dict = util.get_WC_COMPANY_NAME(db_info)
    yesterday_list = util.get_yesterday_list()
    # yesterday_list = [datetime.date(2018, 2, 27)]
    # yesterday_list = [datetime.date(2018, 3, 9), datetime.date(2018, 3, 10), datetime.date(2018, 3, 11)]
    print(keyword_list)


    def print_list(start_row,end_row,ignore=999):
        insert_rnd_content_list = []
        for index, info in enumerate(url_dict_list):
            row_num = index + 2
            print('csv Row Num :', row_num)
            if ignore == (row_num) or not(start_row <= row_num and row_num <= end_row):
                continue

            rnd_content_list = print_RnD(info, yesterday_list, keyword_list, wc_company_dict)
            if rnd_content_list is not None:
                insert_rnd_content_list += rnd_content_list
            print('--------------------- 현재까지 INSERT 할 공고는 %s개입니다.' % len(insert_rnd_content_list))

        print('INSERT 할 공고가 %s개 있습니다.' % len(insert_rnd_content_list))
        if insert_rnd_content_list:
            util.insert_table_WC_CONTENT(insert_rnd_content_list, db_info)


    def print_test(row_num):
        row_num = row_num - 2  # index 값 보정
        # print(url_dict_list[row_num])
        insert_rnd_content_list = print_RnD(url_dict_list[row_num], yesterday_list, keyword_list, wc_company_dict)

        print('INSERT 할 공고가 %s개 있습니다.' % len(insert_rnd_content_list))
        if insert_rnd_content_list:
            util.insert_table_WC_CONTENT(insert_rnd_content_list, db_info)


    print_list(20,20,999)  # 인자로 rowNum을 주면 제외하고 크롤링
    # print_test(41)

    print('예외발생 : ',util.get_except_list())
    print('++++++++++++++++++++++ 조회 완료 ++++++++++++++++++++++')

