# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

from scrapy.pipelines.images import ImagesPipeline
import scrapy
from pymongo import MongoClient


class LeroymerlinPhotosPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if item['photos']:
            for img in item['photos']:
                try:
                    yield scrapy.Request(img, meta=item)
                except Exception as e:
                    print(e)

    def file_path(self, request, response=None, info=None):
        item = request.meta
        url = request.url
        return f"{item['_id']}-{item['name'][:50]}/{url[url.rfind('/') + 1:]}"


    def item_completed(self, results, item, info):
        if results:
            item['photos'] = [itm[1] for itm in results if itm[0]]
        return item


class DataBasePipeline:

    def __init__(self):
        self.client = MongoClient('localhost', 27017)
        self.mongodb = self.client.leroymerlin

    def __del__(self):
        self.client.close()

    def process_item(self, item, spider):

        if self.mongodb['smesi'].count_documents({'_id': item['_id']}) == 0:
            self.mongodb['smesi'].insert_one(item)

        return item
