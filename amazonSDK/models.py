class Product:

    asin = None
    header = None
    price = None
    url = None

    def __init__(self, asin=None, header=None, price=None, url=None):
        self.asin = asin
        self.header = header
        self.price = float(price) if type(price) in [int, float] else float(price.strip('$'))
        self.url = url

    def from_zg_item_immersion(self, data):
        """
        Form Product object from zg_itemImmersion HTML class
        Amazon has two types of responses with different HTML layout
        """
        return set


class Category:
    #TODO: implement link/method to parent and root category
    #TODO: implement link/method subcategories

    name = None
    url = None
    products = []     # type: list[Product]

    def __init__(self, name, url):
        self.name = name
        self.url = url
