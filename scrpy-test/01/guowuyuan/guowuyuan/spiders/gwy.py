# -*- coding: utf-8 -*-
import scrapy

from guowuyuan.items import GuowuyuanItem
from copy import deepcopy


class GwySpider(scrapy.Spider):
    name = 'gwy'
    allowed_domains = ['www.gov.cn','sousuo.gov.cn']
    start_urls = ['http://sousuo.gov.cn/s.htm?q=%E5%8D%AB%E7%94%9F&t=paper']

    def parse(self, response):

        item = GuowuyuanItem()


        li_list = response.xpath("//li[@class='res-list']")

        for li in li_list:

            item["publish_date"] = li.xpath("./p/span[2]/text()").extract_first()
            temp = item["publish_date"][6:10]


            if int(temp) > self.settings["FROM_YEAR"]:


                item["publish_date"] = temp
                item["url"] = li.xpath("./h3/a/@href").extract_first()


                yield scrapy.Request(
                    item["url"],
                    callback = self.parse_detail,
                    meta = {"item":deepcopy(item)}
                )

        next_page_url = response.xpath("//*[@id='snext'][1]/@href").extract_first()

        if next_page_url is not None:

            yield scrapy.Request(
                next_page_url,
                callback = self.parse
            )


    def parse_detail(self,response):

        item = response.meta["item"]

        item["name"] = response.xpath("//table[1]/tbody/tr/td/table[1]/tbody/tr[3]/td[2]/text()").extract_first()

        item["wenhao"] = response.xpath("//table[1]/tbody/tr/td/table[1]/tbody/tr[4]/td[2]/text()").extract_first()

        item["content"] = response.xpath("//table[2]/tbody/tr/td[1]/table/tbody/tr/td/table[1]/tbody/tr[1]/td/p/text()").extract()

        yield item
