
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup


#search_key = input("enter which you search: ")
search_key = '서울 크로스핏'
print("search key: %s" %search_key)

driver = webdriver.Chrome("./chromedriver")
driver.get("https://map.naver.com/v5/search")


timeout = 3
time.sleep(3)
try:
    element_present = EC.presence_of_element_located((By.ID, 'main'))
    WebDriverWait(driver, timeout).until(element_present)
except TimeoutException:
    print("Timed out waiting for page to load")
finally:
    print('end load!')
    # 팝업 창 제거
    #driver.find_element_by_css_selector("button#intro_popup_close").click()

    # 검색창에 검색어 입력하기
    search_box = driver.find_element_by_css_selector("div.input_box>input.input_search")
    search_box.send_keys(search_key)

    time.sleep(3)

    # 검색버튼 누르기
    search_box.send_keys(Keys.ENTER)

    xpath = "//*[@id=\"searchIframe\"]"
    for actualRow in driver.find_elements_by_xpath(xpath):
        thisRowsTD=actualRow[0]
        print(thisRowsTD.text)



    '''# 크롤링
    for p in range(20):
        
        #js_script = "document.querySelector(\"body > app > layout > div > div.container > div.router-output > "\
        #            "shrinkable-layout > search-layout > combined-search-list\").innerHTML"
        js_script = "document.querySelector(\"#searchIframe\")"
        


        raw = driver.execute_script("return " + js_script)
        print('raw is: %s' %raw)

        html = BeautifulSoup(raw, "html.parser")

        contents = html.select("div > div.ps-content > div > div > div .item_search")
        for s in contents:
            search_box_html = s.select_one(".search_box")

            name = search_box_html.select_one(".title_box .search_title .search_title_text").text
            print("식당명: \t" + name)
            try:
                phone = search_box_html.select_one(".search_text_box .phone").text
            except:
                phone = "NULL"
            print("전화번호: \t" + phone)
            address = search_box_html.select_one(".ng-star-inserted .roadAddress").text
            print("주소: " + address)

            print("--"*30)
        # 다음 페이지로 이동
        try:
            next_btn = driver.find_element_by_css_selector("button.btn_next")
            next_btn.click()
        except:
            print("데이터 수집 완료")
            break'''

# 크롭 웹페이지를 닫음
driver.close()
