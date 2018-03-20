import requests
from bs4 import BeautifulSoup as bs
import rnd_crawler.utility as util


url = 'http://www.molit.go.kr/USR/tender/m_83/mng.jsp?SECTION=용역&ID=27368&lcmspage=1&TYPE=VIEW&HOMEPAGENAME=1613000&sTENDERDAY=&eTENDERDAY=&srch_consname=&CONDITION_VAL=&ViewPageCount=15'

csv_info = {'content_Title': '#board-view > tbody > tr:nth-of-type(1) > td > p',
            'content_WriteDate': '#board-view > tbody > tr:nth-of-type(2) > td > p',
            'content_StartDate': 'NoDate',
            'content_EndDate': '#board-view > tbody > tr:nth-of-type(5) > td:nth-of-type(2) > p',
            'content_Body': '#board-view > tbody > tr:nth-of-type(1) > td > p	',
            'content_Files': 'NoDate'
            }

select_list = [
    csv_info['content_Title'],
    csv_info['content_WriteDate'],
    csv_info['content_StartDate'],
    csv_info['content_EndDate'],
    csv_info['content_Body'],
    csv_info['content_Files']
]
req = requests.get(url)
soup = bs(req.text, 'lxml')

# print(req.text)

result_list = []
try:
    for index,s in enumerate(select_list):
        if 'NoDate' != s and '' != s:
            if 4 == index:  # csv_info['content_Body']
                html = soup.select_one(s).contents
            elif index in (1,2,3):  # Date
                html = util.valid_date(soup.select_one(s).text, None).strftime('%Y-%m-%d')
            else:
                html = soup.select_one(s).text
        else:
            html = 'NoDate'
        result_list.append(html)
except Exception as e:
    print(e)
    print('########## get_board_content 예외발생 !!')

for r in result_list:
    print(r)

