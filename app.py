from flask import Flask, render_template, request
import requests  #API call from http
import sqlite3
app = Flask(__name__)
@app.route('/', methods=['Get', 'POST'])
def home():
    coin_name = None
    price = None
    last_searches =[]
    #connect to DB
    conn = sqlite3.connect('crypto.db')
    cur = conn.cursor()

    if request.method == 'POST':
        coin_name = request.form['coin'].lower()

        #build coingecko API url
        url = f'https://api.coingecko.com/api/v3/simple/price?ids={coin_name}&vs_currencies=usd'

        #call the API
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if coin_name in data:
                price = data[coin_name]['usd']

                # Save to DB
                cur.execute("INSERT INTO searches (coin_name, price) VALUES (?, ?)", (coin_name, price))

                conn.commit()

            else:
                price = 'Invalid coin name'
        else:
            price = 'API request failed'

            # Always fetch last 5 searches
            cur.execute("SELECT coin_name, price, timestamp FROM searches ORDER BY id DESC LIMIT 5")
            last_searches = cur.fetchall()

            conn.close()

    return render_template('index.html',coin_name = coin_name , price = price, last_searches = last_searches )

if __name__ == '__main__':
    app.run(debug=True)
