import re

import slate

#from app.models import Line

class PdfParser(object):
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

    def __init__(self, file_path):
        with open(file_path) as f:
            self.doc = slate.PDF(f)
        self.joined_text = self.PAGE_BREAK.join(self.doc)
        self.cleaned_text = self.joined_text
        for pattern in self.REPLACEMENTS:
            self.cleaned_text = re.sub(pattern, "", self.cleaned_text)
        self.cleaned_text = self.cleaned_text.replace(self.PAGE_BREAK, "")

    def extract_lines(self):
        cur_index = 0
        count = 0
        num_laughs = self.cleaned_text.count("(Laughter.)")

        #while count < num_laughs:
        #    index = 

