from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import config
from parser_1 import parsing


app = Flask(__name__)


def connect_db():
    conn = sqlite3.connect(config.dbname)
    return conn


@app.route('/')
def show_data():
    return render_template('index.html')


@app.route('/search/screwdriver', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        min_price = request.form['min_price']
        max_price = request.form['max_price']
        availability = request.form.get('availability')
        unique_models = request.form.get('unique_models')
        
        conn = connect_db()
        cursor = conn.cursor()
        
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
        
        data = cursor.fetchall()
        conn.close()
        return render_template('search.html', data=data)
    
    return render_template('search.html')


#@app.route('/update_db', methods=['POST'])
#def update_db():
#    parsing()
#    return redirect(url_for('show_data'))


if __name__ == '__main__':
    app.run(host='0.0.0.0')