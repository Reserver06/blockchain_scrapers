import re
from scrapy.spiders import SitemapSpider
from ..items import GlyphSocialItem
from ..utils.stash_webpage import stash_webpage
from dataclasses import asdict


class GlyphSocialSpider(SitemapSpider):
    name = "glyph_social"
    sitemap_urls = ["https://www.glyph.social/sitemap.xml"]
    sitemap_rules = [(r"\/companies\/\w+", "parse")]
    custom_settings = {
        "MONGO_URI": "mongodb://localhost:27017/",
        "MONGO_DATABASE": "glyphsocial",
        "MONGO_COLLECTION_NAME": "company_records",
        "ITEM_PIPELINES": {
            "blockchain_scrapers.pipelines.MongoDBScrapersPipeline": 300
        },
        "TWISTED_REACTOR": "twisted.internet.asyncioreactor.AsyncioSelectorReactor",
        "USER_AGENT": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36",
        "DOWNLOAD_DELAY": 3,
    }

    def __init__(self, company=None, *args, **kwargs):
        if company:
            self.sitemap_rules = [(f"\/companies\/{company}", "parse")]

        super(GlyphSocialSpider, self).__init__(*args, **kwargs)

    def parse(self, response):
        item = {}

        stash_webpage(response)

        # Url
        item["url"] = response.url

        # Legal Name
        item["legal_name"] = response.xpath(
            '//ul[@class="list-3 w-list-unstyled"]/li[@class="list-item-2"]/text()'
        ).get()

        # Category
        item["category"] = response.xpath(
            '//div[@class="products__category"]/text()'
        ).get()

        # Headquarters
        item["headquarters"] = response.xpath(
            '//ul[@class="list-3 w-list-unstyled"]/li[@class="list-item-3"]/text()'
        ).get()

        # Founding Year
        item["founding_year"] = response.xpath(
            '//ul[@class="list-3 w-list-unstyled"]/li[@class="list-item-4"]/text()'
        ).get()

        # Founding Team
        item["founding_team"] = ", ".join(
            [
                name
                for name in response.xpath(
                    '//ul[@class="w-list-unstyled"]/li/text()'
                ).getall()
            ]
        ).strip()

        # Facebook
        item["facebook"] = response.xpath(
            '//*[@class="facebook w-inline-block"]/@href'
        ).get()

        # Linkedin
        item["linkedin"] = response.xpath(
            '//*[@class="linkedin w-inline-block"]/@href'
        ).get()

        # Twitter
        item["twitter"] = response.xpath(
            '//*[@class="link-block-5 w-inline-block"]/@href'
        ).get()

        # Website
        item["website"] = response.xpath(
            '//*[@class="link-block-6 w-inline-block"]/@href'
        ).get()

        # Description
        item["description"] = response.xpath('//p[@class="paragraph-18"]/text()').get()

        for key, value in item.items():
            if value == "#":
                item[key] = None

        yield asdict(GlyphSocialItem(**item))
