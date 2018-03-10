import requests
from bs4 import BeautifulSoup as bs

url = 'http://www.msip.go.kr/web/msipContents/contents.do?mId=MTE3'
select_tr = 'div.board-list table > tbody > tr'
select_title = 'td.title span'
select_date = 'td span.date'

req = requests.get(url)
# req.encoding = 'utf-8'
# req.encoding = 'euc-kr'
html = req.text
# print(html)
soup = bs(html, 'lxml')
board_list = soup.select(
    select_tr
)
print(board_list)
for i in board_list:

    title_list = i.select_one(select_title)
    title = title_list.text
    board_no = ''
    date_list = i.select_one(select_date)
    date_str = date_list.text

    print(board_no, title, date_str)

