# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


class LaunchspiderPipeline(object):
    def __init__(self):
        self.file = open('output.csv', 'w', encoding="utf-8")

    def process_item(self, item, spider):
        self.file.write("date,value\n")
        for key, value in item["output"].items():
            self.file.write('{0},{1}\n'.format(key, value))
        return item

    def close_spider(self, spider):
        self.file.close()
