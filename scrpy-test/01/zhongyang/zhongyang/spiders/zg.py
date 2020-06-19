# -*- coding: utf-8 -*-
import scrapy

from zhongyang.items import ZhongyangItem
from copy import deepcopy
class ZgSpider(scrapy.Spider):
    name = 'zg'
    allowed_domains = ['people.cn']
    start_urls = ['http://jhsjk.people.cn/result/2?title=&content=%E5%8D%AB%E7%94%9F&form=701&year=0&submit=%E6%90%9C%E7%B4%A2']

    def parse(self, response):


        item = ZhongyangItem()

        li_list = response.xpath("//ul[@class='list_14 p1_2 clearfix']/li")


        for li in li_list:
            temp = li.xpath("./text()").extract_first()
            temp = temp[1:5]

            if int(temp) > self.settings["FROM_YEAR"]:

                item["publish_date"] = li.xpath("./text()").extract_first()
                item["publish_date"] = item["publish_date"][1:-5]
                item["name"] = li.xpath("./a/text()").extract_first()
                item["url"] = li.xpath("./a/@href").extract_first()

                item ["url"] = "http://jhsjk.people.cn/" + item["url"]


                yield scrapy.Request(
                    item["url"],
                    callback = self.parse_detail,
                    meta = {"item": deepcopy(item)}
                )


        next_page_url = response.xpath("//a[text()='>']/@href").extract_first()
        if next_page_url is not None:
            yield scrapy.Request(
                next_page_url,
                callback = self.parse
            )

    def parse_detail(self,response):

        item = response.meta["item"]


        item["content"] = response.xpath("//div[@class='d2txt_con clearfix']/p/text()").extract()

        yield item
