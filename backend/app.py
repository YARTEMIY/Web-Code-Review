from flask import Flask, render_template, request
import sqlite3


app = Flask(__name__)


def connect_db():
    conn = sqlite3.connect('sqldb.db')
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
        if availability:
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM goods WHERE price >= ? AND price <= ? AND amount != "Нет в наличии" ORDER BY price ASC', (min_price, max_price,))
            data = cursor.fetchall()
            conn.close()
            return render_template('search.html', data=data)
        else:
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM goods WHERE price >= ? AND price <= ? ORDER BY price ASC', (min_price, max_price,))
            data = cursor.fetchall()
            conn.close()
            return render_template('search.html', data=data)
    return render_template('search.html')


if __name__ == '__main__':
    app.run(debug=True)