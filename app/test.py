from app import db
from models import Case, Transcript, LineGroup, Line
from pdf_parser import LineGenerator

if __name__ == '__main__':
    transcript = Transcript.query.filter_by(docket_num="15-7").first()
    print Line.query.all()
    [ line.delete() for line in Line.query.all()]
    print Line.query.all()
    LineGenerator(transcript).process()
    group = LineGroup.query.filter_by(transcript_id=transcript.id).first().id
    print group
    lines = Line.query.all()
    print lines
    for line in lines:
        print line.group_id
        print line.speaker
        print line.text
