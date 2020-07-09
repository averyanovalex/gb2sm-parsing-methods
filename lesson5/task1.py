"""Написать программу, которая собирает входящие письма из своего или тестового почтового ящика
и сложить данные о письмах в базу данных (от кого, дата отправки, тема письма, текст письма полный)
Логин тестового ящика: study.ai_172@mail.ru
Пароль тестового ящика: NextPassword172"""

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
from pymongo import MongoClient


def get_id_from_link(link: str):
    return link[26:link.find('?') - 3]



#ограничение количества писем для парсинга на период отладки
#если None, то отключено
DEBUG_LETTERS_TO_PARSE_COUNT = None


#подключаем MongoDB
client = MongoClient('localhost', 27017)
mongodb = client['emails']


#логинимся в почту
driver = webdriver.Chrome('./chromedriver.exe')
driver.get('https://account.mail.ru/login')

time.sleep(1)

elem = driver.find_element_by_name('username')
elem.send_keys('study.ai_172@mail.ru')
elem.send_keys(Keys.ENTER)

time.sleep(1)

elem = driver.find_element_by_name('password')
elem.send_keys('NextPassword172')
elem.send_keys(Keys.ENTER)

time.sleep(15)

letter_links = set()
last_letter = None

#собираем заголовки на все письма в папке входящих
count = DEBUG_LETTERS_TO_PARSE_COUNT
while True:

    if (count is not None) and (count <= 0): break

    time.sleep(3)
    letters = driver.find_elements_by_class_name('js-letter-list-item')

    for letter in letters:
        letter_links.add(letter.get_attribute('href'))
        if (count is not None):
            count -= 1
            if  count <= 0: break

    if len(letters) > 0 and letters[-1] != last_letter:
        last_letter = letters[-1]
        actions = ActionChains(driver)
        actions.move_to_element(last_letter)
        actions.perform()
    else:
        break

print('Letters: ', len(letter_links))


count_added = 0
count_skipped = 0
for link in letter_links:

    if mongodb.mail_ru.count_documents({'_id': get_id_from_link(link)}) != 0:
        #пропускаем, если такое письмо уже парсили раньше
        count_skipped += 1
        print(f'Letters skipped: {count_skipped}')
        continue

    driver.get(link)

    time.sleep(15)

    elem = driver.find_element_by_class_name('letter-contact')
    from_mail = elem.get_attribute('title')
    from_author = elem.text

    elem = driver.find_element_by_class_name('letter__date')
    datetime = elem.text

    elem = driver.find_element_by_class_name('thread__subject')
    subject = elem.text

    elem = driver.find_element_by_class_name('letter__body')
    body = elem.text

    letter_dict = {'_id' : get_id_from_link(link),
                   'from_mail' : from_mail,
                   'from_author' : from_author,
                   'datetime' : datetime,
                   'subject' : subject,
                   'text' : body}


    #складываем письмо в mongodb
    mongodb.mail_ru.insert_one(letter_dict)
    count_added += 1
    print(f'Letters added: {count_added}')





driver.quit()