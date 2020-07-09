"""
2) Написать программу, которая собирает «Хиты продаж» с сайта техники mvideo и складывает данные в БД.
Магазины можно выбрать свои. Главный критерий выбора: динамически загружаемые товары
"""

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import time
import json
from pymongo import MongoClient


driver = webdriver.Chrome('./chromedriver.exe')
driver.get('https://www.mvideo.ru/')

time.sleep(1)


#находим нужный блок-карусель (block). Однозначного атриббута у тега нет, поэтому ищем по xpath и тексту заголовка
block = None
elems = driver.find_elements_by_xpath("//div[@data-init='gtm-push-products']")
for elem in elems:
    if elem.find_element_by_tag_name('div').text == 'Хиты продаж':
        block = elem

        #позиционируюмся на найденный блок (скроллим страницу туда)
        #если этого не сделать, почему-то не срабатывает позиционирование на кнопку "Дальше" в этом блоке
        actions = ActionChains(driver)
        actions.move_to_element(block)
        actions.perform()

        break

#каждый раз при нажатии "Дальше" в наш блок-карусель догружаются новые товары, но отображается лишь часть
#поэтому сначала заполняем блок всеми товарами (жмем кнопку пока товары догружаются), потом оптом парсим товары
total_items_count = 0
while True:
    elems = block.find_elements_by_class_name('gallery-list-item')

    button = block.find_element_by_class_name('sel-hits-button-next')
    if len(elems) != total_items_count:
        total_items_count =  len(elems)

        actions = ActionChains(driver)
        actions.move_to_element(button)
        actions.click(button)
        actions.perform()

    else:
        break

    time.sleep(5)


#все, теперь парсим эти товары

client = MongoClient('localhost', 27017)
mongodb = client['mvideo'].hits

count_added = 0
for elem in elems:
    item_block = elem.find_element_by_tag_name('a')

    #в одном атрибуте лежит удобный json с нужной информацией, воспользуемся этим
    raw_item_info = json.loads(item_block.get_attribute('data-product-info').replace('\n', ''))
    item_info = {'_id' : raw_item_info['productId'],
              'productName' : raw_item_info['productName'],
              'price' : float(raw_item_info['productPriceLocal'])}

    if mongodb.count_documents({'_id': item_info['_id'] }) == 0:
        mongodb.insert_one(item_info)
        count_added +=1
        print('added: ', count_added)



driver.quit()