import pickle
import re
from scrapy.spiders import SitemapSpider
from ..items import CryptoslateItem
from dataclasses import asdict
from pathlib import Path


class CryptoslateSpider(SitemapSpider):
    name = "cryptoslate"
    sitemap_urls = ["https://cryptoslate.com/sitemap_index.xml"]
    sitemap_follow = [r"\/post-sitemap"]
    custom_settings = {
        "MONGO_URI": "mongodb://localhost:27017/",
        "MONGO_DATABASE": "cryptoslate",
        "MONGO_COLLECTION_NAME": "news_articles",
        "ITEM_PIPELINES": {
            "blockchain_scrapers.pipelines.MongoDBScrapersPipeline": 300
        },
        "TWISTED_REACTOR": "twisted.internet.asyncioreactor.AsyncioSelectorReactor",
        "USER_AGENT": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36",
        "DOWNLOAD_DELAY": 3,
    }

    def __init__(self, category=None, *args, **kwargs):
        if category:
            self.sitemap_rules = [
                (category, "parse"),
            ]
        super(CryptoslateSpider, self).__init__(*args, **kwargs)

    def parse(self, response):
        item = {}
        if re.search(r"/blog/$", response.url):
            return

        stash_webpage(response)

        # URL
        item["url"] = response.url

        # Title
        item["title"] = response.xpath("//h1/text()").get()

        # Sub Title
        item["sub_title"] = response.xpath("//p[@class='post-subheading']/text()").get()

        # Topic
        item["topic"] = response.xpath("//span[@class='big-cat']/span/a/text()").get()

        # Author
        item["author"] = response.xpath("//div[@class='author-info']/a/text()").get()

        # Author Socials
        links = response.xpath(
            "(//span[@class='author-social break'])[1]/a/@href"
        ).getall()
        item["author_socials"] = ", ".join(
            [link for link in links if not re.search("cdn-cgi", link)]
        )

        # Read Length
        item["read_length"] = response.xpath(
            "//div[@class='post-reading']/span/text()"
        ).get()

        # Time Published
        times = response.xpath("(//*[@class='post-date'])[1]//text()").getall()
        item["time_published"] = " ".join([time.strip() for time in times]).strip()

        yield asdict(CryptoslateItem(**item))


def stash_webpage(response):
    raw_html = response.text
    raw_url = response.url
    url = raw_url.split(".com/")[1].replace("/", "")

    item = {
        "url": response.url,
        "raw_html": raw_html,
    }
    path = Path.cwd().joinpath("blockchain_scrapers").joinpath("pickles")
    with open(path.joinpath(f"{url}.pickle"), "wb+") as pf:
        pickle.dump(item, pf)
