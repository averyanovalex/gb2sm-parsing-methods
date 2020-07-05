from pprint import pprint
from lxml import html
import requests

header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'}

def request_to_ebay():
    response = requests.get('https://ru.ebay.com/b/Samsung-Cell-Phones-and-Smartphones/9355/bn_352130',
                            headers=header)
    dom = html.fromstring(response.text)

    phones = []
    items = dom.xpath("//ul[@class='b-list__items_nofooter']/li")
    for item in items:
        phone = {}
        name = item.xpath(".//h3[@class='s-item__title'][1]/text()")
        price = item.xpath(".//span[@class='s-item__price']/span/text()")
        image = item.xpath(".//img[@class='s-item__image-img']/@src")
        review = item.xpath(".//span[@class='s-item__reviews-count']/../@href")

        phone['name'] = name[0]
        phone['price'] = price
        phone['image'] = image[0]
        phone['review'] = review

        phones.append(phone)
    return(phones)


pprint(request_to_ebay())



