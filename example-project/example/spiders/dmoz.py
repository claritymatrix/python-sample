from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

import re

class DmozSpider(CrawlSpider):
    """Follow categories and extract links."""
    name = 'dmoz'
    allowed_domains = ['gov.cn']
    start_urls = ['http://sousuo.gov.cn/column/30900/0.htm','http://sousuo.gov.cn/column/30562/0.htm']

    rules = [
            Rule(LinkExtractor(allow=r'http://www.gov.cn/premier/20\d{2}-\d{2}/\d{2}/content_\d+\.htm'),callback = 'parse_detail',follow = False),
            Rule(LinkExtractor(allow=r'http://sousuo.gov.cn/column/30900/\d+\.htm'),follow = True),
            Rule(LinkExtractor(allow=r'http://http://www.gov.cn/guowuyuan/cwhy/\d+c\d{2}/index.htm'),follow = True),
            Rule(LinkExtractor(allow=r'http://sousuo.gov.cn/column/30562/\d+\.htm'),follow = True),

    ]




    def parse_detail(self,response):
        item = {}

        item["title"] = response.xpath("//div[@class='article oneColumn pub_border']/h1/text()").extract_first()

        item["time"] = re.findall("(20\d{2}-\d{2}-\d{2} \d{2}:\d{2})",response.body.decode())[0]
        item["article"] = response.xpath("//div[@class='pages_content']/p/text()").extract()
        
        yield item 




