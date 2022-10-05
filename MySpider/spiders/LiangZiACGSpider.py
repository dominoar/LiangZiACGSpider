import logging
import re
import sys

import pymysql
import requests
import scrapy
from lxml import etree
from scrapy import Request
from scrapy.http import Response

from MySpider.items import GalgameItem

page_number: int = 0


# 抓取全站包含galgame的每一页
class LiangZiAcgSpider(scrapy.Spider):
    name = 'AllPage'
    allowed_domains = ["https://lzacg.one"]
    all_page: int

    # 抓取指定页面时取消注释
    # start_urls = ['https://lzacg.one/galgame/page/33']
    # 将所有预先url交给引擎
    def start_requests(self):
        for i in range(0, 34):
            yield Request(url=f'https://lzacg.one/galgame/page/{i}')

    def parse(self, response: Response, **kwargs):
        global page_number
        # 将量子论坛的所有一级资源输出到本地，以方便解析
        try:
            print("WriteStarting………………")
            open(file=f'/html/量子ACG/index{page_number}.html', mode='w+', encoding='UTF-8').writelines(
                response.body.decode())
            # 抓取指定页面时取消注释
            # open(file=f'/html/量子ACG/index33.html', mode='w+', encoding='UTF-8').writelines(
            #     response.body.decode())
        except Exception as e:
            print(e.args, e)
        finally:
            page_number = page_number + 1


class LiangZiGalgame(scrapy.Spider):
    """单独解析一个资源"""
    name = 'OneGalgame'
    allowed_domains = ['https://lzacg.one']
    start_urls = ['https://lzacg.one/5545', 'https://lzacg.one/5547', 'https://lzacg.one/5548']

    def parse(self, response, **kwargs):
        galgame = GalgameItem()
        galgame['title'] = response.xpath('//h1[@class="article-title"]/a/text()')[0].extract()
        galgame['home'] = response.xpath('//h1[@class="article-title"]/a/@href')[0].extract()
        galgame['downlinks'] = response.xpath('//a[contains(@class,"wp-block-button__link")]/@href').extract()
        galgame['images'] = response.xpath('//figure[contains(@class,"wp-block-image")]/img/@src').extract()
        yield galgame


# 抓取每一页中所有的galgame
class LiangZiGalgameSpider(scrapy.Spider):
    name = 'AllGalgame'
    allowed_domains = ["https://lzacg.one"]
    start_urls = ['file:///D:/html/%E9%87%8F%E5%AD%90ACG/index0.html']

    def start_requests(self):
        # 预填充所有页面资源到引擎
        for i in range(1, 34):
            page = etree.parse(f'/html/量子ACG/index{i}.html', etree.HTMLParser())
            links = page.xpath('//div[@class="item-thumbnail"]/a/@href')
            print(f'正在填充第{i}页的资源链接…………')
            for link in links:
                yield Request(url=link)

    def parse(self, response: Response, **kwargs):
        global page_number
        file_name = '/html/量子ACG/Galgame'
        try:
            open(file_name + f'/index{page_number}.html', 'w+', encoding='UTF-8').writelines(
                response.body.decode())
            page_number = page_number + 1
        except Exception as e:
            print(e.args, e)
        pass


# 解析所有获取到的galgame
class GalgameResult(scrapy.Spider):
    name = 'DataResult'
    j = 100 / 427

    def start_requests(self):
        for i in range(0, 427):
            print(f'{i * self.j}%')
            yield Request(url=f'file:///D:/html/%E9%87%8F%E5%AD%90ACG/Galgame/index{i}.html')

    def parse(self, response: Response, **kwargs):
        galgame = GalgameItem()
        galgame['title'] = response.xpath('//h1[@class="article-title"]/a/text()')[0].extract()
        galgame['home'] = response.xpath('//h1[@class="article-title"]/a/@href')[0].extract()
        galgame['downlinks'] = response.xpath('//a[contains(@class,"wp-block-button__link")]/@href').extract()
        galgame['images'] = response.xpath('//figure[contains(@class,"wp-block-image")]/img/@src').extract()
        yield galgame
