import requests
from bs4 import BeautifulSoup as bs

url = 'http://www.mohw.go.kr/react/al/sal0201ls.jsp?PAR_MENU_ID=04&MENU_ID=0402'
select_tr = 'div.board_list table > tbody > tr'
select_title = 'td.ta_l a'
select_date = 'td:nth-of-type(3)'

req = requests.get(url)
# req.encoding = 'utf-8'
# req.encoding = 'euc-kr'
html = req.text
# print(html)
soup = bs(html, 'lxml')
board_list = soup.select(
    select_tr
)
# print(boardList)
for i in board_list:

    title_list = i.select_one(select_title)
    title = title_list.text
    board_no = ''
    date_list = i.select_one(select_date)
    date_str = date_list.text

    print(board_no, title, date_str)

