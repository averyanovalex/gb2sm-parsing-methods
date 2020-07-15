# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst, Join
from w3lib.html import remove_tags


def process_price(value:str):
    if value:
        return float(value.replace(' ', '').replace(',', '.'))


def process_id(value: str):
    return int(value[value.rfind('-')+1:-1])


def process_property(value: str):

    key_index1 = value.find('<dt class="def-list__term">') + 27
    key_index2 = value.find('</dt>')
    key = value[key_index1:key_index2]

    val_index1 = value.find('<dd class="def-list__definition">') + 33
    val_index2 = value.find('</dd>')
    val = value[val_index1:val_index2].strip()

    #если val - правильное число, преобразуем к числу
    if val:
        try:
            val = float(val)
        except:
            pass

    return {key : val}


class LeruaparserItem(scrapy.Item):
    # define the fields for your item here like:
    _id = scrapy.Field(input_processor=MapCompose(process_id), output_processor=TakeFirst())
    name = scrapy.Field(output_processor=TakeFirst())
    url = scrapy.Field(output_processor=TakeFirst())
    description = scrapy.Field(input_processor=MapCompose(remove_tags), output_processor=Join())
    price = scrapy.Field(input_processor=MapCompose(process_price), output_processor=TakeFirst())
    photos = scrapy.Field()
    properties = scrapy.Field(input_processor=MapCompose(process_property))

