from amazonSDK.page_scrap import parse_page


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
        data = parse_page(self.url)
        departments = data.find_all("ul", {"id": "zg_browseRoot"})[0].find_all("li")
        result = {}
        for department in departments:
            if department.find('a'):
                result.update({department.find('a').text: department.find('a').attrs.get('href', '')})
        return result

    def get_product_list(self, url):
        """
        Return product list from URL
        :param url:
        :return:
        """
        data = parse_page(url)
        data = data.find('ul', {'class': 'a-pagination'}).find('li', {'class': 'a-last'})
        pass