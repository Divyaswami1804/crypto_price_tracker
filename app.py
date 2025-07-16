from flask import Flask, render_template, request
import requests  #API call from http
app = Flask(__name__)
@app.route('/', methods=['Get', 'POST'])
def home():
    coin_name = None
    price = None

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
            else:
                price = 'Invalid coin name'
        else:
            price = 'API request failed'


    return render_template('index.html',coin_name = coin_name , price = price )

if __name__ == '__main__':
    app.run(debug=True)
