from flask import Flask, render_template, request
import requests
import time

app = Flask(__name__)

# Simple in-memory cache
crypto_cache = {}

@app.route("/", methods=["GET", "POST"])
def index():
    crypto_price = None
    error = None

    if request.method == "POST":
        crypto = request.form["crypto"].lower()
        current_time = time.time()

        # If we have cached and it's fresh (60 sec)
        if crypto in crypto_cache and current_time - crypto_cache[crypto]["timestamp"] < 60:
            crypto_price = crypto_cache[crypto]["price"]
        else:
            url = f"https://api.coingecko.com/api/v3/simple/price?ids={crypto}&vs_currencies=usd"
            try:
                response = requests.get(url)
                if response.status_code == 200:
                    data = response.json()
                    crypto_price = data[crypto]["usd"]

                    # Cache it
                    crypto_cache[crypto] = {
                        "price": crypto_price,
                        "timestamp": current_time
                    }

                    # Sleep to avoid hitting limit too fast
                    time.sleep(2)

                else:
                    error = f"API Error: {response.status_code}"
            except Exception as e:
                error = str(e)

    return render_template("index.html", crypto_price=crypto_price, error=error)

