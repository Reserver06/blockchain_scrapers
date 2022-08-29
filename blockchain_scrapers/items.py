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


@dataclass
class GlyphSocialItem:
    url: str
    legal_name: str
    category: str
    headquarters: str
    founding_year: str
    founding_team: str
    facebook: str
    linkedin: str
    twitter: str
    website: str
    description: str
