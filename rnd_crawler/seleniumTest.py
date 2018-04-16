from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import rnd_crawler.utility as util


options = webdriver.ChromeOptions()
options.add_argument("--disable-extensions")
options.add_argument("--start-maximized")
driver = webdriver.Chrome('./chromedriver', chrome_options=options)

url = 'http://www.kiost.ac.kr/cop/bbs/BBSMSTR_000000000074/selectBoardList.do'
click_css = {}
select_tr = '#content tbody > tr'
select_title = 'td:nth-of-type(2) a'
select_date = 'td:nth-of-type(3)'

try:
    driver.get(url)
    time.sleep(5)
    for css in click_css:
        driver.find_element_by_css_selector(css).click()
        time.sleep(5)
    board_list = driver.find_elements_by_css_selector(select_tr)
    print(board_list)
    for tr in board_list:
        title = tr.find_element_by_css_selector(select_title)
        print(title.text)
        date = tr.find_element_by_css_selector(select_date)
        date_str = util.valid_date(date.text, 'YYYY.MM.DD')
        print(date_str)
except AttributeError:
    print('########## Selenium 작동이 중지 되었습니다')
finally:
    driver.quit()

# WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, css)))

