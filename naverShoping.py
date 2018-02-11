import requests
from bs4 import BeautifulSoup as bs

req = requests.get('https://search.shopping.naver.com/detail/detail.nhn?cat_id=50002334&nv_mid=12675036195&query=%EC%95%84%EC%9D%B4%EC%BD%98+%EA%B8%B0%EC%96%B4+2018&frm=NVSCPRO')
html = req.text

soup = bs(html, 'lxml')
lowPrice = soup.select(
    '#_mainSummaryPrice span.low_price > .num'
)

priceNum = lowPrice[0].text.replace(',', '')
priceTarget = 200000

print('현재 가격 :', priceNum)
if int(priceNum) >= priceTarget:
    print('최저가가 아닙니다.')
else:
    print('최저가입니다.')
