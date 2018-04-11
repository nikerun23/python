from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time


options = webdriver.ChromeOptions()
options.add_argument("--disable-extensions")
options.add_argument("--start-maximized")
driver = webdriver.Chrome('./chromedriver', chrome_options=options)

url = 'https://www.nrf.re.kr/biz/notice/list?search_type=ALL&page=1'
click_css = '#submenu > div.sub_list > ul > li:nth-child(1) > a'
select_tr = '#DIV_LIST > table > tbody > tr'
select_title = 'td:nth-of-type(3) a'
select_date = 'td:nth-of-type(5)'

try:
    driver.get(url)
    time.sleep(3)
    driver.find_element_by_css_selector(click_css).click()
    time.sleep(3)
    # board_list = driver.find_elements_by_css_selector(select_tr)
    # board_list = board_list[1:]
    # for tr in board_list:
    #     title = tr.find_element_by_css_selector(select_title)
    #     print(title.text)
    #     date = tr.find_element_by_css_selector(select_date)
    #     print(date.text)
except Exception:
    print('########## Selenium 작동이 중지 되었습니다')
# finally:
    # driver.quit()


# WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, css)))
