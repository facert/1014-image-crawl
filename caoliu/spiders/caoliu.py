#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urlparse
import scrapy
from ..items import ImageItem


class CaoSpider(scrapy.Spider):
    name = "caoliu"
    allowed_domains = ["cl.c1oulske1.pw"]
    start_urls = ['http://cl.c1oulske1.pw/thread0806.php?fid=2',
                    'http://cl.c1oulske1.pw/thread0806.php?fid=8',
                    'http://cl.c1oulske1.pw/thread0806.php?fid=16',
                    'http://cl.c1oulske1.pw/thread0806.php?fid=15',
                    'http://cl.c1oulske1.pw/thread0806.php?fid=4',
                    'http://cl.c1oulske1.pw/thread0806.php?fid=5',
                    'http://cl.c1oulske1.pw/thread0806.php?fid=21']

    domain = "http://cl.c1oulske1.pw/"

    def parse(self, response):
        for url in self.start_urls:
            for i in range(1, 10):
                yield scrapy.Request(('%s&search=&page=%s' % (url, i)), callback=self.parse_products)

    def parse_products(self, response):
        urls = response.xpath('//tr[@class="tr3 t_one"]/td[2]/h3/a/@href').extract()
        # date = response.xpath('//tr[@class="tr3 t_one"]/td[3]/div/text()').extract()[0]
        # import pdb;pdb.set_trace()
        for url in urls:
            yield scrapy.Request(urlparse.urljoin(self.domain, url), callback=self.parse_product_detail)

    def parse_product_detail(self, response):
        if response.url.split('/')[-3] in ['2', '15', '4', '5', '21']:
            image_src = response.xpath('//img/@src').extract()
        else:
            image_src = response.xpath('//input/@src').extract()
        title = response.xpath('//title').extract()[0].split(' ')[0]
        print response.url
        print image_src
        print '-------------'

        for i in image_src:
            image = ImageItem()
            image['image_src'] = i
            image['url'] = response.url
            image['title'] = title
            yield image
