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
        # if ((index + 2) == 50):
        #     continue
        print('csv Row Num :',index + 2)
        print_RnD(info, yesterday_list)


def print_test(row_num):
    row_num = row_num - 2  # index 값 보정
    print(url_dict_list[row_num])
    print_RnD(url_dict_list[row_num], yesterday_list)


print_list()
# print_test(89)

# +++++++++++ Main end +++++++++++++++++++++++++++++++++

print('++++++++++++++++++++++ 조회 완료 ++++++++++++++++++++++')

# 중복검사
# http://www.ntis.go.kr/rndgate/eg/un/ra/confirm.do
# wcTitle : 'TEST공고명'

# 등록
# headers = {
#     'Origin': 'http://www.ntis.go.kr',
#     'Accept-Encoding': 'gzip, deflate',
#     'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36',
#     'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
#     'Accept': 'application/json, text/javascript, */*; q=0.01',
#     'Referer': 'http://www.ntis.go.kr/rndgate/eg/un/ra/createForm.do',
#     'X-Requested-With': 'XMLHttpRequest',
#     'Connection': 'keep-alive',
# }
#
# data = [
#   ('waUid', ''),
#   ('waBbsUid', ''),
#   ('confirmYn', 'Y'),
#   ('roFormCd', '28802'),
#   ('deptCd', 'P50'),
#   ('wcCompanyName', 'TEST\uACF5\uACE0\uAE30\uAD00\uBA85'),
#   ('wcTitle', 'TEST\uACF5\uACE0\uBA85'),
#   ('wcUrl', 'TESTURL'),
#   ('wcDt', '2018-03-14'),
#   ('roStrtDt', '2018-03-15'),
#   ('roEndDt', '2018-03-17'),
#   ('roDivCd', ''),
#   ('roAmt', ''),
#   ('hour', '00'),
#   ('min', '00'),
#   ('roReference', ''),
#   ('roDbrainCd', ''),
#   ('wcPContent', '<span style="font-size: 12px;">TEST</span><span style="color: rgb(32, 32, 32); font-family: &quot;Nanum Gothic&quot;, sans-serif; font-size: 13px; letter-spacing: -1px; text-align: right; background-color: rgb(243, 243, 243);">\uACF5\uACE0\uB0B4\uC6A9</span>'),
#   ('', ''),
# ]
#
# response = requests.post('http://www.ntis.go.kr/rndgate/eg/un/ra/create.do', headers=headers, cookies=cookies, data=data)
