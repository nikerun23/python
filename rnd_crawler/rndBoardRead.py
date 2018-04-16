import requests
from bs4 import BeautifulSoup as bs
import rnd_crawler.utility as util


def print_RnD(csv_info, yesterday_list, keyword_list):
    print(csv_info['부처'], '---', csv_info['기관'], '---------------------------------------')
    print(csv_info['URL'])
    if 'X' == csv_info['Crawler']:  # Crawler
        print('X --- 크롤링 제외 ------------------------')
        return None
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
        html = util.selenium_read_board(csv_info)
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
        except ConnectionError as e:
            print(e)
            print('########## req.get ConnectionError 예외발생 !!')
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

    for tr in board_list:
        try:
            title_list = tr.select_one(select_title)
            title = util.valid_title(title_list.text)
            board_no = ''
            date_list = tr.select_one(select_date)
            board_date = util.valid_date(date_list.text, date_format)  # datetime객체로 반환
            # 전일 공고만 출력
            # if util.yesterday_check(yesterday_list, board_date):
            #     if util.get_keyword_title(title, keyword_list):
            #         print(board_no, title, board_date)  # 결과 데이터 라인
            # util.get_board_content_selenium(title,url,select_title)

            if 'href' in title_list.attrs:  # 제목 링크에 href가 존재할 경우만
                if 'http' in content_url[:7]:
                    title_url = util.valid_a_href(content_url,title_list.get('href'))
                    print('href 가 있습니다 =',title_url)
                    csv_info['content_WriteDate'] = board_date.strftime('%Y-%m-%d')
                    rnd_content = util.get_board_content(title_url, csv_info)
                    print(rnd_content)
                    print('============================================================')
            # if 'onclick' in title_list.attrs:  # 제목 링크에 onclick 존재할 경우만
            #     onclick = title_list.attrs['onclick']
            #     print('onclick 가 있습니다 = ', title_list.attrs['onclick'])
            #     title_href = onclick[onclick.find("'")+1:onclick.rfind("'")]
            #     print(content_url+title_href)
            #
            # print(board_no, title, board_date, '\n',content_url+title_href)


            # util.write_board_selenium(rnd_content)
        except AttributeError as e:
            print(e)
            print('########## Attribute Error PASS !!')
            pass
    print('-----------------------------------------------------------------------')


# +++++++++++ Main start +++++++++++++++++++++++++++++++++

# url_dict_list = util.csv_read_url('csv/url_list.csv')
url_dict_list = util.csv_read_url('csv/url_list - google.csv')
keyword_list = util.csv_read_keyword('csv/search_keyword.csv')
yesterday_list = util.get_yesterday_list()
# yesterday_list = [datetime.date(2018, 2, 27)]
# yesterday_list = [datetime.date(2018, 3, 9), datetime.date(2018, 3, 10), datetime.date(2018, 3, 11)]
print(keyword_list)


def print_list(ignore=999):
    for index, info in enumerate(url_dict_list):
        print('csv Row Num :',index + 2)
        if ignore == (index + 2):
            continue
        print_RnD(info, yesterday_list, keyword_list)


def print_test(row_num):
    row_num = row_num - 2  # index 값 보정
    # print(url_dict_list[row_num])
    print_RnD(url_dict_list[row_num], yesterday_list, keyword_list)


# print_list()  # 인자로 rowNum을 주면 제외하고 크롤링
print_test(90)

print('예외발생 : ',util.get_except_list())
print('++++++++++++++++++++++ 조회 완료 ++++++++++++++++++++++')

