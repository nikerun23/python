import requests
from bs4 import BeautifulSoup as bs

req = requests.get('http://naver.com')
html = req.text

soup = bs(html, 'lxml')

newest_list = soup.select(
    'div.ah_list > ul.ah_l > li.ah_item > a.ah_a > span.ah_k'
)

num = 1
for i in newest_list:
    print(num, i.text)
    num += 1;