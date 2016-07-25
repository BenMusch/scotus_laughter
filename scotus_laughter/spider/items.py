# -*- coding: utf-8 -*-

from scrapy.item import Item, Field


class CaseItem(Item):
    docket_num = Field()
    date = Field()
    title = Field()
    term = Field()

class OyezCaseItem(CaseItem):
    audio = Field()

class ScotusCaseItem(CaseItem):
    transcript = Field()
