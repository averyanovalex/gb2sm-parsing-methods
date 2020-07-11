import scrapy
from scrapy.http import HtmlResponse
from booksparser.items import BooksparserItem


class LabirintSpider(scrapy.Spider):
    name = 'labirint'
    allowed_domains = ['labirint.ru']
    #жанр "информационные технологии", ~1900 книг
    start_urls = ['https://www.labirint.ru/genres/2304/?page=1']

    def parse(self, response:HtmlResponse):

        with open('temp.html', 'w', encoding='utf-8') as f:
            f.write(response.text)

        next_page = response.xpath("//div[@class='pagination-next']/a/@href").extract_first()
        next_page = response.url[:response.url.find('?')] + next_page

        #stop while develop
        #if next_page[-1] == '3': return

        book_links = response.xpath("//div[@id='catalog']//a[contains(@class, 'product-title')]/@href").extract()
        for link in book_links:
            yield response.follow(link, self.parse_book)


        yield response.follow(next_page, callback=self.parse)


    def parse_book(self, response:HtmlResponse):

        href = response.url
        title = response.xpath("//h1/text()").extract_first()
        authors = response.xpath("//a[@data-event-label='author']/text()").extract()
        rate = response.xpath("//div[@id='rate']/text()").extract_first()
        genre = response.xpath("//div[@id='thermometer-books']/span/a/span/text()").extract()
        annotation = response.xpath("//h2[1]/../p/text()").extract_first()

        price = response.xpath("//span[@class='buying-priceold-val-number']/text()").extract_first()
        if price is None:
            price = response.xpath("//span[@class='buying-price-val-number']/text()").extract_first()

        special_price = response.xpath("//span[@class='buying-pricenew-val-number']/text()").extract_first()


        yield BooksparserItem(href=href, title=title, authors=authors,
                              special_price=special_price, price=price, rate=rate,
                              genre=genre, annotation=annotation)
