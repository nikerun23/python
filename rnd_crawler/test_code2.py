# -*- coding: utf-8 -*-
import rnd_crawler.utility as util
import re
from bs4 import BeautifulSoup as bs
import requests
from urllib.request import urlretrieve
from urllib.request import urlopen
import os
import cgi

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
}

url = 'http://www.mof.go.kr/jfile/readDownloadFile.do?fileId=MOF_ARTICLE_19574&fileSeq=1'

print('url :', url)
response = requests.get(url, stream=True, headers=headers)

download_path = 'files/2018-04-16/해양수산부/'
filename = 'TEST.hwp'
file_path = download_path + filename

directory = os.path.dirname(file_path)  # 폴더경로만 반환한다
if not os.path.exists(directory):
    os.makedirs(directory, exist_ok=True)  # exist_ok=True 상위 경로도 생성한다

# urlretrieve(url, file_path)
response = urlopen(url)
csv = response.read()
print(response)
print(csv)
response.encoding = 'utf-8'
_, params = cgi.parse_header(response.headers.get('Content-Disposition', ''))
filename = params

print(filename)

# f = open(filename, "wb")
# for chunk in response.iter_content(chunk_size=1024):
#     if chunk:
#         f.write(chunk)


# filename = re.findall("[^/]*$", url)[0]
# print('filename :', filename)