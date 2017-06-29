'''
name: db_finder.py
goal: get connection to RVDB.db and search for the needed information
'''

import sqlite3
import os
import hashlib

PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))


# def get_connection():
#     conn = sqlite3.connect(db_path)
#     # object type returned for TEXT data type
#     conn.text_factory = str
#     return conn


class dbFinder:
    def __init__(self, db_path=PROJECT_ROOT + '/RVDB.db'):
        self.conn = sqlite3.connect(db_path)
        self.conn.text_factory = str
    
    def __del__(self):
        self.conn.close()
    
    def search_coll(self, word):
        cur = self.conn.cursor()
        cmd = 'SELECT coll, cnt FROM COLL WHERE word="%s"' % (word)
        return list(cur.execute(cmd))
    
    def search_cnts(self, word):
        cur = self.conn.cursor()
        cmd = 'SELECT word, cnt FROM WORD_COUNT WHERE word="%s";' % (word)
        for res in cur.execute(cmd):
            return res[1]