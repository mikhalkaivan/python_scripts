from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from example.items import TitleItem


class PhysphacSpider(CrawlSpider):
    name = 'titles'
    start_urls = [
        'http://old.gsu.by/physfac/'
    ]

    rules = (
        Rule(LinkExtractor(restrict_xpaths="//table[@class='moduletable_menu']//a"), callback="parse_titles"),
    )

    def parse_titles(self, response):
        title = TitleItem()
        t = response.xpath("//title/text()").extract_first()
        title['title'] = t
        yield title
