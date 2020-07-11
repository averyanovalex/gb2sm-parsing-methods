# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

from pymongo import MongoClient


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

            if self.mongodb.labirint.count_documents({'_id': item['_id']}) == 0:
                self.mongodb.labirint.insert_one(item)



        return item
