# -*- coding: UTF-8 -*-

import requests
from bs4 import BeautifulSoup as bs
import rnd_crawler.utility_v1 as util
import logging
import logging.handlers
from rnd_crawler import ColoredFormatter
import http
import datetime

def print_RnD(csv_info, yesterday_list, keyword_list, wc_company_dict):
    if 'X' == csv_info['Crawler']:  # Crawler
        logger.debug('X --- 크롤링 제외 ------------------------')
        return None
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
            logger.error(e)
            logger.error('########## req.get ConnectionRefusedError 예외발생 !!')
        except http.client.RemoteDisconnected as e:
            logger.error(e)
            logger.error('########## req.get RemoteDisconnected 예외발생 !!')
        except ConnectionError as e:
            logger.error(e)
            logger.error('########## req.get ConnectionError 예외발생 !!')
        except Exception as e:
            logger.error(e)
            logger.error('########## req.get Exception 예외발생 !!')
        else:
            # etc_1 열
            if 'utf-8' == etc_1_str:
                req.encoding = 'utf-8'
            elif 'euc-kr' == etc_1_str:
                req.encoding = 'euc-kr'
            html = req.text
    # print(html)
    if '' == html:
        logger.error('########## HTML에 정보가 없습니다 !!')
        return None

    soup = bs(html, 'lxml')
    board_list = soup.select(select_tr)
    # print(board_list)

    crawlwe_result = False
    for tr in board_list:
        try:
            title_list = tr.select_one(select_title)
            title = util.valid_title(title_list.text)
            date_list = tr.select_one(select_date)
            board_date = util.valid_date(date_list.text, date_format)  # datetime객체로 반환
            # 전일 공고만 출력
            if util.yesterday_check(yesterday_list, board_date):
                if util.get_keyword_title(title, keyword_list):
                    # print("%s %s" % (title, board_date))  # 결과 데이터 라인
                    logger.info("%s %s" % (title.replace('\xad','').replace('\xa0','').replace('\u200b','').replace('\u2024',''), board_date))  # 결과 데이터 라인
                    # logger.info("%s %s" % (title, board_date))  # 결과 데이터 라인

            # util.get_board_content_selenium(title,url,select_title)

            # if util.get_keyword_title(title, keyword_list):
            #     if 'href' in title_list.attrs and board_date is not None:  # 제목 링크에 href가 존재할 경우만
            #         if 'http' in content_url[:7]:
            #             title_url = util.valid_a_href(content_url,title_list.get('href'))
            #             print('href 가 있습니다 =',title_url)
            #             csv_info['content_WriteDate'] = board_date.strftime('%Y-%m-%d')
            #             rnd_content = util.get_board_content(title_url, csv_info, wc_company_dict)
            #             logger.debug(rnd_content)
            #             logger.debug('============================================================')
            # if 'onclick' in title_list.attrs:  # 제목 링크에 onclick 존재할 경우만
            #     onclick = title_list.attrs['onclick']
            #     print('onclick 가 있습니다 = ', title_list.attrs['onclick'])
            #     title_href = onclick[onclick.find("'")+1:onclick.rfind("'")]
            #     print(content_url+title_href)
            #
        except Exception as e:
            logger.error(e)
            logger.error('########## Exception Error PASS !!')
            pass
        else:
            crawlwe_result = True
    if not crawlwe_result:
        logger.debug('seed_id: %s 크롤링에 실패하였습니다' % seed_id)
    logger.debug('----------------------------------------------------------')
    # logger.debug('%s ----------' % crawlwe_result)


# +++++++++++ Main start +++++++++++++++++++++++++++++++++
#
if __name__ == '__main__':
    logger = logging.getLogger('rndBoardRead')
    logger.setLevel(logging.DEBUG)

    streamHandler = logging.StreamHandler()
    fileHandler = logging.FileHandler('./log/test.log')

    # log_format = '[%(asctime)s]:%(levelname)-7s:%(message)s'
    # time_format = '%H:%M:%S'
    # formatter = ColoredFormatter.ColoredFormatter(log_format, datefmt=time_format)
    # streamHandler.setFormatter(formatter)

    logger.addHandler(streamHandler)
    # logger.addHandler(fileHandler)

    try:
        url_dict_list = util.csv_read_url('csv/url_list - google.csv')
        keyword_list = util.csv_read_keyword('csv/search_keyword.csv')
        db_info = util.csv_read_url('csv/DB_info.csv')[1]  # DB 접속 정보 0: 운영, 1: dev
        wc_company_dict = util.get_WC_COMPANY_NAME(db_info)
        yesterday_list = util.get_yesterday_list()
        # yesterday_list = [datetime.date(2018, 4, 30),datetime.date(2018, 5, 1)]        # yesterday_list = [datetime.date(2018, 3, 9), datetime.date(2018, 3, 10), datetime.date(2018, 3, 11)]
        logger.debug(keyword_list)

        def print_list(ignore=999):
            for index, crawler_info in enumerate(url_dict_list):
                logger.debug('csv Row Num : %s' % (index + 2))
                if ignore == (index + 2):
                    continue
                logger.debug('%s - %s --- %s ---------------------------------------' % (crawler_info['SEED_ID'], crawler_info['부처'], crawler_info['기관']))
                logger.debug(crawler_info['URL'])
                print_RnD(crawler_info, yesterday_list, keyword_list, wc_company_dict)


        def print_test(row_num):
            row_num = row_num - 2  # index 값 보정
            crawler_info = url_dict_list[row_num]
            logger.debug('%s - %s --- %s ---------------------------------------' % (
            crawler_info['SEED_ID'], crawler_info['부처'], crawler_info['기관']))
            logger.debug(crawler_info['URL'])
            print_RnD(url_dict_list[row_num], yesterday_list, keyword_list, wc_company_dict)

        print_list()  # 인자로 rowNum을 주면 제외하고 크롤링
        # print_test(8)
    except Exception as e:
        print('==========================================================')
        print(e)
        print('==========================================================')
    logger.debug('예외발생 : %s' % util.get_except_list())
    logger.debug('++++++++++++++++++++++ 조회 완료 ++++++++++++++++++++++')

