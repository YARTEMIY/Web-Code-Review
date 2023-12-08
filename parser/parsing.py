from bs4 import BeautifulSoup
from selenium import webdriver
import sqlite3
import os


def get_product_instrumentorugie(page):
    driver = webdriver.Chrome()
    driver.get(f'https://instrument-orugie.ru/catalog/elektroinstrument/shurupoverti/akkumulyatornye_shurupoverty/?PAGEN_1={page}')
    driver.implicitly_wait(10)
    html = driver.execute_script('return document.body.innerHTML')
    driver.close()

    bsObj = BeautifulSoup(html, 'html.parser')
    found_goods = bsObj.find_all('div', {'class' : 'catalog_item_wrapp item'})

    all_goods = []

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
        
        all_goods.append((title, price, amount, link))

        add_goods(title, price, amount, link)

    return all_goods


def get_product_vseinstrumenti(page):
    driver = webdriver.Chrome()
    driver.get(f'https://www.vseinstrumenti.ru/category/akkumulyatornye-dreli-shurupoverty-15/page{page}/')
    driver.implicitly_wait(10)
    html = driver.execute_script('return document.body.innerHTML')
    driver.close()

    bsObj = BeautifulSoup(html, 'html.parser')
    found_goods = bsObj.find_all('div', {'class' : 'dGMJLz fSNq2j Ppy5qY LXySrk'})

    all_goods = []

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
        
        all_goods.append((title, price, amount, link))

        add_goods(title, price, amount, link)

    return all_goods


def create_tables(cur, conn):
    cur.execute('DROP TABLE IF EXISTS goods')
    
    cur.execute(''' 
    CREATE TABLE goods (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        price INTEGER,
        amount TEXT,
        link TEXT
    )
    ''')
    
    conn.commit()


def add_goods(title, price, amount, link):
    conn = sqlite3.connect(f"{os.path.abspath("bd/sqldb.db")}")

    cur = conn.cursor()
    cur.execute(f'''INSERT INTO goods (title, price, amount, link) VALUES 
                ('{title}', '{price}', '{amount}', '{link}')''')
    
    conn.commit()
    conn.close()


def parsing():
    page = 1

    break_point = get_product_instrumentorugie(page)
    while True:
        page += 1
        all_goods = get_product_instrumentorugie(page)
        if all_goods == break_point:
            page = 1
            break

    break_point = get_product_vseinstrumenti(page)
    while True:
        page += 1
        all_goods = get_product_vseinstrumenti(page)
        if all_goods == break_point:
            break


with sqlite3.connect(f"{os.path.abspath("bd/sqldb.db")}") as conn:
    cur = conn.cursor()
    create_tables(cur, conn)

parsing()