# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from wxapp.items import WxappItem

class WxappSpiderSpider(CrawlSpider):
    name = 'wxapp_spider'
    allowed_domains = ['www.wxapp-union.com']
    start_urls = ['http://www.wxapp-union.com/portal.php?mod=list&catid=1&page=1']

    rules = (
        # .+表示前面有任意个字符  \d表示数字
        Rule(LinkExtractor(allow=r'.+mod=list&catid=1&page=\d'), follow=True),
        Rule(LinkExtractor(allow=r'article-.+\.html'),callback="parse_detail", follow=False),
    )

    def parse_detail(self, response):
        title = response.xpath("//h1[@class='ph']/text()").get()
        # print(title)
        author_p = response.xpath("//p[@class='authors']")
        author = author_p.xpath(".//a/text()").get()
        pub_time = author_p.xpath(".//span/text()").get()
        # print("author:%s/pub_time:%s" %(author,pub_time))
        # print("="*30)
        article_content = response.xpath("//td[@id='article_content']//text()").getall()
        content = "".join(article_content).strip()
        # print(content)
        # print("=" * 30)
        item = WxappItem(title=title, author=author, pub_time=pub_time, content=content)
        yield item  # 返回item，此处等价于 return item

