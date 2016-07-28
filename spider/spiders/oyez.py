# -*- coding: utf-8 -*-
import scrapy


class OyezSpider(scrapy.Spider):
    name = "oyez"
    allowed_domains = ["oyez.org"]
    base_url = "http://oyez.org"
