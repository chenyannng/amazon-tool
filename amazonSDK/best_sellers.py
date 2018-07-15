import json
from helpers.url import make_request, full_url_from_relative, get_asin_from_url
from amazonSDK.models import Category, Product
from bs4 import BeautifulSoup


class BestSellers:

    url = 'https://www.amazon.com/Best-Sellers/zgbs'
    categories = []

    def __init__(self, url=None):
        self.url = url if url else self.url

    def get_categories(self, recursive=False):
        """
        Return list of categories in best sellers and URL's
        :param recursive: include sub-categories
        :return: json of category_name:url
        :rtype dict
        """
        #TODO: implement recursive scanning
        print('Collecting Best Sellers categories')
        data = make_request(self.url)
        departments = data.find_all("ul", {"id": "zg_browseRoot"})[0].find_all("li")
        for department in departments:
            if department.find('a'):
                self.categories.append(Category(name=department.find('a').text,
                                                url=department.find('a').attrs.get('href', '')))
        return self.categories

    def populate_all_categories(self):
        """ Populate all categories with products """
        for category in self.categories:
            print('Populating {} category'.format(category.name))
            product_num = self.populate_category(category)
            print('  {} products added'.format(product_num))

    def populate_category(self, category):
        """
        Populate category with products
         :param Category category: category
        """
        data = make_request(category.url)    # retrieve all 100 items on one page
        pages = self._get_pages_from_response(data)

        for page_url in pages:
            data = make_request(page_url)
            products = self._get_products_from_responses(data)
            category.products.extend(products)

    def _get_pages_from_response(self, data):
        """
        Return list of links to all pages with products in category
        :param BeautifulSoup data:
        :return: set of urls to all pages:
        :rtype set
        """
        if data.find('ul', {'class': 'a-pagination'}):      # new style
            pagination = data.find('ul', {'class': 'a-pagination'})
        elif data.find('ol', {'class': 'zg_pagination'}):   # old style
            pagination = data.find('ol', {'class': 'zg_pagination'})
        else:
            raise Exception('Unknown page buttons HTML format!')

        links = [x.get('href') for x in pagination.find_all(href=True)]
        return set(links)

    def _get_products_from_responses(self, data):
        """
        Return list of product from web response
        :param BeautifulSoup data:
        :return:
        :rtype list
        """
        result = []
        if data.find_all('li', {'class': 'zg-item-immersion'}):     # new style
            products = data.find_all('li', {'class': 'zg-item-immersion'})
            for product in products:
                url = full_url_from_relative(product.span.div.a.get('href'))
                header = product.find('div', {'class': 'p13n-sc-truncated'}).text
                asin = None
                price = product.find('span', {'class': 'p13n-sc-price'}).text
                result.append(Product(asin=asin, header=header, price=price, url=url))
        elif data.find_all('div', {'class': 'zg_itemImmersion'}):   # old style
            products = data.find_all('div', {'class': 'zg_itemImmersion'})
            for product in products:
                url = full_url_from_relative(product.a.get('href'))
                header = product.find('div', {'class': 'p13n-sc-truncate'}).text.strip()
                asin = json.loads(product.find('div', {'class': 'p13n-asin'}).get('data-p13n-asin-metadata'))['asin']
                price = product.find('span', {'class': 'p13n-sc-price'}).text
                result.append(Product(asin=asin, header=header, price=price, url=url))
        else:
            raise Exception('Unknown page HTML format while parsing best sellers products')
        return result
