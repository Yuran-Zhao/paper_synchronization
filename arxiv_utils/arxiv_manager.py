import re
import os
import urllib.request
import requests as rq
from bs4 import BeautifulSoup as bs
from urllib.parse import urlencode


class arxivManager(object):
    def __init__(self, arxiv_number=None, papername=None):
        super().__init__()
        self.headers = {
            "User-Agent":
            "Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0"
        }
        assert (arxiv_number is not None) or (papername is not None)
        if arxiv_number is None:
            assert papername is not None
            self.arxiv_number = self.obtain_arxiv_number_by_papername(papername)
            if self.arxiv_number is None:
                exit(1)
        else:
            self.arxiv_number = arxiv_number
        soup = self.obtain_soup(self.arxiv_number)
        self.papername = papername if papername is not None else self.parse_papername(
            soup)
        self.authors = self.parse_authors(soup)
        self.submission_time = self.parse_submission_time(soup)

    def obtain_arxiv_number_by_papername(self, papername):
        query = urlencode({'query': papername})
        url = 'https://arxiv.org/search/?{}&searchtype=all&source=header'.format(
            query)
        resp = rq.get(url, headers=self.headers)
        soup = bs(resp.content, 'lxml')
        return self.parse_arxiv_number(soup)

    def parse_arxiv_number(self, soup):
        tmp = soup.find_all('p',
                            class_='list-title is-inline-block')[0].get_text()
        raw = tmp.split('\n')[0]
        pattern = re.compile(r"arXiv:(\d+.\d+)")
        arxiv = re.findall(pattern, raw)
        if len(arxiv) > 0:
            number = arxiv[0]
        else:
            print("[Error] Fail to get arxiv number.")
            number = None
        return number

    def obtain_soup(self, arxiv_number):
        url = 'https://arxiv.org/abs/{}'.format(arxiv_number)
        resp = rq.get(url, headers=self.headers)
        soup = bs(resp.content, 'lxml')
        return soup

    def parse_papername(self, soup):
        raw_title = soup.find('h1', class_='title mathjax')
        # TODO:
        # parse the text

    def parse_authors(self, soup):
        raw_authors = soup.find('div', class_='authors')
        # TODO:
        # parse the text

    def parse_submission_time(self, soup):
        raw_time = soup.find('div', class_='submission-history')
        # TODO:
        # parse the text

    def download(self, path):
        url = 'https://arxiv.org/pdf/{}'.format(self.arxiv_number)
        try:
            u = urllib.request.urlopen(url)
        except:
            print(
                "Can't obtain the pdf file from arxiv. Maybe need to download manually"
            )
            return False
        with open(os.path.join(path, self.papername + '.pdf')) as fout:
            while True:
                buffer = u.read(8192)
                if buffer:
                    fout.write(buffer)
                else:
                    break
        return True
