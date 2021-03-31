from bs4 import BeautifulSoup
import requests
import re
import csv

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup



search_key = input("enter which you search: ")
#search_key = '서울 크로스핏'
print("search key: %s" %search_key)
full_url = "https://m.map.naver.com/search2/search.naver?query=%s" %search_key

print('start crawling : %s' %full_url)
'''
response = requests.get(full_url)
#print(response.text)

bs = BeautifulSoup(response.text, 'html.parser')
f = open('result.txt','w')
f.write(response.text)
f.close()
'''

driver = webdriver.Chrome("./chromedriver")
driver.get(full_url)

timeout = 3
try:
    element_present = EC.presence_of_element_located((By.ID, 'main'))
    WebDriverWait(driver, timeout).until(element_present)
except TimeoutException:
    print("Timed out waiting for page to load")
finally:
    print('end load!')
    time.sleep(3)
    #크롬에서 받음
    raw = driver.page_source
    soup = BeautifulSoup(raw, 'html.parser')
    list_selector ='#ct > div.search_listview._content._ctList > ul > li:nth-child(1)'
    #title = soup.select_one(list_selector)
    #title = soup.find_all('li class="_item _lazyImgContainer"')
    poi_list = soup.find_all(attrs={'class':'_item _lazyImgContainer'})

    tel_re = re.compile('data-tel=".*" data-title="')
    title_re = re.compile('data-title=".*"><div class="item_info"')
    new_address_re = re.compile('<div class="bx_address"><p>.*</p> <p><span>지번')
    old_address_re = re.compile('지번</span>.*</p></div>')
    #print(titles)
    f = open('result.txt','w')
    print('이름\t전화번호\t신주소\t구주소\n')
    f.write('이름\t전화번호\t신주소\t구주소\n')

    for poi in poi_list:
        title= str(title_re.findall(str(poi))).replace('[\'data-title="','').replace('"><div class="item_info"\']','').replace('amp;', '')
        tel = str(tel_re.findall(str(poi))).replace('[\'data-tel="','').replace('" data-title="\']','')
        new_address= str(new_address_re.findall(str(poi))).replace('[\'<div class="bx_address"><p>','').replace('</p> <p><span>지번\']','')
        old_address =str(old_address_re.findall(str(poi))).replace('[\'지번</span>','').replace('</p></div>\']','')
        print('%s\t%s\t%s\t%s' %(title,tel,new_address,old_address))
        f.write('%s\t%s\t%s\t%s\n' %(title,tel,new_address,old_address))
    f.close()




# 크롭 웹페이지를 닫음
driver.close()
