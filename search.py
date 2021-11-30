import requests as rq
from bs4 import BeautifulSoup as bs
from urllib.parse import urlencode
import re

headers = {
    "User-Agent":
    "Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0"
}


def get_citedby(papername):
    pass


def gs_search(papername):
    encoded_name = urlencode({'q': papername})
    url = "https://dblp.org/search?{}".format(encoded_name)
    resp = rq.get(url, headers=headers)
    soup = bs(resp.content, 'lxml')