import scrapy
from scrapy.http import HtmlResponse
from leruaparser.items import LeruaparserItem
from scrapy.loader import ItemLoader


class LeroymerlinruSpider(scrapy.Spider):
    name = 'leroymerlinru'
    allowed_domains = ['leroymerlin.ru']


    def __init__(self, search):
        self.start_urls = [f'https://leroymerlin.ru/search/?q={search}']


    def parse(self, response: HtmlResponse):

        # debug: stop while develop
        #if response.url[-1] == '2':
        #    return

        item_links = response.xpath("//div[@class='product-name']/a")
        for link in item_links:
            yield response.follow(link, callback=self.parse_item)


        next_page = response.xpath("//a[contains(@class, 'next-paginator-button')]")
        yield response.follow(next_page[0], callback=self.parse)


    def parse_item(self, response: HtmlResponse):

        loader = ItemLoader(item=LeruaparserItem(), response=response)
        loader.add_xpath("name", "//h1[@itemprop='name']/text()")
        loader.add_value('url', response.url)
        loader.add_value('_id', response.url)
        loader.add_xpath('description', "//section[@id='nav-description']//p")
        loader.add_xpath('price', "//span[@slot='price']/text()")
        loader.add_xpath('photos', "//picture[@slot='pictures']/source[1]/@srcset")
        loader.add_xpath('properties', "//div[@class='def-list__group']")
        yield loader.load_item()


