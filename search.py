import requests as rq
from bs4 import BeautifulSoup as bs
from urllib.parse import urlencode
import re

headers = {
    "User-Agent":
    "Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0"
}


def get_papername_by_arxiv_number(arxiv_number):
    pass


def get_arxiv_number_by_papername(papername):
    query = urlencode({'query': papername})
    url = 'https://arxiv.org/search/?{}&searchtype=all&source=header'.format(
        query)
    resp = rq.get(url, headers=headers)
    soup = bs(resp.content, 'lxml')


def get_arxiv_number_by_soup(soup):
    tmp = soup.find_all('p', class_='list-title is-inline-block')[0].get_text()
    raw = tmp.split('\n')[0]
    pattern = re.compile(r"arXiv:(\d+.\d+)")
    arxiv = re.findall(pattern, raw)
    if len(arxiv) > 0:
        number = arxiv[0]
    else:
        print("[Error] Fail to get arxiv number.")
        number = None
    return number


def get_authors_by_soup(soup):
    tmp = soup.find_all('p', class_='authors')[0].get_text()
    raw_authors = tmp.strip('\n').split('\n')[1:]
    authors = [item.strip() for item in raw_authors if item.strip() != '']
    return authors


def search_paper(papername):
    authors, year = dblp_search(papername)
    citation = gs_search(papername)
    return authors, year, citation


def dblp_search(papername):
    encoded_name = urlencode({'q': papername})
    url = "https://dblp.org/search?{}".format(encoded_name)
    resp = rq.get(url, headers=headers)
    soup = bs(resp.content, 'lxml')


def gs_search(papername):
    encoded_name = urlencode({'q': papername})
    url = "https://dblp.org/search?{}".format(encoded_name)
    resp = rq.get(url, headers=headers)
    soup = bs(resp.content, 'lxml')