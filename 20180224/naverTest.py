import requests
from bs4 import BeautifulSoup as bs

req = requests.get('https://www.naver.com/')
soup = bs(req.text, 'lxml')
naverList = soup.select_one('#PM_ID_serviceNavi > li:nth-of-type(4) > a > span.an_txt')
naverList2 = soup.select('#PM_ID_serviceNavi > li:nth-of-type(4) > a > span.an_txt')
print(type(naverList))
print(type(naverList2))
print(naverList2[0].text)
print(naverList.text)