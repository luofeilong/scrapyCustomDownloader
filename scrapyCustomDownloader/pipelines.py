# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class ScrapycustomdownloaderPipeline(object):
    def process_item(self, item, spider):

        print '%s   %s  %s' % (item['name'], item['url'], item['price']) #, item['publication'], item['author'], item['belong'], item['memprice']

        return item
