# -*- coding: utf-8 -*-
import calendar
import arrow
import scrapy
from LaunchSpider.items import LaunchspiderItem
import collections


def to_format(value):
    day = value.split()[0].zfill(2)
    month = str(list(calendar.month_name).index(value.split()[1])).zfill(2)
    return "2019-" + month + "-" + day + "T00:00:00+00:00"


def getAllDay():
    start_date = '2019-01-01'
    a = 0
    all_date_list = []
    days_sum = 365
    print()
    while a < days_sum:
        b = arrow.get(start_date).shift(days=a).format("YYYY-MM-DD")
        a += 1
        b += "T00:00:00+00:00"
        all_date_list.append(b)
    return all_date_list


class LaunchSpider(scrapy.Spider):
    name = 'launch'
    allowed_domains = ['en.wikipedia.org']
    start_urls = ['http://en.wikipedia.org/wiki/2019_in_spaceflight#Orbital_launches/']

    def parse(self, response):
        item = LaunchspiderItem()
        result = collections.OrderedDict().fromkeys(getAllDay(), 0)
        row_id = 5
        row = int(response.xpath(
            '//*[@id="mw-content-text"]/div/table[3]/tbody/tr[' + str(row_id) + ']/td[1]/@rowspan').extract_first())
        while row:
            date = response.xpath('//*[@id="mw-content-text"]/div/table[3]/tbody/tr[' + str(
                row_id) + ']/td[1]/span/text()').extract_first()
            date = to_format(date)
            for i in range(1, row):
                outcome = response.xpath('//*[@id="mw-content-text"]/div/table[3]/tbody/tr[' + str(
                    row_id + i) + ']/td[6]/text()').extract_first("").replace('\n', '')
                if outcome == "Operational" or outcome == "Successful" or outcome == "En Route":
                    result[date] += 1
                    break
            row_id += row
            row = response.xpath(
                '//*[@id="mw-content-text"]/div/table[3]/tbody/tr[' + str(row_id) + ']/td[1]/@rowspan').extract_first(
                "")
            if row == "":
                row_id += 1
                row = response.xpath('//*[@id="mw-content-text"]/div/table[3]/tbody/tr[' + str(
                    row_id) + ']/td[1]/@rowspan').extract_first("")
                if row == "": break
                row = int(row)
            else:
                row = int(row)

        item["output"] = result
        yield item
