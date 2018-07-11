class Category:
    #TODO: implement link/method to parent and root category
    #TODO: implement link/method subcategories

    name = None
    url = None

    def __init__(self, name, url):
        self.name = name
        self.url = url


class Product:

    asin = None
    header = None
    price = None

    def __init__(self, asin, header=None, price=None):
        self.asin = asin
        self.header = header
        self.price = price
