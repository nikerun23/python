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
import sys
import chardet


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
}

# url = 'http://www.mof.go.kr/jfile/readDownloadFile.do?fileId=MOF_ARTICLE_19574&fileSeq=1'
# url = 'https://www.kitech.re.kr/upload_files/download.php?filepath=business/20180417093400.hwp&filename=%BC%AD%BD%C4+%C1%A65%C8%A3_IT%C0%B6%C7%D5%B8%C2%C3%E3+%BB%EA%BE%F7%BF%EB%BC%B6%C0%AF+%BB%FD%BB%EA%BF%AA%B7%AE%B0%AD%C8%AD%BB%E7%BE%F7+%C1%F6%BF%F8%BD%C5%C3%BB%BC%AD_%C7%D1%B1%B9%BC%B6%C0%AF%BC%F6%C3%E2%C0%D4%C1%B6%C7%D5.hwp'
url = 'http://www.molit.go.kr/LCMS/DWN.jsp?fold=tender&fileName=%EA%B3%BC%EC%97%85%EC%A7%80%EC%8B%9C%EC%84%9C%28%EC%84%B1%EC%9E%A5%EC%B4%89%EC%A7%84%EC%A7%80%EC%97%AD_%EC%9E%AC%EC%A7%80%EC%A0%95_%EB%B0%8F_%EB%82%99%ED%9B%84%EC%A7%80%EC%97%AD_%EC%A7%80%EC%9B%90%EC%B2%B4%EA%B3%84_%EA%B0%9C%EC%84%A0%EB%B0%A9%EC%95%88_%EB%A7%88%EB%A0%A8_%EC%97%B0%EA%B5%AC%29%281%29.hwp'
# url = 'http://www.msip.go.kr/cms/www/news/notice/__icsFiles/afieldfile/2018/04/13/상품판매형 방송채널사용사업 재승인 관련 시청자 의견 반영 여부 및 심사결과 공표.hwp'

response = urllib.request.urlopen(url)
file = response.read()
res_headers = response.info()['Content-Disposition']
print('res_headers :',response.headers)
if res_headers is not None:
    _, params = cgi.parse_header(response.info()['Content-Disposition'])
    filename = urllib.parse.unquote(params["filename"])  # 바이트 문자열

    print('type(filename) :',type(filename))
    try:
        filename = filename.encode('latin-1')
        filename_enc = chardet.detect(filename)['encoding']
        print('filename.encode(latin-1) :',type(filename))
    except UnicodeEncodeError:
        filename_enc = 'euc-kr'

    if 'utf-8' == filename_enc:
        filename = filename.decode('utf8')  # Binary 타입의 파일명을 utf-8로 인코딩
    elif 'EUC-KR' == filename_enc:
        filename = filename.decode('euc-kr')  # Binary 타입의 파일명을 euc-kr로 인코딩
print('filename :',filename)

download_path = 'files/2018-04-18/해양수산부/'
file_path = download_path + filename

directory = os.path.dirname(file_path)  # 폴더경로만 반환한다
if not os.path.exists(directory):
    os.makedirs(directory, exist_ok=True)  # exist_ok=True 상위 경로도 생성한다

f = open(file_path, "wb")
f.write(file)
f.close()
