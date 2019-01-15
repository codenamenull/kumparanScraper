# -*- coding: utf-8 -*-
import re

from scrapy import Request, Spider
from scrapy.loader import ItemLoader
from scrapy.loader.processors import Join, Compose, TakeFirst

from w3lib.html import remove_tags, remove_tags_with_content

from ..items import NewsItem

class TirtoSpider(Spider):
    name = 'tirto'
    allowed_domains = ['tirto.id']

    def __init__(self, *args, **kwargs):
        self.start_url = 'https://tirto.id/'

    def start_requests(self):
        yield Request(f"{self.start_url}", callback=self.parse, meta={'handle_httpstatus_list': [200]})

    def parse(self, response):
        list_news = response.xpath('//div/div[@class="row"]/div[@class="col-md-6 mb-3"]/a/@href').extract()[-4:]
        for news in list_news:
            url = self.start_url + news
            yield Request(f"{url}", callback=self.parse_news, meta={'handle_httpstatus_list': [200]})

    def parse_news(self, response):
        # Item Loader
        item_loader = TirtoItemLoader(item=NewsItem(), response=response)
        item_loader.add_xpath('title', '//h1[@class="news-detail-title text-center animated zoomInUp my-3"]/text()')
        item_loader.add_xpath('content', '//div[@class="content-text-editor"]')
        news_item = item_loader.load_item()

        for key, value in dict(news_item).items():
            print(f"{key}: {value}")

        return news_item

def content_in_processer(value):
    value = remove_tags_with_content(value, which_ones=('h2'))

    value = re.sub(r"<div (?:class=\"(?:baca-holder bold|hiddencaption-photo)\"|id=\"hide-cap\")>.*?<\/div>", '', value)
    value = re.sub(r"[\s]", ' ', value)
    value.strip()

    value = remove_tags(value)

    return value

class TirtoItemLoader(ItemLoader):
    title_out = TakeFirst()
    content_in = Compose(lambda v: v[1], content_in_processer)
    content_out = Join()
