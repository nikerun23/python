import requests
from bs4 import BeautifulSoup as bs

url = 'http://www.kfi.or.kr/home/brd/brd230/brd230_Type4_Lis.do?board_seq=14'
select_tr = 'li.pd_t4 table.board_tb tr'
select_title = 'td:nth-of-type(2) a'
select_date = 'td:nth-of-type(3)'

req = requests.get(url)
# req = requests.get(url, verify=False)
# req.encoding = 'utf-8'
# req.encoding = 'euc-kr'
html = req.text
# print(html)
soup = bs(html, 'lxml')
board_list = soup.select(
    select_tr
)

# print(board_list)
for i in board_list:
    try:
        title_list = i.select_one(select_title)
        title = title_list.text
        board_no = ''
        date_list = i.select_one(select_date)
        date_str = date_list.text.strip()

        print(board_no, title, date_str)
    except AttributeError:
        print('AttributeError !!')
        pass



