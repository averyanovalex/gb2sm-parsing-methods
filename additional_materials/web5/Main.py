from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import time

driver = webdriver.Chrome('./chromedriver.exe')
driver.get('https://api.nasa.gov/planetary/apod?api_key=AY6ihlmPkduiC2u0Cn1AfNTxYcymf1tfVgTN9eOL')



elem = driver.find_element_by_id('user_email')
elem.send_keys('study.ai_172@mail.ru')

elem = driver.find_element_by_id('user_password')
elem.send_keys('Password172')

elem.send_keys(Keys.ENTER)

time.sleep(0.9)
profile = driver.find_element_by_class_name('avatar')
profile_link = profile.get_attribute('href')
driver.get(profile_link)

edit_profile = driver.find_element_by_class_name('text-sm')
edit_profile_link = edit_profile.get_attribute('href')
driver.get(edit_profile_link)


# select = driver.find_element_by_name('user[gender]')
# options = select.find_elements_by_tag_name('option')
#
# for option in options:
#     if option.text == 'Мужской':
#         option.click()

gender = driver.find_element_by_name('user[gender]')
select = Select(gender)
select.select_by_value('0')

gender.submit()

driver.back()
driver.forward()
driver.refresh()

# driver.quit()

