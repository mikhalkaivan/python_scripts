from scrapy.spiders import Spider, Rule
from example.items import ArticleItem


class PhysphacSpider(Spider):
    name = 'physphac'
    start_urls = [
        'http://old.gsu.by/physfac/'
    ]

    def parse(self, response):
        titles = response.xpath("//table[@class='blog']//td[@class='contentheading']/text()").extract()
        for title in titles:
            item = ArticleItem()
            item['title'] = title
            yield item

        next_page = response.xpath("//a[@title='Следующая']/@href").extract_first()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)



