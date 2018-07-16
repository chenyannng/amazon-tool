import requests
from bs4 import BeautifulSoup
from requests.exceptions import RequestException
from amazonSDK.exceptions import CaptchaException

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, sdch, br",
    "Accept-Language": "en-US,en;q=0.8",
}

domain = 'https://www.amazon.com'


class UserAgents:
    default = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36'
    chromeMac = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36'
    chromeMobile = 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Mobile Safari/537.36'


def make_request(url, return_soup=True, max_requests=3, request_number=1, user_agent=UserAgents.default):
    """ Make web request"""

    if request_number > max_requests:
        raise Exception('Reached the max number of requests: {}'.format(max_requests))

    headers.update({"User-Agent": user_agent})

    try:
        response = requests.get(url, headers=headers)
    except RequestException as e:
        print('Error executing request [{} of {}]: {}'.format(request_number, max_requests, e))
        return make_request(url, request_number=request_number+1)

    if response.status_code != 200:
        return None

    if 'Sorry, we just need to make sure you\'re not a robot' in response.text:
        raise CaptchaException('Request blocked by captcha!')

    if return_soup:
        return BeautifulSoup(response.content, "html.parser")

    return response.text


def full_url_from_relative(url):
    """ Convert relative url to absolute """
    url = url.strip('/')
    parts = url.split('/')
    return '/'.join([domain, parts[0], parts[1], parts[2]])


def get_asin_from_url(url):
    """ Extract ASIN from URL """

    if domain not in url:
        raise Exception('Invalid URL! It not contain domain https://www.amazon.com')

    parts = url.lstrip(domain).strip('/').split('/')

    if parts[1] != 'dp':
        raise Exception('Failed to parse URL, ASIN not found!')

    return parts[2]
