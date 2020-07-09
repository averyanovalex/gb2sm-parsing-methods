from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains


chrome_options = Options()
import time

chrome_options.add_argument('start-maximized')
driver = webdriver.Chrome(options=chrome_options)
driver.get('https://pikabu.ru/')


for i in range(5):
    time.sleep(3)
    articles = driver.find_elements_by_tag_name('article')
    if articles[-1] != last_article:
        last_article = articles[-1]
        actions = ActionChains(driver)
        actions.move_to_element(articles[-1])   #.key_down(Keys.CTRL).key_down(Keys.ENTER).key_up(Keys.Enter)
        actions.perform()









# from selenium.webdriver.common.action_chains import ActionChains
#
# chrome_options = Options()
# import time
# chrome_options.add_argument('start-maximized')
#
# driver = webdriver.Chrome(options=chrome_options)
#
# driver.get('https://pikabu.ru/')
#
# for i in range(5):
#     time.sleep(5)
#     articles = driver.find_elements_by_tag_name('article')
#     actions = ActionChains(driver)
#
#     actions.move_to_element(articles[-1])
#     actions.perform()