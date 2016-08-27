# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from datetime import datetime

from app.spider.spiders.scotus import ScotusSpider
from app.models import Case, Transcript
from app.app import db

class SpiderPipeline(object):

    def process_item(self, item, spider):
        return item

class DatabasePipeline(object):

    def process_item(self, item, spider):
        if isinstance(spider, ScotusSpider):
            if 'Question' in item['docket_num']:
                split = item['docket_num'].split('-')
                try:
                    docket_num = "%s-%s" % (split[0], split[1])
                except:
                    import pdb; pdb.set_trace()
                question_num = int(split[-1])
            else:
                docket_num = item['docket_num']
                question_num = 1
            case = Case.query.get(docket_num)
            if case:
                if not Transcript.query.filter_by(docket_num=docket_num,
                        question_num=question_num):
                    print "Creating case for %s..." % item['docket_num']
                    transcript = Transcript(item['url'], case, question_num)
                    db.session.add(transcript)
                    db.session.commit()
                    print 'Success! ' + item['docket_num']
            else:
                print "Creating case and trascript for %s..." % item['docket_num']
                date = datetime.strptime(item['date'], ScotusSpider.date_format)
                case = Case(docket_num, item['title'], date)
                transcript = Transcript(item['transcript'], case, question_num)
                db.session.add(case)
                db.session.add(transcript)
                db.session.commit()
                print 'Success! ' + item['docket_num']
