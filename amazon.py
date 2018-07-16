from flask import Flask, render_template, jsonify, request
from amazonSDK.best_sellers import BestSellers
from amazonSDK.exceptions import CaptchaException
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


@app.route('/_best_sellers_populate')
def page_best_sellers_populate():
    bs = BestSellers()
    try:
        bs.get_categories()
        bs.populate_all_categories()
        for category in bs.categories:
            print('Processing {} category'.format(category.name))
            products = bs.get_product_list(category.url)
            print('{} products found in {}'.format(len(products), category.name))
        return jsonify(result='Population completed')
    except CaptchaException as e:
        return jsonify(result=e.message)
    except Exception as e:
        return jsonify(result='Unknown error! Please check console logs')


@app.route('/best_sellers')
def page_best_sellers():
    return render_template('best_sellers.html', categories={})


@app.route('/best_sellers_results', methods=['POST'])
def page_best_sellers_results():
    price_min = request.form['price_min']
    price_max = request.form['price_max']
    return render_template('best_sellers_results.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
