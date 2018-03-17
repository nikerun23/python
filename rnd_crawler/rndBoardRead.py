import requests
from bs4 import BeautifulSoup as bs
import rnd_crawler.utility as util


def print_RnD(csv_info, yesterday_list):
    print(csv_info['부처'], '---', csv_info['기관'], '---------------------------------------')
    print(csv_info['URL'])
    url = csv_info['URL']
    select_tr = csv_info['TR']
    select_title = csv_info['Title']
    select_date = csv_info['Date']
    etc_1_str = csv_info['etc_1']
    etc_2_str = csv_info['etc_2']
    date_format = csv_info['DateFormat']
    content_url = csv_info['a_href']

    if 'Ajax' == etc_1_str:  # Selenium
        html = util.selenium_read_board(csv_info)
    else:
        # etc_2 열
        if 'verify=False' == etc_2_str:
            req = requests.get(url, verify=False)
        else:
            req = requests.get(url)
        # etc_1 열
        if 'utf-8' == etc_1_str:
            req.encoding = 'utf-8'
        elif 'euc-kr' == etc_1_str:
            req.encoding = 'euc-kr'
        html = req.text
        # print(util.valid_a_href(url, '/jfile/readDownloadFile.do?fileId=MOF_ARTICLE_19241&amp;fileSeq=1'))

    # print(html)
    if '' == html:
        print('########## HTML에 정보가 없습니다 !!')
        return

    soup = bs(html, 'lxml')
    board_list = soup.select(select_tr)
    # print(board_list)
    # if 'tr th' == etc_2_str:  # th가 tr에 포함되어있을때 tr 제거
        # board_list = board_list[1:]
    for tr in board_list:
        try:
            title_list = tr.select_one(select_title)
            title = util.valid_title(title_list.text)
            title_href = title_list.get('href')
            board_no = ''
            date_list = tr.select_one(select_date)
            board_date = util.valid_date(date_list.text, date_format)  # datetime객체로 반환
            # 전일 공고만 출력
            # if util.yesterday_check(yesterday_list, board_date):
            print(board_no, title, board_date)
                # print(board_no, title, board_date, '\n',content_url+title_href)
                # util.get_board_content(content_url+title_href, csv_info)
        except AttributeError as e:
            print(e)
            print('########## Attribute Error PASS !!')
            pass
    print('-----------------------------------------------------------------------')


# +++++++++++ Main start +++++++++++++++++++++++++++++++++

url_dict_list = util.csv_read_url('csv/url_list.csv')
yesterday_list = util.get_yesterday_list()
# yesterday_list = [datetime.date(2018, 2, 27)]
# yesterday_list = [datetime.date(2018, 3, 9), datetime.date(2018, 3, 10), datetime.date(2018, 3, 11)]


def print_list():
    for index, info in enumerate(url_dict_list):
        print('csv Row Num :',index + 2)
        print_RnD(info, yesterday_list)


def print_test(row_num):
    row_num = row_num - 2  # index 값 보정
    print(url_dict_list[row_num])
    print_RnD(url_dict_list[row_num], yesterday_list)


print_list()
# print_test(89)

print('++++++++++++++++++++++ 조회 완료 ++++++++++++++++++++++')

