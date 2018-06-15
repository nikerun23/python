# -*- coding: UTF-8 -*-

import requests
from bs4 import BeautifulSoup as bs
import rnd_crawler.utility_v0 as util_v0
import rnd_crawler.utility_v1 as util
import logging
import logging.handlers
from rnd_crawler import ColoredFormatter
import http
import datetime

global except_list
except_list = []

def print_RnD(csv_info, yesterday_list, keyword_list, wc_company_dict):
    if 'N' == csv_info['USE_YN']:  # Crawler
        logger.debug('X --- 크롤링 제외 ------------------------')
        return None
    seed_id = csv_info['SEED_ID']
    url = csv_info['URL']
    select_tr = csv_info['TR']
    select_title = csv_info['Title']
    select_date = csv_info['Date']
    etc_1_str = csv_info['ETC_1']
    etc_2_str = csv_info['ETC_2']
    date_format = csv_info['DateFormat']
    content_url = csv_info['content_url']
    html = ''

    if 'Ajax' == etc_1_str:  # Selenium
        html = util.selenium_headless_read_board(csv_info)
    else:
        try:
            # etc_2 열
            if 'verify=False' == etc_2_str:
                req = requests.get(url, verify=False)
            else:
                req = requests.get(url)
        except http.client.RemoteDisconnected as e:
            logger.error(e)
            logger.error('########## req.get RemoteDisconnected 예외발생 !!')
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

        except Exception as e:
            logger.error(e)
            logger.error('########## Exception Error PASS !!')
            pass
        else:
            crawlwe_result = True
    if not crawlwe_result:
        logger.debug('seed_id: %s 크롤링에 실패하였습니다' % seed_id)
    logger.debug('----------------------------------------------------------')


# +++++++++++ Main start +++++++++++++++++++++++++++++++++
#
if __name__ == '__main__':
    logger = logging.getLogger('rndBoardRead')
    logger.setLevel(logging.DEBUG)

    streamHandler = logging.StreamHandler()
    # fileHandler = logging.FileHandler('./log/test.log')

    # log_format = '[%(asctime)s]:%(levelname)-7s:%(message)s'
    # time_format = '%H:%M:%S'
    # formatter = ColoredFormatter.ColoredFormatter(log_format, datefmt=time_format)
    # streamHandler.setFormatter(formatter)

    logger.addHandler(streamHandler)
    # logger.addHandler(fileHandler)

    try:
        url_dict_list = util_v0.csv_read_url('csv/url_list - google.csv')
        keyword_list = util_v0.csv_read_keyword('csv/search_keyword.csv')
        wc_company_dict = {'소방방재청': '400051', '지식경제부': '400071', '농림수산식품부': '400072', '문화체육관광부': '400073', '국토해양부': '400074', '교육과학기술부': '400075', '보건복지부': '400025', '기타': '400001', '교육인적자원부': '400014', '방위사업청': '400018', '행정안전부': '400019', '과학기술부': '400020', '문화관광부': '400021', '농림부': '400022', '산업자원부': '400023', '정보통신부': '400024', '환경부': '400026', '노동부': '400027', '건설교통부': '400029', '해양수산부': '400030', '기상청': '400043', '농촌진흥청': '400045', '산림청': '400046', '중소기업청': '400047', '식품의약품안전처': '400049', '문화재청': '400050', '기 타': '400099', '국무총리실': '400077', '국가청소년위원회': '400091', '원자력안전위원회': '400092', '방송통신위원회': '400080', '기획재정부': '400079', '경찰청': '400081', '공정거래위원회': '400082', '국방부': '400083', '법무부': '400084', '법제처': '400085', '여성부': '400086', '외교통상부': '400087', '통일부': '400088', '해양경찰청': '400089', '행정중심복합도시건설': '400090', '국가과학기술위원회': '400078', '고용노동부': '400060', '관세청': '400061', '과학기술정보통신부': '400062', '교육부': '400063', '국무조정실': '400064', '조달청': '400065', '국토교통부': '400066', '농림축산식품부': '400067', '산업통상자원부': '400068', '소방청': '400069', '여성가족부': '400070', '외교부': '400052', '국세청': '400053', '인사혁신처': '400054', '통계청': '400055', '중소벤처기업부': '400056', '특허청': '400057', '범부처 사업': '400058'}

        yesterday_list = util.get_yesterday_list()
        yesterday_list = [datetime.date(2018, 6, 11),datetime.date(2018, 6, 12),datetime.date(2018, 6, 14)]
        logger.debug(keyword_list)

        def print_list(start_row,end_row,ignore=999):
            for row_num, crawler_info in enumerate(url_dict_list):
                row_num = row_num + 2
                logger.debug('csv Row Num : %s' % (row_num))
                if ignore == (row_num) or not(start_row <= row_num and row_num <= end_row):
                    continue
                logger.debug('%s - %s --- %s ---------------------------------------' % (crawler_info['SEED_ID'], crawler_info['부처'], crawler_info['기관']))
                logger.debug(crawler_info['URL'])
                print_RnD(crawler_info, yesterday_list, keyword_list, wc_company_dict)

        print_list(1,130,999)  # 인자로 rowNum을 주면 제외하고 크롤링

    except Exception as e:
        logger.debug('==========================================================')
        logger.debug(e)
        logger.debug('==========================================================')
    logger.debug('예외발생 : %s' % util.get_except_list())
    logger.debug('++++++++++++++++++++++ 조회 완료 ++++++++++++++++++++++')

