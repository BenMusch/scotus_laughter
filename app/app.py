# Python bytecode 2.7 (disassembled from Python 2.7)

# Embedded file name: /Users/benmusch/Documents/programming-trinkets/scotus-laughter/app/app.py
# Compiled at: 2016-07-28 15:57:44
from flask import Flask, jsonify, abort
app = Flask(__name__)
from mocks import speakers, cases, cases_for_speaker
from decorators import crossdomain

PAGE_BREAK = "{PAGE BREAK}"

@app.route('/api/cases', methods=['GET'])
@crossdomain(origin='*')
def get_cases():
    return jsonify(cases)


@app.route('/api/cases/<docket_num>', methods=['GET'])
@crossdomain(origin='*')
def get_case_by_docket_num(docket_num):
    for case in cases:
        if case['docket_num'] == docket_num:
            return jsonify(case)

    abort(404)

@app.route('/api/speakers', methods=['GET'])
@crossdomain(origin='*')
def get_speakers():
    return jsonify(speakers)


@app.route('/api/speakers/<int:speaker_id>', methods=['GET'])
@crossdomain(origin='*')
def get_speaker_by_id(speaker_id):
    for speaker in speakers:
        if speaker['id'] == speaker_id:
            return jsonify(speaker)

    abort(404)


@app.route('/api/speakers/<int:speaker_id>/cases', methods=['GET'])
@crossdomain(origin='*')
def get_cases_by_speaker(speaker_id):
    return jsonify(cases_for_speaker(speaker_id))


if __name__ == '__main__':
    app.run(debug=True)
