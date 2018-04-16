# -*- coding: utf-8 -*-
import rnd_crawler.utility as util
import re
from bs4 import BeautifulSoup as bs

html = "<a>해양수산부 <script>수립 연구 용역 입찰공고</script> </a>"
soup = bs(html, 'lxml')
soup.script.extract()
print(soup)

