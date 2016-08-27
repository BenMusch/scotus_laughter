# -*- coding: utf-8 -*-
import re

from scrapy.spider import Spider
from scrapy.selector import Selector
from scrapy.http import Request

from app.spider.spiders.base import BaseSpider
from app.spider.items import ScotusCaseItem


class ScotusSpider(BaseSpider):
    name = "scotus"
    allowed_domains = ["supremecourt.gov"]
    base_url = "http://www.supremecourt.gov/"
    filler_characters = ["\r", "\xa0"]
    date_format = '%m/%d/%y'

    def parse_term(self, response):
        hxs = Selector(response)

        rows = hxs.xpath("//table/tr")
        for row in rows:
            row_text = "".join(row.xpath(".//text()").extract())
            if self.docket_num:
                dont_skip = self.docket_num in row_text
            else:
                dont_skip = re.findall(self.docket_regex, row_text)
            if dont_skip:
                row_text = self._clean_text(row_text)
                case = ScotusCaseItem()
                case["docket_num"] = re.findall(self.docket_regex, row_text)[0][0]
                row_text = row_text.replace(case["docket_num"] + ".", "")
                case["title"] = re.findall(self.title_regex,
                        row_text)[0].strip()
                case["date"] = re.findall(self.date_regex, row_text)[0]
                case["transcript"] = row.xpath(".//a/@href").extract()[0]
                case["transcript"] = case["transcript"].replace("../",
                        self.base_url + "oral_arguments/")
                yield case

    def term_request(self):
        return self.case_request()

    def case_request(self):
        url = "{}oral_arguments/argument_transcript/{}".format(
                self.base_url, self.term)
        return Request(url, callback=self.parse_term)

    def _clean_text(self, text):
        text = text.encode("ascii", "ignore")
        for char in self.filler_characters:
            text = text.replace(char, "")
        return text
