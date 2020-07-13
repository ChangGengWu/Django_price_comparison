import os
from selenium import webdriver
import requests
from time import sleep
import time
from bs4 import BeautifulSoup
from selenium import webdriver
import datetime
import sys
# upper = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
# a = upper+'\models.py'
# sys.path.append(upper+'\models.py')

from polls.models import Product_info
keyword = "pixel4"

pchome_url = "https://ecshweb.pchome.com.tw/search/v3.3/?q="+ keyword +"%204&scope=all&sortParm=rnk&sortOrder=dc"
momo_url = "https://www.momoshop.com.tw/search/searchShop.jsp?keyword=" + \
    keyword + "&searchType=6"

#取得檔案位置
DIR_NAME = os.path.dirname(os.path.abspath(__file__))
print(DIR_NAME)
#開啟driver
# driver = webdriver.Chrome(executable_path=DIR_NAME+'/chromedriver')

# #Get item price in pchome
driver.get(pchome_url)
sleep(2)
i = 0
prod_id = ""
d1 = driver.find_elements_by_tag_name('dl')
for items in d1:
        if i == 1:
            break
        else:
            if items.get_attribute("id") != "":
                prod_id = items.get_attribute("id")
                i += 1
price_path = "//div[@id='ItemContainer']/dl[@id='" + prod_id + "']/dd[3]/ul/li/span/span"
price = driver.find_element_by_xpath(price_path)

pc_price = price.get_attribute('textContent')
pc_crawDate = datetime.date.today()
#Get item price in momo
driver.get(momo_url)
sleep(2)
# price_path = "//div[contains(@class, 'listArea')]/ul/li"
# price = driver.find_element_by_xpath(price_path)
soup = BeautifulSoup(driver.page_source, "html.parser")
item_list = soup.find_all('div', class_='listArea')
item_content = str(item_list)
soup2 = BeautifulSoup(item_content, "html.parser")
price = soup2.find('span',class_='price')

momo_price = (str(price.text).replace("$", "")).replace(",", "")
momo_crawDate = datetime.date.today()

Product_info.object.create(p_name="Pixel4", p_price=pc_price, p_site="PChome")
print(pc_price,pc_crawDate)
print(momo_price,momo_crawDate)
    

