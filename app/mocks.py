# Python bytecode 2.7 (disassembled from Python 2.7)

# Embedded file name: /Users/benmusch/Documents/programming-trinkets/scotus-laughter/app/mocks.py
# Compiled at: 2016-07-29 10:43:22
scalia = {'name': 'Antonin Scalia',
 'id': 1}
souter = {'name': 'David H. Souter',
 'id': 2}
mckenna = {'name': 'Robert M. McKenna',
 'id': 3}
davis = {'name': 'Ethan P. Davis',
 'id': 4}
speakers = [scalia,
 souter,
 mckenna,
 davis]
wash_lines = [[{'speaker': souter,
   'laughter': False,
   'text': "It's helpful to your case, but, going back to my question, do you know any people who go around saying, well, you know, I really prefer the Democrats; I'm a Republican myself?"},
  {'speaker': souter,
   'laughter': False,
   'text': "I mean that, that doesn't happen."},
  {'speaker': mckenna,
   'laughter': True,
   'text': "--Well, the example of Senator Lieberman comes to mind, where he said I really prefer the democrats and I'm running as an independent. (Laughter.)"},
  {'speaker': souter,
   'laughter': False,
   'text': "There's always one"},
  {'speaker': souter,
   'laughter': False,
   'text': "But seriously, as a systemic matter, do you really think that's... thats's a distinction that anyone would recognize?"}]]
ocasio_lines = [[{'speaker': davis,
   'laughter': False,
   'text': "Justice Scalia, until 1992, I think that was an open question, but this Court decided in Evans v. United States in '92 that Hobbs Act extortion encompasses the paying of -- of bribes."},
  {'speaker': scalia,
   'laughter': True,
   'text': 'I dissented, I assume. (Laughter.)'},
  {'speaker': davis,
   'laughter': False,
   'text': 'You did.'},
  {'speaker': davis,
   'laughter': False,
   'text': "But, Your Honor, I think that that -- the decision in Evans was really the high-water mark of this Court's Hobbs Act jurisprudence. And since then the Court has been careful not to expand the Hobbs Act --"}]]
cases = [{'docket_num': '06-713',
  'title': 'Washington State Grange v. Washington State Republican Party',
  'date': '10/01/2007',
  'term': 2007,
  'transcript': 'https://www.supremecourt.gov/oral_arguments/argument_transcripts/06-713.pdf',
  'lines': wash_lines}, {'docket_num': '82-940',
  'title': 'Ocasio v. United States',
  'term': 2015,
  'transcript': 'https://www.supremecourt.gov/oral_arguments/argument_transcripts/14-361_7mip.pdf',
  'lines': ocasio_lines}]

def cases_for_speaker(speaker):

    def has_speaker(case):
        lines = [ line for line_group in case['lines'] for line in line_group ]
        return speaker in [ line['speaker']['id'] for line in lines ]

    return filter(has_speaker, cases)
