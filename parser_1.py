from bs4 import BeautifulSoup
from selenium import webdriver
import sqlite3
import time
import config


model = {0: 'insert your text'}


def get_model_name(title):
    list = title.split()[2:]
    model = ' '.join(list).lower()
    return model


def add_model_item(name):
    if name not in model.values():
        model[max(model.keys()) + 1] = name


def get_product_instrumentorugie(page):
    driver = webdriver.Chrome()
    driver.get(f'https://instrument-orugie.ru/catalog/elektroinstrument/shurupoverti/akkumulyatornye_shurupoverty/?PAGEN_1={page}')
    driver.implicitly_wait(10)
    html = driver.execute_script('return document.body.innerHTML')
    driver.close()

    all_goods = []

    bsObj = BeautifulSoup(html, 'html.parser')
    found_goods = bsObj.find_all('div', {'class' : 'catalog_item_wrapp item'})

    for i in found_goods:
        title = i.find('div', {'class' : 'item-title'}).text.strip()

        try:
            price = i.find('span', {'class' : 'price_value'}).text.strip()
        except Exception:
            price = -1
        else:
            price = i.find('span', {'class' : 'price_value'}).text.strip()
            price = price.replace(' ', '')

        amount = i.find('span', {'class' : 'value'}).text.strip()

        link = f'https://instrument-orugie.ru/catalog/?q={title}&s=Найти'

        model_name = get_model_name(title)

        add_model_item(model_name)
        
        good = (title, price, amount, link, model_name)

        all_goods.append(good)

        add_good(good)

    return all_goods


def get_product_vseinstrumenti(page):
    driver = webdriver.Chrome()
    driver.get(f'https://www.vseinstrumenti.ru/category/akkumulyatornye-dreli-shurupoverty-15/page{page}/')
    time.sleep(15)
    driver.implicitly_wait(10)
    html = driver.execute_script('return document.body.innerHTML')
    driver.close()

    all_goods = []

    bsObj = BeautifulSoup(html, 'html.parser')
    found_goods = bsObj.find_all('div', {'class' : 'dGMJLz fSNq2j Ppy5qY LXySrk'})

    for i in found_goods:
        title = i.find('span', {'class' : 'typography text v2 -no-margin'}).text.strip()

        try:
            price = i.find('p', {'class' : 'typography heading v5 -no-margin R34yPj ACNQm3'}).text.strip()
        except Exception:
            price = -1
        else:
            price = i.find('p', {'class' : 'typography heading v5 -no-margin R34yPj ACNQm3'}).text.strip()
            price = price.replace(' ', '')
            price = price.replace('\xa0', '')
            price = price[:-2]

        try:
            amount = i.find('p', {'class' : 'SyU0Xg'}).text.strip()
        except Exception:
            amount = 'Нет в наличии'
        else:
            amount = i.find('p', {'class' : 'SyU0Xg'}).text.strip()
            amount = amount.replace('\n', '')
            amount = amount.replace('    ', ' ')

        link = f'https://www.vseinstrumenti.ru/search/?what={title}'

        flag = True
        for name in model.values():
            index = title.lower().find(name)
            if index != -1:
                if index == len(title) - len(name):
                    model_name = name
                    flag = False
                    break
        if flag:
            add_model_item(title.lower())
            model_name = model[max(model.keys())]
        
        good = (title, price, amount, link, model_name)

        all_goods.append(good)

        add_good(good)

    return all_goods


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


def parsing():
    with sqlite3.connect(config.dbname) as conn:
        cur = conn.cursor()
        create_tables(cur, conn)

    page = 1

    break_point = get_product_instrumentorugie(page)
    while True:
        page += 1
        all_goods = get_product_instrumentorugie(page)
        if all_goods == break_point or len(all_goods) == 0:
            page = 1
            break

    break_point = get_product_vseinstrumenti(page)
    while True:
        page += 1
        all_goods = get_product_vseinstrumenti(page)
        if all_goods == break_point or len(all_goods) == 0:
            page = 1
            break