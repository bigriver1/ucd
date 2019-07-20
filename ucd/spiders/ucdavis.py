# -*- coding: utf-8 -*-
import scrapy

class UcdavisSpider(scrapy.Spider):
    name = 'ucdavis'
    allowed_domains = ['ucdavis.edu']

    start_urls = ['']

    def start_requests(self):

        with open('name.txt') as fp:
            data = fp.read()

        name_list = []
        for i in data.split('\n'):
            name_list.append(i)

        for url in name_list:

            url = 'http://directory.ucdavis.edu/search/directory_results.shtml?filter=%s'%url
            yield scrapy.Request(url=url, callback=self.parse)


    def parse(self, response):
        #print(response.body)
        table = response.xpath('//tr[@valign="top"]')
        for i in table:
            y = i.xpath('td/a/text()').extract()
            w = i.xpath('td/text()').extract()
            print(y ," : ", w)

        fp = open('/Users/wenlin/Documents/python/ucd/ucd/spiders/name.txt', 'r')
        print('*'*100)
        data = fp.read()
        print(data)
        #print(table)

