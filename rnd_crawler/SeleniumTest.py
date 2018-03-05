from selenium import webdriver

driver = webdriver.Chrome('./chromedriver')

url = 'http://www.nipa.kr/board/boardList.it?boardNo=102&menuNo=31&page=1'
click_css = {'#container > div.leftWrap > div.snb > ul > li:nth-of-type(2) > a',
             '#container > div.leftWrap > div.snb > ul > li:nth-of-type(4) > a'}
select_tr = '#q_content table > tbody > tr'
select_title = 'td.title a'
select_date = 'td.date'

driver.get(url)
for click in click_css:
    driver.find_element_by_css_selector(click).click()
board_list = driver.find_elements_by_css_selector(select_tr)

for tr in board_list:
    title = tr.find_element_by_css_selector(select_title)
    print(title.text)
    date = tr.find_element_by_css_selector(select_date)
    print(date.text)

driver.quit()

