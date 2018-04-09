import requests
from bs4 import BeautifulSoup as bs
import re
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'
}
html = requests.get('https://search.naver.com/search.naver?query=deepmind+pdf', headers=headers).text

# print(html)
soup = bs(html, 'lxml')
pdfs = soup.select('a[href$=".pdf"]')
for pdf in pdfs:
    url = pdf['href']
    print('url :',url)
    response = requests.get(url, stream=True)
    filename = re.findall("[^/]*$", url)[0]
    print('filename :',filename)
# 링크들에 들어가기 URL서 파일 이름 찾기
filename = 'pdf/'+filename
f = open(filename, "wb")
for chunk in response.iter_content(chunk_size=1024):
    if chunk:
        f.write(chunk)


