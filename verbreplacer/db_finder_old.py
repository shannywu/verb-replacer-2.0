'''
name: db_finder_old.py
goal: get connection to RVDB.db and search for the needed information
'''

import sqlite3
import os
import hashlib

PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))

def get_connection():
    conn = sqlite3.connect(PROJECT_ROOT + '/RVDB.db')
    # object type returned for TEXT data type
    conn.text_factory = str
    return conn


def search_coll(word):
    with get_connection() as conn:
        cur = conn.cursor()
        cmd = 'SELECT coll, cnt FROM COLL WHERE word="%s"' % (word)
        return list(cur.execute(cmd))


def search_cnts(word):
     with get_connection() as conn:
        cur = conn.cursor()
        cmd = 'SELECT word, cnt FROM WORD_COUNT WHERE word="%s";' % (word)
        for res in cur.execute(cmd):
            return res[1]


def search_channel(word):
    with get_connection() as conn:
        cur = conn.cursor()
        cmd = 'SELECT correct, orig, avg FROM EF_CHANNEL WHERE wrong="%s"' % (word)
        return list(cur.execute(cmd))

