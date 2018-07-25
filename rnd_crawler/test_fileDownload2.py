# -*- coding: utf-8 -*-

from selenium import webdriver
import time
import os
import uuid


if '__main__' == __name__:
    file_info = {}
    file_info['url'] = 'http://www.nrf.re.kr/biz/notice/view?nts_no=106288&menu_no=&biz_no=&search_type=ALL&search_keyword=&page=1'
    # file_info['url'] = 'https://www.nims.re.kr/noticeYard/post/bidding/32895'
    # file_info['css'] = '#container > div.content_body > div.board_file > ul > li > a'
    file_info['css'] = '#container > section > div > div.board_view > div:nth-of-type(3) > div > form > a'
    download_path = 'C:/FILE/TEST/20180724/'




    try:
        options = webdriver.ChromeOptions()
        # 헤드리스모드
        # options.add_argument('--headless')
        # options.add_argument('--disable-gpu')  # 호환성용 (필요없는 경우도 있음)
        # options.add_argument('--window-size=1920x1080')  # (가상)화면 크기 조절
        # options.add_argument("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36")
        options.add_experimental_option("prefs", {
            "download.default_directory": download_path,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True
        })

        driver = webdriver.Chrome(chrome_options=options)
        driver.set_page_load_timeout(60)  # selenium timeout 60초

        driver.get(file_info['url'])
        time.sleep(3)
        file_list = driver.find_elements_by_css_selector(file_info['css'])
        file_size = 0

        for file in file_list:
            file_info['uid_file_name'] = str(uuid.uuid4())

            uid_file_name = file_info['uid_file_name']
            file_path = download_path + uid_file_name
            print('file_path :', file_path)
            directory = os.path.dirname(file_path)  # 폴더경로만 반환한다
            if not os.path.exists(directory):
                os.makedirs(directory, exist_ok=True)  # exist_ok=True 상위 경로도 생성한다

            time.sleep(1)
            file.click()  # 다운로드 시작
            file_name = file.text
            print('file_name :', file_name)
            time.sleep(10)

            # 최근에 받은 파일명을 반환한다
            download_name = max([f for f in os.listdir(download_path)],
                                key=lambda xa: os.path.getctime(os.path.join(download_path, xa)))
            print('download_name :', download_name)

            old_name = os.path.join(download_path, download_name)
            new_name = os.path.join(download_path, uid_file_name)
            os.rename(old_name, new_name)  # 파일명을 uuid로 변경

            time.sleep(1)
            file_size = os.path.getsize(file_path)
            print('file_size :', file_size)
    except Exception as e:
        print(e)
    finally:
        driver.close()

