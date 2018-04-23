# -*- coding: utf-8 -*-
import rnd_crawler.utility as util
import re
from bs4 import BeautifulSoup as bs
import requests
from urllib.request import urlretrieve
from urllib.request import urlopen
import urllib
import os
import cgi
import unicodedata

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
}

url = 'http://www.mof.go.kr/jfile/readDownloadFile.do?fileId=MOF_ARTICLE_19574&fileSeq=1'

print('url :', url)
# response = requests.get(url, stream=True, headers=headers)
filename = 'TEST2.hwp'

response = urllib.request.urlopen(url)
# # urlretrieve(url, file_path)
csv = response.read()
# print(response)
# print(urlopen(url).info())
print(type(csv))
res_headers = response.info()['Content-Disposition']
if res_headers is not None:
    value, params = cgi.parse_header(response.info()['Content-Disposition'])
    print(params["filename"])
    filename = urllib.parse.unquote(params["filename"]).encode('latin-1').decode('utf-8')
    print(type(filename))
print('filename :',filename)

download_path = 'files/2018-04-18/해양수산부/'
file_path = download_path + filename

directory = os.path.dirname(file_path)  # 폴더경로만 반환한다
if not os.path.exists(directory):
    os.makedirs(directory, exist_ok=True)  # exist_ok=True 상위 경로도 생성한다

f = open(file_path, "wb")
f.write(csv)
f.close()



# download_path = 'files/2018-04-16/해양수산부/'
# filename = 'TEST.hwp'
# file_path = download_path + filename
#
# directory = os.path.dirname(file_path)  # 폴더경로만 반환한다
# if not os.path.exists(directory):
#     os.makedirs(directory, exist_ok=True)  # exist_ok=True 상위 경로도 생성한다
#

# print(type(response))
# f = open(file_path, "wb")
# for chunk in response.iter_content(chunk_size=1024):
#     if chunk:
#         f.write(chunk)
# f.close()

# filename = re.findall("[^/]*$", url)[0]
# print('filename :', filename)