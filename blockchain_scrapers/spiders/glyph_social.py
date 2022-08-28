import scrapy


class GlyphSocialSpider(scrapy.Spider):
    name = 'glyph_social'
    allowed_domains = ['www.glyph.social']
    start_urls = ['http://www.glyph.social/']

    custom_settings = {
        "MONGO_HOST":"localhost",
        "MONGO_PORT":'27017',
        "MONGO_DB_NAME":"glyph_social",
        "MONGO_COLLECTION_NAME":"company_records",
    }
    def parse(self, response):
        pass
