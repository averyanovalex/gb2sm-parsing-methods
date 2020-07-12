# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

from pymongo import MongoClient
from _datetime import datetime


class BooksparserPipeline:

    def __init__(self):
        self.client = MongoClient('localhost', 27017)
        self.mongodb = self.client.books

    def __del__(self):
        self.client.close()


    def process_item(self, item, spider):

        if spider.name == 'labirint':

            id_temp = item['href'][:-1]
            item['_id'] = id_temp[id_temp.rfind('/')+1:]

            item['title'] = item['title'][item['title'].find(':')+2:]
            item['authors'] = ', '.join(item['authors'])
            item['special_price'] = None if item['special_price'] is None else int(item['special_price'])
            item['price'] = None if item['price'] is None else int(item['price'])
            item['rate'] = float(item['rate'])

        elif spider.name == 'book24':

            item['_id'] = item['href'][item['href'].rfind('-')+1:-1]
            item['authors']  = None if item['authors'] is None else ', '.join(item['authors'])
            item['rate'] = None if item['rate'] is None else float(item['rate'].replace(',', '.'))
            item['genre'] = item['genre'][1:]
            item['annotation'] = None if len(item['annotation']) == 0 else '\n'.join(item['annotation'])
            item['special_price'] = None if item['special_price'] is None else int(item['special_price'].replace(' ', ''))
            item['price'] = item['special_price'] if item['price'] is None else int(item['price'][:-3].replace(' ', ''))

        if self.mongodb[spider.name].count_documents({'_id': item['_id']}) == 0:
            item['added_at'] = datetime.now()
            self.mongodb[spider.name].insert_one(item)

        return item
