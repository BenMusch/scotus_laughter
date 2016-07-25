# -*- coding: utf-8 -*-
import re

import scrapy

class BaseSpider(scrapy.Spider):
    name = "base"
    docket_regex = r"\d+\-\d+"
    date_regex = r"[01]\d\/[0-3]\d\/\d{2}"
    title_regex = r".+\sv\.\s.+"

    def __init__(self, *args, **kwargs):
        self.docket_num = kwargs.get('docket_num')
        self.term = kwargs.get('term')

    def start_requests(self):
        if self.docket_num:
            yield self.case_request()
        elif self.term:
            yield self.term_request()

    def parse_term(self, response):
        pass

    def parse_case(self, response):
        pass

    def term_request(self, term):
        raise NotImplementedError()

    def case_request(self, docket_num):
        raise NotImplementedError()

