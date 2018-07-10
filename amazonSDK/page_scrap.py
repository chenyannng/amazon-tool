import requests
from bs4 import BeautifulSoup


def parse_page(url):
    content = requests.get(url).content
    return BeautifulSoup(content, "html.parser")
