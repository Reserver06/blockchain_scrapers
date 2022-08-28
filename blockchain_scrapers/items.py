# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from dataclasses import dataclass


@dataclass
class CryptoslateItem:
    url: str
    title: str
    sub_title: str
    topic: str
    author: str
    author_socials: str
    read_length: str
    time_published: str
