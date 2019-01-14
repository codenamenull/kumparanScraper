# -*- coding: utf-8 -*-
from scrapy import Request, Spider
from scrapy.loader import ItemLoader
from scrapy.loader.processors import Join, MapCompose, TakeFirst

from w3lib.html import remove_tags

from ..items import NewsItem

class KumparanSpider(Spider):
    name = 'kumparan'
    allowed_domains = ['kumparan.com']

    def __init__(self, *args, **kwargs):
        self.base_url = 'https://kumparan.com'
        self.start_url = 'https://kumparan.com/trending/cerita/'

    def start_requests(self):
        yield Request(f"{self.start_url}", callback=self.parse, meta={'handle_httpstatus_list': [200]})

    def parse(self, response):
        list_news = response.xpath('//div[@class="View__StyledView-sc-1nce11s-0 dEXYcz"]/a/@href').extract()
        for news in list_news:
            url = self.base_url + news
            yield Request(f"{url}", callback=self.parse_news, meta={'handle_httpstatus_list': [200]})

    def parse_news(self, response):
        # Item Loader
        item_loader = KumparanItemLoader(item=NewsItem(), response=response)
        item_loader.add_xpath('title', '//span[@data-qa-id="story-title"]/span/span/span/text()')
        item_loader.add_xpath('content', '//span[@class="track_paragraph components__TextParagraph-s1de2sbe-0 SXPvF Textweb__StyledText-sc-2upo8d-0 dABVaj"]')
        news_item = item_loader.load_item()

        for key, value in dict(news_item).items():
            print(f"{key}: {value}")

        return news_item

class KumparanItemLoader(ItemLoader):
    title_out = TakeFirst()
    content_in = MapCompose(remove_tags)
    content_out = Join()