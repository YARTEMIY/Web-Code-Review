from flask import Flask, render_template, request
import sqlite3
import config
from database import check_checkbox


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

        cur = check_checkbox(min_price, max_price, availability, unique_models, cursor)
        
        data = cur.fetchall()
        conn.close()
        return render_template('search.html', data=data)
    
    return render_template('search.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0')