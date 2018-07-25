import requests
from bs4 import BeautifulSoup as bs
from selenium import webdriver
import time

options = webdriver.ChromeOptions()
options.add_argument("--disable-extensions")
options.add_argument("--start-maximized")
driver = webdriver.Chrome('./chromedriver', chrome_options=options)

driver.get('http://www.ntis.go.kr/ThMain.do')
time.sleep(1)
driver.find_element_by_css_selector('#userid').send_keys('hoon1234')
driver.find_element_by_css_selector('#password').send_keys('gate4fkd!!')
driver.find_element_by_css_selector('#logIn').click()
time.sleep(1)

driver.get('http://www.ntis.go.kr/rndgate/eg/un/ra/myAncmMng.do')
driver.find_element_by_css_selector('#myRndForm div.table_option > a').click()

