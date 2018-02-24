import requests
from bs4 import BeautifulSoup as bs

# cURL Create
headers = {
    'Origin': 'https://login.coupang.com',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.119 Safari/537.36',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Accept': '*/*',
    'Referer': 'https://login.coupang.com/login/login.pang?rtnUrl=http%3A%2F%2Fwww.coupang.com%2Fnp%2Fpost%2Flogin%3Fr%3Dhttp%253A%252F%252Fwww.coupang.com%252F',
    'X-Requested-With': 'XMLHttpRequest',
    'Connection': 'keep-alive',
}

data = [
  ('email', 'leehyunkeun@hanmail.net'),
  ('password', 'wlsldjtm23'),
  ('rememberMe', 'false'),
  ('token', ''),
  ('captchaAnswer', '')
]

s = requests.Session() # Session 객체 생성

s.headers = headers # Session 객체에 헤더 추가

s.get('https://login.coupang.com/login/login.pang') # 쿠키 채우기용 로그인 페이지 방문

ls = s.post('https://login.coupang.com/login/loginProcess.pang', data=data) # 로그인 POST 요청
print(ls.text) # 로그인 결과
print('cookies.sid :', s.cookies.get('sid'))

# 실제 크롤링할 페이지 방문
res = s.get('http://cart.coupang.com/cartView.pang')
soup = bs(res.text, 'lxml')
cartList = soup.select('tr.cart-deal-item > td.product-box > div.product-name-part > a')
print(cartList)
print('장바구니')
for i in cartList:
    print(i.text)
