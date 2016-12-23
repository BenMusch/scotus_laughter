import re
import logging
import time
from urllib import urlretrieve

import slate

from models import Line, LineGroup
from app import db

class PdfParser(object):
    '''
    Parses a formatted transcript pdf into an array of the text for Lines with
    laughter
    '''
    PAGE_BREAK = "{PAGE BREAK}"
    REPLACEMENTS = [
            # various whitespace chars
            "\xc2",
            "\xa0",
            "\n",
            "\xad",
            "\x0c",
            # removes line numbers and footers
            "\s*AldersonReportingCompany\s*",
            "\s*SubjecttoFinalReview\s*",
            "\s*1\s*2\s*3\s*4\s*5\s*6\s*7\s*8\s*9\s*10\s*11\s*12\s*13\s*14\s*15\s*16\s*17\s*18\s*19\s*20\s*21\s*22\s*23\s*24\s*25\s*",
            "Official\d+",
        ]
    SPEAKER_PATTERN = "([A-Z][A-Z\s\.\\']+:)"
    LAUGHTER = "(Laughter.)"

    def __init__(self, file_path, transcript=None):
        if 'http' in file_path:
            tmp_filename = "../" + transcript.docket_num + "-" + str(int(time.time()))
            urlretrieve(file_path, tmp_filename)
            file_path = tmp_filename
        with open(file_path) as f:
            self.doc = slate.PDF(f)
        self.joined_text = self.PAGE_BREAK.join(self.doc)
        self.cleaned_text = self.joined_text
        for pattern in self.REPLACEMENTS:
            self.cleaned_text = re.sub(pattern, "", self.cleaned_text)
        self.cleaned_text = self.cleaned_text.replace(self.PAGE_BREAK, "").replace("  ", " ")

    def extract_laughter(self):
        i = 0
        count = 0
        num_laughs = self.cleaned_text.count(self.LAUGHTER)

        lines = self._zipped_lines()
        laughter_groups = []

        while count < num_laughs:
            line = lines[i]
            i += 1
            if self.LAUGHTER in line[1]:
                laughter_group = [lines[i-2], line]
                count += 1
                if len(lines) > i:
                    next_line = lines[i]
                    while self.LAUGHTER in next_line[1] and len(lines) > i:
                        laughter_group += [next_line]
                        count += 1
                        i += 1
                        next_line = lines[i]
                    laughter_group += [next_line]
                laughter_groups.append(laughter_group)
        return laughter_groups


    def _zipped_lines(self):
        lines = re.split(self.SPEAKER_PATTERN, self.cleaned_text)
        zipped = []
        i = 0
        cur_line = lines[i]
        started_args = False

        while 'submitted.)' not in cur_line:
            try:
                cur_line = lines[i]
            except:
                logging.log(logging.ERROR, 'Index %s out of bounds' % i)
                break

            i += 1
            if not started_args:
                started_args = 'proceedings' in cur_line.lower().replace(" ", "")
            elif re.match(self.SPEAKER_PATTERN, cur_line) and len(lines) > i:
                zipped.append([cur_line, lines[i].strip()])
                i += 1
        return zipped

class LineGenerator(object):
    '''
    Takes the data from the PdfParser and interacts with the database. Given a
    Transcript, this object will perist the relevant Lines and LineGroups to the
    database.
    '''

    def __init__(self, transcript):
        self.transcript = transcript

    def process(self):
        parser = PdfParser(self.transcript.url)
        for line_group_data in parser.extract_laughter():
            group = LineGroup(self.transcript)
            index = 0
            for line_data in line_group_data:
                index += 1
                speaker_name = line_data[0]
                text = line_data[1]
                has_laughter = PdfParser.LAUGHTER in text
                line = Line(speaker_name, text, group, index, has_laughter)
                db.session.add(line)
            db.session.add(group)
        db.session.commit()
