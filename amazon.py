from flask import Flask, render_template, jsonify
from amazonSDK.best_sellers import BestSellers
app = Flask(__name__)


@app.route('/')
def page_home():
    return render_template('home.html')


@app.route('/about')
def page_about():
    return render_template('about.html')


@app.route('/graph_sample')
def page_graph():
    from bokeh.plotting import figure
    from bokeh.io import output_file, show, save
    import pandas

    dataframe = pandas.read_csv('http://pythonhow.com/data/bachelors.csv')
    x = dataframe['Year']
    y = dataframe['Engineering']

    output_file("templates/graph.html")
    f = figure(plot_width=1024, plot_height=700)    # create figure object
    f.title.text = 'Test data'
    f.title.text_color = 'Red'
    f.line(x, y)
    save(f)
    return render_template('graph.html')


@app.route('/best_sellers')
def page_best_sellers():
    bs = BestSellers()
    categories = bs.get_bs_categories()
    for category, url in categories.items():
        print('Processing {} category'.format(category))
        products = bs.get_product_list(url)
        print('{} products found in {}'.format(len(products), category))
    return render_template('best_sellers.html', categories=categories)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
