import scrapy
from scrapy.item import Item, Field


class CustomItem(Item):
    text = Field()


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = [
    ]

    def parse(self, response):
        return CustomItem(text=response.body)

