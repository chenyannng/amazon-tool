from helpers.url import make_request, full_url_from_relative, get_asin_from_url
from amazonSDK.models import Category, Product


class BestSellers:

    url = 'https://www.amazon.com/Best-Sellers/zgbs'
    categories = []

    def __init__(self, url=None):
        self.url = url if url else self.url

    def get_bs_categories(self, recursive=False):
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
            self.populate_category(category)

    def populate_category(self, category):
        """
        Populate category with products
         :param Category category: category
        """
        data = make_request(category.url)    # retrieve all 100 items on one page

        #TODO: Add second page processing here
        #pages = [i for i in data.find_all('li', {'class': 'zg_page'})]

        #items = data.find_all('span', {'class': 'a-list-item'})
        items = data.find_all('li', {'class': 'zg-item-immersion'})

        for item in items:
            # zg-item-immersion vs zg_itemImmersion
            category.products.append(Product().from_zg_item_immersion(data=item))


        """
            url = full_url_from_relative(item.find('a', {'class': 'a-link-normal'})['href'])
            result.append(Product(asin=get_asin_from_url(url),
                                  header=item.find('div', {'class': 'p13n-sc-truncate'}).text.strip(),
                                  price=item.find('span', {'class': 'p13n-sc-price'}).text.strip(),
                                  url=url,))
        """
        pass
