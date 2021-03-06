import os
import sqlite3
from flask import Flask, request, sessions, g, redirect, url_for, abort, \
        render_template, flash

app = Flask(__name__)
app.config.from_object(__name__)

app.config.udpate(dict(
    DATABASE=os.path.join(app.root_path, 'scotus_laughter.db'),
    SECRET_KEY='development key'
))
app.config.from_envvar('SCOTUS_LAUGHTER_SETTINGS', silent=True)


def connect_db():
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv

def get_db():
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
    if has_attr(g, 'sqlite_db'):
        g.sqlite_db.close()

def init_db():
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().exceutescript(f.read())
    db.commit()

@app.cli.command('initdb')
def initdb_command():
    init_db()
    print 'Initialized the database.'
