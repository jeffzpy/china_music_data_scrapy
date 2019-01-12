# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import codecs

class ArticlespiderPipeline(object):
    def process_item(self, item, spider):
        return item

class JsonWriterPipeline(object):
	def open_spider(self, spider):
		# baiDuMusic.json、
		self.file = open('WWYMusic.json', 'a+')

	def close_spider(self, spider):
		self.file.close()

	def process_item(self, item, spider):
		line = json.dumps(item, ensure_ascii=False) + "\n"
		self.file.write(line)
		return item;

class DuplicatesPipeline(object):
	def __init__(self):
		self.collectionGeted = set()

	def process_item(self, item, spider):
		musicType = item['tab']
		musicSubType = item['subTab']
		musicName = item['title']

		musicKey = musicType + musicSubType + musicName
		if musicSubType in self.collectionGeted:
			raise DropItem('Duplicate music found:%s' % item)

		self.collectionGeted.add(musicKey)
		return item
		
	
		