import scrapy


class CryptoslateSpider(scrapy.Spider):
    name = 'cryptoslate'
    allowed_domains = ['www.cryptoslate.com']
    start_urls = ['http://www.cryptoslate.com/']

    custom_settings = {
        "MONGO_URI":"mongodb://localhost:27017/",
        "MONGO_DATABASE":"cryptoslate",
        "MONGO_COLLECTION_NAME":"news_articles",
        "ITEM_PIPELINES":{"blockchain_scrapers.pipelines.MongoDBScrapersPipeline":300},
        "TWISTED_REACTOR": "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
    }
    def parse(self, response):
        yield {
            "title": response.xpath('//title').get(),
            "nothing":None
        }

