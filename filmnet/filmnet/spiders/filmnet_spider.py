import scrapy


class FilmnetSpiderSpider(scrapy.Spider):
    name = "filmnet_spider"
    allowed_domains = ["filmnet.ir"]
    start_urls = ["https://filmnet.ir/"]

    def parse(self, response):
        pass
