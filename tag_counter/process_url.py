from bs4 import BeautifulSoup
from requests.exceptions import ConnectionError
from loguru import logger
import requests
import re


def url_format(url):
    """Returns a fully qualified url sorta"""
    if not re.match('(?:http|https)://', url):
        return 'http://{}'.format(url)
    return url


def url_name(url):
    """Returns the name of the url provided"""
    return re.findall(R"[^.]*\.[^.]{2,3}(?:\.[^.]{2,3})?$", url)[0]


def count_tags(full_url) -> {}:
    """Returns all the tags from the url html along with the count of occurrences"""

    try:
        soup = BeautifulSoup(requests.get(full_url).text, 'html.parser')
        s = {tag.name: len(soup.find_all(tag.name)) for tag in soup.findAll()}
    except ConnectionError as ce:
        logger.error('Failed to establish a connection \n Exception:{}'.format(ce))
    except Exception as e:
        logger.error('Something bad happened \n Exception:{}'.format(e))
    else:
        return s
