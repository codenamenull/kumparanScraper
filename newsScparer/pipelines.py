# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
from pathlib import Path
from datetime import date
from scrapy.utils.project import get_project_settings

class NewsscparerPipeline(object):

    def __init__(self, *args, **kwargs):
        self.news_items = []
        self.settings = get_project_settings()
        self.parent_dir = Path(__file__).resolve().parent
        self.news_dir = self.parent_dir.joinpath(self.settings.get('JSON_STORE'))
     
    def open_spider(self, spider):
        self.news_dir.mkdir(parents=True, exist_ok=True)
        self.file = open(f"{self.news_dir}/news_{spider.name}_{str(date.today())}.json", 'w')

    def close_spider(self, spider):
        self.file.write(json.dumps(self.news_items))
        self.file.close()

    def process_item(self, item, spider):
        self.news_items.append(dict(item))
        return item