from selenium import webdriver
import time


def daily_point(login_id, login_pw):
    print(login_id, login_pw, ' RUN !!!')
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # 헤드리스모드
    options.add_argument('--disable-gpu')  # 호환성용 (필요없는 경우도 있음)
    options.add_argument('--window-size=1920x1080')  # (가상)화면 크기 조절
    options.add_argument('--no-sandbox')
    driver = webdriver.Chrome(chrome_options=options)
    # driver = webdriver.Chrome('./chromedriver')
    driver.set_page_load_timeout(60)  # selenium timeout 60초
    login_url = 'https://memberssl.auction.co.kr/Authenticate/default.aspx?url=http%3A//promotion.auction.co.kr/promotion/MD/eventview.aspx%3FtxtMD%3D05F804C1E8'
    try:
        driver.get(url=login_url)

        time.sleep(5)
        driver.find_element_by_css_selector('#id').send_keys(login_id)
        driver.find_element_by_css_selector('#password').send_keys(login_pw)
        time.sleep(1)
        driver.find_element_by_css_selector('#Image1').click()
        time.sleep(5)
        driver.get('http://eventv2.auction.co.kr/event3/Regular/EverydayPoint/IfrmMainContents.aspx')
        time.sleep(5)

        for index in range(1,7):
            event_list = driver.find_elements_by_css_selector('div.swiper-slide-visible a.btn_point')
            for bt in event_list:
                if '적립하러' in bt.text:
                    time.sleep(1)
                    bt.click()
                    time.sleep(1)
                    alert = driver.find_element_by_css_selector('.ly_msg_box p.txt')
                    if '지급된' in alert.text:
                        driver.refresh()
                        time.sleep(3)
                        break
                    driver.find_element_by_css_selector('.btn_type').click()
                    time.sleep(3)
                    tabs = driver.window_handles
                    driver.switch_to.window(tabs[1])
                    driver.close()
                    driver.switch_to.window(tabs[0])
                    time.sleep(3)

            driver.find_element_by_css_selector('.swiper-button-next').click()
            time.sleep(2)
    except Exception as e:
        print(e)
    finally:
        driver.close()


if '__main__' == __name__:
    

