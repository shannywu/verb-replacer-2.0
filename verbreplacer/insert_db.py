import fileinput
import sqlite3

TABLE_SCHEMA = ('CREATE TABLE EF_CHANNEL('
                    "wrong TEXT, "
                    "correct TEXT, "
                    "orig INT, "
                    "avg FLOAT "
                    ');')


def get_connection():
    conn = sqlite3.connect('RVDB.db')
    conn.text_factory = str
    return conn

def parse_word_cnts():
    for line in fileinput.input('resources/ef.result.model.txt'):
        wrong, correct, reg, orig, avg = line.strip().split('\t')
        yield (wrong, correct, orig, avg)

def init_db(word_cnts):
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("DROP TABLE IF EXISTS EF_CHANNEL;")
        # create table
        cur.execute(TABLE_SCHEMA)
        # insert data
        cur.executemany('INSERT INTO EF_CHANNEL VALUES (?,?,?,?)', word_cnts)

def search_cnts(word):
    with get_connection() as conn:
        cur = conn.cursor()
        cmd = 'SELECT * FROM EF_CHANNEL WHERE wrong="%s";' % (word)
        for res in cur.execute(cmd):
            return res
        

if __name__ == '__main__':
    # bnc word lemma data
    word_cnts = list(parse_word_cnts())
    # insert data into sqlite3 db
    init_db(word_cnts)
    # search example. (Notice: result will be None if not exist)
    print search_cnts('say');
