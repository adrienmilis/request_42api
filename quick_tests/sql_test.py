import sqlite3
from contextlib import closing

with closing(sqlite3.connect('api_tokens.db')) as con:
    with closing(con.cursor()) as cur:
    
        cur.execute('''CREATE TABLE IF NOT EXISTS tokens
                        (date text, username text, token text)''')
    
        cur.execute("INSERT INTO tokens VALUES ('date1', 'amilis', 'token1')")
        cur.execute("INSERT INTO tokens VALUES ('date2', 'login2', 'token2')")
        con.commit()
    
        for row in cur.execute("SELECT * from tokens"):
            print(row[1])
