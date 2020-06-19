# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import re
import json
import codecs

### spider name list

zg_name = "zg"
gwy_name = "gwy"

class GuowuyuanPipeline(object):
    def process_item(self, item, spider):

        item["content"] = self.process_content(item["content"])



        #print (item)
        return item

    def process_content(self,content):

        content = [re.sub(r"\xa0\s","",i) for i in content]

        content = [i for i in content if len(i) > 0]

        return content




class JsonWithEncodingPipleline(object):


    def open_spider(self,spider):


        self.file = codecs.open("gwy.json","w",encoding="utf-8")


    def process_item(self,item,spider):


        lines = json.dumps(dict(item),ensure_ascii=False) + "\n"
        self.file.write(lines)


    def spider_close(self,spider):
        self.file.close()
