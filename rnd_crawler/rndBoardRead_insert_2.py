# -*- coding: UTF-8 -*-
import requests
from bs4 import BeautifulSoup as bs
import rnd_crawler.utility_v1 as util
import logging.handlers
from rnd_crawler import ColoredFormatter
import http
import datetime

def print_RnD(csv_info, yesterday_list, keyword_list, wc_company_dict):
    if 'X' == csv_info['Crawler']:  # Crawler
        logger.debug('X --- 크롤링 제외 ------------------------')
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
    if '' == html:
        logger.error('########## HTML에 정보가 없습니다 !!')
        return None

    soup = bs(html, 'lxml')
    board_list = soup.select(select_tr)

    rnd_content_list = []
    for tr in board_list:
        try:
            title_list = tr.select_one(select_title)
            title = util.valid_title(title_list.text)
            date_list = tr.select_one(select_date)
            board_date = util.valid_date(date_list.text, date_format)  # datetime객체로 반환

            if util.yesterday_check(yesterday_list, board_date):
                if util.get_keyword_title(title, keyword_list):
                    if 'href' in title_list.attrs and board_date is not None:  # 제목 링크에 href가 존재할 경우만
                        if 'http' in content_url[:7]:
                            title_url = util.valid_a_href(content_url,title_list.get('href'))
                            csv_info['content_WriteDate'] = board_date.strftime('%Y-%m-%d')  # 공고 작성일
                            rnd_content = util.get_board_content(title_url, csv_info, wc_company_dict)
                            logger.debug(rnd_content)
                            logger.debug('============================================================')
                            rnd_content_list.append(rnd_content)

        except AttributeError as e:
            logger.error('########## Attribute Error PASS !!')
            logger.error(e)
            pass
        except Exception as e:
            logger.error('########## print_RnD() : Exception Error PASS !!')
            logger.error(e)
            pass
    logger.debug('-----------------------------------------------------------------------')
    return rnd_content_list


# +++++++++++ Main start +++++++++++++++++++++++++++++++++

if __name__ == '__main__':

    logger = logging.getLogger('rndBoardRead')
    logger.setLevel(logging.DEBUG)
    streamHandler = logging.StreamHandler()
    logger.addHandler(streamHandler)

    url_dict_list = util.csv_read_url('csv/url_list - google.csv')
    keyword_list = util.csv_read_keyword('csv/search_keyword.csv')
    db_info = util.csv_read_url('csv/DB_info.csv')[1]  # DB 접속 정보 0: 운영, 1: dev
    wc_company_dict = util.get_WC_COMPANY_NAME(db_info)

    # yesterday_list = [datetime.date(2018, 2, 27)]
    # yesterday_list = [datetime.date(2018, 4, 20)
    #     , datetime.date(2018, 4, 23)
    #     , datetime.date(2018, 4, 24)
    #     , datetime.date(2018, 4, 25)
    #     , datetime.date(2018, 4, 26)
    #     , datetime.date(2018, 4, 27)]
    yesterday_list = util.get_yesterday_list()


    def print_list(start_row,end_row,ignore=999):
        insert_rnd_content_list = []
        insert_count = 0
        for index, crawler_info in enumerate(url_dict_list):
            try:
                row_num = index + 2
                logger.debug('csv Row Num : %d' % row_num)
                if ignore == (row_num) or not(start_row <= row_num and row_num <= end_row):
                    continue

                logger.debug('%s - %s --- %s ---------------------------------------' % (crawler_info['SEED_ID'], crawler_info['부처'], crawler_info['기관']))
                logger.debug(crawler_info['URL'])
                rnd_content_list = print_RnD(crawler_info, yesterday_list, keyword_list, wc_company_dict)
                if rnd_content_list is not None:
                    insert_rnd_content_list += rnd_content_list
                logger.debug('--------------------- 현재까지 INSERT 할 공고는 %s개입니다.' % len(insert_rnd_content_list))
                util.insert_table_WC_LOG(crawler_info['SEED_ID'], len(rnd_content_list), db_info)
            except Exception as e:
                logger.error('print_list() Exception !!')
                logger.error(e)
                pass

        rnd_len = len(insert_rnd_content_list)
        logger.debug('INSERT 할 공고가 %s개 있습니다.' % rnd_len)
        if insert_rnd_content_list:
            insert_count = util.insert_table_WC_CONTENT(insert_rnd_content_list, db_info)
            # print('util.insert_table_WC_FILE')
            # print('===========================================================')
            # for file_list in insert_rnd_content_list:
            #     print(file_list['files'])
                # util.insert_table_WC_FILE(file_list['files'], db_info)
        return insert_count


    rnd_len = print_list(2,130,999)  # 인자로 rowNum을 주면 제외하고 크롤링

    logger.debug('예외발생 : %s' % util.get_except_list())

    logger.debug('++++++++++++++++++++++ 조회 완료 ++++++++++++++++++++++')

