from flask import Flask, render_template, request
app = Flask(__name__)
@app.route('/', methods=['Get', 'POST'])
def home():
    coin_name = None
    if request.method == 'POST':
        coin_name = request.form['coin']
    return render_template('index.html',coin_name = coin_name )

if __name__ == '__main__':
    app.run(debug=True)
