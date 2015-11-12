#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urlparse
import scrapy
from ..items import ImageItem
from .. import settings


class CaoSpider(scrapy.Spider):
    name = "caoliu"
    allowed_domains = [settings.ALLOW_DOMAIN]
    start_urls = ['%s/thread0806.php?fid=2' % settings.CAOLIU_URL,
                    '%s/thread0806.php?fid=8' % settings.CAOLIU_URL,
                    '%s/thread0806.php?fid=16' % settings.CAOLIU_URL,
                    '%s/thread0806.php?fid=15' % settings.CAOLIU_URL,
                    '%s/thread0806.php?fid=4' % settings.CAOLIU_URL,
                    '%s/thread0806.php?fid=5' % settings.CAOLIU_URL,
                    '%s/thread0806.php?fid=21' % settings.CAOLIU_URL]

    domain = settings.CAOLIU_URL

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
