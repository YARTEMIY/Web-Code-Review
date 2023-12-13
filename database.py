import sqlite3
import config


def create_tables(cur, conn):
    cur.execute('DROP TABLE IF EXISTS goods')
    
    cur.execute(''' 
    CREATE TABLE goods (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        price INTEGER,
        amount TEXT,
        link TEXT,
        model_name TEXT
    )
    ''')

    cur.execute('CREATE UNIQUE INDEX IF NOT EXISTS idx_title ON goods(title);')
    
    conn.commit()


def add_good(good):
    conn = sqlite3.connect(config.dbname)
    cur = conn.cursor()
    title, price, amount, link, model_name = good
    cur.execute("""
    INSERT INTO goods (title, price, amount, link, model_name)
    VALUES (?, ?, ?, ?, ?)
    ON CONFLICT(title) DO UPDATE SET 
        price=excluded.price, 
        amount=excluded.amount;
    """, (title, price, amount, link, model_name))
    
    conn.commit()
    conn.close()


def check_checkbox(min_price, max_price, availability, unique_models, cursor):
    if unique_models:
            extra_query = "GROUP BY model_name HAVING MIN(price)"
    else:
        extra_query = ""
    
    if availability:
        query = (f'SELECT * FROM goods WHERE price >= ? AND price <= ? '
                    f'AND amount != "Нет в наличии" {extra_query} '
                    'ORDER BY price ASC')
        cursor.execute(query, (min_price, max_price))
    else:
        query = (f'SELECT * FROM goods WHERE price >= ? AND price <= ? '
                    f'{extra_query} ORDER BY price ASC')
        cursor.execute(query, (min_price, max_price))
    
    return cursor