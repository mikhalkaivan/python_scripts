from scrapy import Spider
from belmeta.items import JobItem


class JobSpider(Spider):

    name='belmeta'

    def __init__(self, category=None, location=None, *args, **kwargs):
        super(JobSpider, self).__init__(*args, **kwargs)
        self.start_urls = ["http://belmeta.com/vacansii?q=%s&l=%s" % (category, location)]

    def parse(self, response):
        jobs = response.xpath("//article[@class='job no-logo']")
        for job in jobs:
            j = JobItem()
            j["title"] = job.xpath(".//h2/a/strong/text()").extract_first()
            j["salary"] = job.xpath(".//div[@class='salary']/text()").extract_first()
            j["company"] = job.xpath(".//div[@class='company']/text()").extract_first()
            j["source"] = job.xpath(".//div[@class='from']/text()").extract_first()
            j["date"] = job.xpath(".//span[@class='days']/@data-value").extract_first()
            yield j

        next_page = response.xpath("//a[@class='next']/@href").extract_first()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)