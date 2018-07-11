from helpers.url import make_request
from amazonSDK.models import Category, Product


class BestSellers:

    url = 'https://www.amazon.com/Best-Sellers/zgbs'

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
        result = []
        for department in departments:
            if department.find('a'):
                result.append(Category(name=department.find('a').text, url=department.find('a').attrs.get('href', '')))
        return result

    def get_product_list(self, url):
        """
        Return product list from URL
        :param url:
        :return:
        """
        data = make_request(url)
        # bad user-agent from work:
        # user-agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36
        pages = [i for i in data.find_all('li', {'class': 'zg_page'})]
        pass