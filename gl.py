# -*- coding: utf-8 -*-
# import requests
# from lxml import etree
# from scrapy.selector import Selector
from scrapy.http import Request
from gulu.items import GuluItem
from scrapy_redis.spiders import RedisSpider,Spider,CrawlSpider
from gulu.Type_name import type_text
import scrapy
import time
from urllib.parse import urljoin
import datetime
from copy import deepcopy
s = time.time()

class GlSpider(Spider):
    name = 'gl'
    allowed_domains = ['www.guruin.com']
    # start_urls = https://www.guruin.com/mini-articles
    # 分布式爬虫的redis_key
    # redis_key = "glspider:start_urls"
    # 获取动态域
    # def __init__(self, *args, **kwargs):
    #     # Dynamically define the allowed domains list.
    #     domain = kwargs.pop('domain', '')
    #     self.allowed_domains = filter(None, domain.split(','))
    #     super(GlSpider, self).__init__(*args, **kwargs)

    # start_urls = []
    # for name in type_text:
    #     url = 'https://www.guruin.com/%s' %name
    #     start_urls.append(url)
    # start_urls = ['https://www.guruin.com/education']
    num = 0
    url = "https://www.guruin.com/news.html+infinite?page="
    start_urls = (
        url + str(num),
    )

    # def start_requests(self):
    #     for url in self.start_urls:
    #         # print(url)
    #         yield Request(url=url, callback=self.parse)

    def parse(self, response):
        # item = GuluItem()
        # 类型
        # item['type'] = response.xpath('//div[@class="swiper-slide"][2]/a/span/text()')
        for each in response.xpath('//div[@class="campaign no-hidden"]'):
            item = GuluItem()
            # 标题 | .//a/div/text()
            item['title'] = each.xpath('.//h2/a/text()').extract_first()

            # 内容
            # item['content'] = each.xpath('.//p/text()').extract_first()

            # 图片url
            item['image_url'] = each.xpath(".//div/img/@src").extract_first()

            # # 城市
            # item['city'] = each.xpath('./div[1]/div/text()').extract_first()
            # 添加时间
            d = datetime.datetime.fromtimestamp(int(s))
            item['addtime'] = d
            # item['date_time'] = self.get_data_time(response)

            # 标签
            # item['tag'] = each.xpath('.//div[@class="campaign-info-category"]/text()').extract()[0]
            # 子类的url
            item['detail_url'] = each.xpath('.//h2/a/@href').extract_first()
            if item['detail_url'] is not None:
                item['detail_url'] = "https://www.guruin.com" + item['detail_url']
                yield scrapy.Request(item['detail_url'], callback=self.parse_detail, meta={"item": item})
            if self.num < 1418:
                self.num += 1
                yield scrapy.Request(self.url + str(self.num), callback=self.parse)

    def parse_detail(self, response):
        item = response.meta['item']

        # item['link_url'] = response.xpath('//div[@class="col-md-9"]//p//@href').extract()
        item['content_text'] = response.xpath('//div[@class="col-md-9"]//p//text() |  //div[@class="col-md-9"]//h2//text()').extract()
        # item['address'] = response.xpath('//div[@class="campaign-md"]/a/div/text()').extract()[0]

        item['detail_img'] = response.xpath('//div[@class="col-md-9"]//img/@src').extract()
        yield item



"""
        # scrapy选择器
        # selector = Selector(response)
        # guruin = selector.xpath()
        # guruin = response.xpath("//div[@class='campaign-desc'] | //div[@class='row']")
        for each in response.xpath("//div[@class='campaign-desc']"):
            item = GuluItem()
            # 类型
            # item['type'] = self.get_type(response)

            # 子类的url
            item['url'] = self.get_url(response)

            # 标题
            item['title'] = self.get_title(response)

            # 内容
            item['content'] = self.get_content(response)

            # 图片url
            item['image_url'] = self.get_image_url(response)

            # 城市
            item['city'] = self.get_city(response)

            # 添加时间
            d = datetime.datetime.fromtimestamp(int(s))
            item['addtime'] = d
            # item['date_time'] = self.get_data_time(response)

            # 布尔值，确认是否已爬取
            # item['python_bool'] = self.get_python_bool(response)
            # 构造下一页的请求
            # 判断页面总数，循环请求
            # yield item
            # 对URL进行下一步处理，跟进详情页信息，callback：parse_detail回调行数进行处理
            yield scrapy.Request(item['url'], callback=self.parse_detail, meta={'item': item})

        if self.num < 184:
            self.num += 1
            yield scrapy.Request(self.url + str(self.num), callback=self.parse)

    #
    #
    def parse_detail(self, response):
        item = response.meta['item']
        item['content_text'] = response.xpath('//div[@class="ignore-opencc"]/p/text()').extract()
        item['address'] = response.xpath('//div[@class="campaign-md"]/a/div/text()').extract()[0]
        item['tag'] = response.xpath('//div[@class="campaign-info"]/div/span/text()').extract()[0]
        yield item
        

    def get_url(self, response):
        u = response.xpath('//div[@class="campaign-desc"]/h2/a/@href ').extract()
        if len(u):
            u = u[0]
            url = urljoin("https://www.guruin.com", u)
        else:
            url = "NULL"
        return url.strip()


    # def get_type(self, response):
    #     type = response.xpath('//div[@class="swiper-slide"][2]/a/span/text()').extract()
    #     if len(type):
    #         type = type[0]
    #     else:
    #         type = "NULL"
    #     return type.strip()

    def get_title(self, response):
        title = response.xpath('//div[@class="campaign-desc"]/h2/a/text() | //div[@class="row"]//a/text()').extract()
        if len(title):
            title = title[0]
        else:
            title = "NULL"
        return title.strip()

    def get_content(self, response):
        content = response.xpath('//div[@class="campaign-desc"]//p/text()').extract()
        if len(content):
            content = content[0]
        else:
            content = "NULL"
        return content.strip()

    def get_image_url(self, response):
        image_url = response.xpath('//div[@class="row"]//a/@style').extract()
        if len(image_url):
            image_url = image_url[0]
        else:
            image_url = "NULL"
        return image_url.strip()

    def get_city(self, response):
        city = response.xpath('//div[@class="campaign-desc"]/div[1]/div/text()').extract()
        if len(city):
            city = city[0]
        else:
            city = "NULL"
        return city.strip()
"""


