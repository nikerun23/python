import requests
from bs4 import BeautifulSoup as bs

url = 'https://www.nrf.re.kr/tender/list?menu_no=57'
select_tr = 'div.board_list tbody > tr'
select_title = 'td a.ntsviewBtn'
select_date = 'td:nth-of-type(5)'

req = requests.get(url, verify=False)
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

    title_list = i.select_one(select_title)
    title = title_list.text
    board_no = ''
    date_list = i.select_one(select_date)
    date_str = date_list.text.strip()

    print(board_no, title, date_str)

