import requests
from bs4 import BeautifulSoup
from requests.exceptions import RequestException

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, sdch, br",
    "Accept-Language": "en-US,en;q=0.8",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36",
}


def make_request(url, return_soup=True, max_requests=2, request_number=1):
    """ Make web request"""

    if request_number > max_requests:
        raise Exception('Reached the max number of requests: {}'.format(max_requests))

    try:
        response = requests.get(url, headers=headers)
    except RequestException as e:
        print('Error executing request [{} of {}]: {}'.format(request_number, max_requests, e))
        return make_request(url, request_number=request_number+1)

    if response.status_code != 200:
        return None

    if return_soup:
        return BeautifulSoup(response.content, "html.parser")

    return response.text
