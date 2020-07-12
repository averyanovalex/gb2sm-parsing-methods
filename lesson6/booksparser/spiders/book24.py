import scrapy
from scrapy.http import HtmlResponse
from booksparser.items import BooksparserItem


class Book24Spider(scrapy.Spider):
    name = 'book24'
    allowed_domains = ['book24.ru']
    #https://book24.ru/search/?q=программирование
    start_urls = ['https://book24.ru/search/?q=%D0%BF%D1%80%D0%BE%D0%B3%D1%80%D0%B0%D0%BC%D0%BC%D0%B8%D1%80%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5']

    def parse(self, response):

        next_page = response.xpath("//div[contains(@class, 'catalog-pagination__list')]/a[text()='Далее']/@href")\
                            .extract_first()

        # stop while develop
        #if next_page[13] == '3': return

        book_links = response.xpath("//div[@class='book__title ']/a/@href").extract()
        for link in book_links:
            yield response.follow(link, self.parse_book)

        if next_page is None:
            return
        else:
            yield response.follow(next_page, callback=self.parse)


    def parse_book(self, response:HtmlResponse):

        href = response.url
        title = response.xpath("//h1/text()").extract_first()

        if response.xpath("//div[@class='item-tab__chars-list']/div[1]/span/text()").extract_first() == 'Автор:':
            authors = response.xpath("//div[@class='item-tab__chars-list']/div[1]//a/text()").extract()
        else:
            authors = None

        rate = response.xpath("//div[@class='rating']//span[@class='rating__rate-value']/text()").extract_first()
        genre = response.xpath("//div[@class='breadcrumbs__list']/div/a/text()").extract()
        annotation = response.xpath("//div[@class='text-block-d']/p/text()").extract()
        price = response.xpath("//div[@class='item-actions__price-old']/text()").extract_first()
        special_price = response.xpath("//div[@class='item-actions__price']/b/text()").extract_first()


        yield BooksparserItem(href=href, title=title, authors=authors,
                              special_price=special_price, price=price, rate=rate,
                              genre=genre, annotation=annotation)

