from bs4 import BeautifulSoup
from selenium import webdriver
from database import add_good, create_tables
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

    for catalog_item in found_goods:
        title = catalog_item.find('div', {'class' : 'item-title'}).text.strip()

        try:
            price = catalog_item.find('span', {'class' : 'price_value'}).text.strip().replace(' ', '')
        except Exception:
            price = -1

        amount = catalog_item.find('span', {'class' : 'value'}).text.strip()

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
    time.sleep(10)
    driver.implicitly_wait(10)
    html = driver.execute_script('return document.body.innerHTML')
    driver.close()

    all_goods = []

    bsObj = BeautifulSoup(html, 'html.parser')
    found_goods = bsObj.find_all('div', {'class' : 'dGMJLz fSNq2j Ppy5qY LXySrk'})

    for catalog_item in found_goods:
        title = catalog_item.find('span', {'class' : 'typography text v2 -no-margin'}).text.strip()

        try:
            price = catalog_item.find('p', {'class' : 'typography heading v5 -no-margin R34yPj ACNQm3'}).text.strip()
        except Exception:
            price = -1
        else:
            price = catalog_item.find('p', {'class' : 'typography heading v5 -no-margin R34yPj ACNQm3'}).text.strip()
            price = price.replace(' ', '')
            price = price.replace('\xa0', '')
            price = price[:-2]

        try:
            amount = catalog_item.find('p', {'class' : 'SyU0Xg'}).text.strip()
        except Exception:
            amount = 'Нет в наличии'
        else:
            amount = catalog_item.find('p', {'class' : 'SyU0Xg'}).text.strip()
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


def iterate_through_pages(website):
    page = 1

    break_point = website(page)
    while True:
        page += 1
        all_goods = website(page)
        if all_goods == break_point or len(all_goods) == 0:
            break


def parsing():
    with sqlite3.connect(config.dbname) as conn:
        cur = conn.cursor()
        create_tables(cur, conn)

    iterate_through_pages(get_product_instrumentorugie)
    iterate_through_pages(get_product_vseinstrumenti)