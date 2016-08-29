from sqlalchemy import event

from app import db

class Case(db.Model):
    docket_num = db.Column(db.String(10), primary_key=True)
    title = db.Column(db.String(256), index=True, unique=True)
    date = db.Column(db.DateTime)

    def __init__(self, docket_num, title, date):
        self.docket_num = docket_num
        self.title = title
        self.date = date

    def __repr__(self):
        return '<Case %s: %s>' % (self.docket_num, self.title)

class Transcript(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(256), unique=True)
    docket_num = db.Column(db.String(10), db.ForeignKey('case.docket_num'))
    question_num = db.Column(db.Integer, default=1)
    processed = db.Column(db.Boolean, default=False)

    def __init__(self, url, case, question_num=1, processed=False):
        self.url = url
        self.docket_num = case.docket_num
        self.question_num = question_num
        self.processd = processed

class LineGroup(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    transcript_id = db.Column(db.Integer, db.ForeignKey('transcript.id'))

    def __init__(self, transcript):
        self.transcript_id = transcript.id

class Line(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    speaker = db.Column(db.String(100))
    text = db.Column(db.String)
    has_laughter = db.Column(db.Boolean)
    group_index = db.Column(db.Integer)
    group_id = db.column(db.Integer, db.ForeignKey('line_group.id'))

    def __init__(self, speaker, text, group, group_index, has_laughter):
        self.speaker = speaker
        self.text = text
        self.group_id = group.id

from pdf_parser import LineGenerator

@event.listens_for(Transcript, 'after_insert')
def process_transcript(mapper, connection, target):
    '''
    Once a Transcript is created, process the pdf file and mark the transcript
    as processed
    '''
    print 'beginning process for ' + target.docket_num
    LineGenerator(target).process()
    target.proccessed = True
    db.session.commit()
    print 'finished processing' + target.docket_num

