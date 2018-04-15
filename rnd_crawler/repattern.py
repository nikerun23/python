import re
import requests
from bs4 import BeautifulSoup as bs


req = requests.get('http://post.naver.com/viewer/postView.nhn?volumeNo=14174358&memberNo=34218501&mainMenu=CARGAME')

html = req.text
# print(html)
soup = bs(html, 'lxml')

comment_list = soup.select('div.se_component_wrap')

# print(comment_list[0].text)

header_pattern = re.compile('<h3.*>.*<\/h3>')
date_pattern = re.compile('\d{4}-\d{2}-\d{2}')

header_str = header_pattern.findall(comment_list[0].text)
date_str = date_pattern.findall(comment_list[0].text)

# print(header_str, date_str)

