from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def page_home():
    return render_template('home.html')


@app.route('/about')
def page_about():
    return render_template('about.html')


if __name__ == '__main__':
    app.run(debug=True, port=5000)
