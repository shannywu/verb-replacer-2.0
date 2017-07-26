import fileinput
import sqlite3

TABLE_SCHEMA = ('CREATE TABLE EF_VOBJ_TABLE('
                    "wrong TEXT, "
                    "correct TEXT, "
                    "cnt INT "
                    ');')


def get_connection():
    conn = sqlite3.connect('RVDB.db')
    conn.text_factory = str
    return conn

def parse_word_cnts():
    for line in fileinput.input('ef.vobj.channel.txt'):
        wrong, correct, cnt = line.strip().split('\t')
        yield (wrong.lower(), correct.lower(), cnt)

def init_db(word_cnts):
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("DROP TABLE IF EXISTS EF_VOBJ_TABLE;")
        # create table
        cur.execute(TABLE_SCHEMA)
        # insert data
        cur.executemany('INSERT INTO EF_VOBJ_TABLE VALUES (?,?,?)', word_cnts)

def search_cnts(word):
    with get_connection() as conn:
        cur = conn.cursor()
        cmd = 'SELECT * FROM EF_VOBJ_TABLE WHERE wrong="%s";' % (word)
        for res in cur.execute(cmd):
            return res
        

if __name__ == '__main__':
    # bnc word lemma data
    word_cnts = list(parse_word_cnts())
    # insert data into sqlite3 db
    init_db(word_cnts)
    # search example. (Notice: result will be None if not exist)
    print search_cnts('paly_game');
