class Product:

    asin = None
    header = None
    price = None
    url = None

    def __init__(self, asin=None, header=None, price=None, url=None):
        self.asin = asin
        self.header = header
        self.url = url
        self.set_price(price)

    def set_price(self, price):
        if price:
            self.price = float(price) if type(price) in [int, float] else float(price.strip('$'))
        else:
            self.price = None

class Category:
    #TODO: implement link/method to parent and root category
    #TODO: implement link/method subcategories

    name = None
    url = None
    products = []     # type: list[Product]

    def __init__(self, name, url):
        self.name = name
        self.url = url
