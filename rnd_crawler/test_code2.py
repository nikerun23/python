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

# url = 'http://www.mof.go.kr/jfile/readDownloadFile.do?fileId=MOF_ARTICLE_19574&fileSeq=1'
url = 'http://www.molit.go.kr/LCMS/DWN.jsp?fold=tender&amp;fileName=%EA%B3%BC%EC%97%85%EC%A7%80%EC%8B%9C%EC%84%9C%28%EC%95%84%ED%94%84%EB%A6%AC%EC%B9%B4_%EC%9D%B8%ED%94%84%EB%9D%BCODA_%EC%A7%80%EC%9B%90%EC%A0%84%EB%9E%B5_%EC%88%98%EB%A6%BD_%EB%B0%8F_%EC%82%AC%EC%97%85%EA%B8%B0%ED%9A%8D_%EC%A1%B0%EC%82%AC%EC%97%B0%EA%B5%AC%29.hwp'
url = 'http://www.moel.go.kr/common/downloadFile.do;jsessionid=yzeEOrtFwzAVcw9uhzRL50kwdruAHMI4hbXHVIZ4A4z1U3fJ0y6fJox6FmIHv0MN.moel_was_outside_servlet_www1?file_seq=20180700242&bbs_seq=20180700095&bbs_id=9'
filename = 'TEST2.hwp'

print('url :', url)
# response = requests.get(url, stream=True, headers=headers)

response = urllib.request.urlopen(url)
# # urlretrieve(url, file_path)
csv = response.read()
# print(response)
# print(urlopen(url).info())
# print(type(csv))
res_headers = response.info()['Content-Disposition']
if res_headers is not None:
    value, params = cgi.parse_header(response.info()['Content-Disposition'])
    print('params["filename"]: ',params["filename"])
    filename = urllib.parse.unquote(params["filename"])  # 바이트 문자열
    # filename = urllib.parse.unquote(params["filename"]).encode('latin-1').decode('utf-8')
    print(type(filename))
print('filename :',filename)

download_path = 'files/2018-04-27/해양수산부/'
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