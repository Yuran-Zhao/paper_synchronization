import re
import os
import logging
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
        if soup is None:
            logging.warning("Can't build the arxivMananer Object")
            exit(1)
        self.papername = self.parse_papername(soup)
        self.authors = self.parse_authors(soup)
        self.submission_date = self.parse_submission_date(soup)

    def __repr__(self) -> str:
        return 'Title: {}\nAuthors{}\nSubmission Date{}'.format(
            self.papername, self.authors, self.submission_date)

    def obtain_arxiv_number_by_papername(self, papername):
        query = urlencode({'query': papername})
        url = 'https://arxiv.org/search/?{}&searchtype=all&source=header'.format(
            query)
        try:
            resp = rq.get(url, headers=self.headers)
            soup = bs(resp.content, 'lxml')
            arxiv_number = self.parse_arxiv_number(soup)
        except Exception as e:
            # MAYBE this paper hasn't been submitted to arXiv.org
            # or the format of HTML has been modified
            logging.warning(e)
            arxiv_number = None
        return arxiv_number

    def parse_arxiv_number(self, soup):
        try:
            tmp = soup.find_all(
                'p', class_='list-title is-inline-block')[0].get_text()
            raw = tmp.split('\n')[0]
            pattern = re.compile(r"arXiv:(\d+.\d+)")
            arxiv = re.findall(pattern, raw)
            if len(arxiv) > 0:
                arxiv_number = arxiv[0]
            else:
                logging.warning("Can not get arxiv number of {}.".format(
                    self.papername))
                arxiv_number = None
        except Exception as e:
            # MAYBE this paper hasn't been submitted to arXiv.org
            # or the format of HTML has been modified
            logging.warning(e)
            arxiv_number = None
        return arxiv_number

    def obtain_soup(self, arxiv_number):
        url = 'https://arxiv.org/abs/{}'.format(arxiv_number)
        try:
            resp = rq.get(url, headers=self.headers)
            soup = bs(resp.content, 'lxml')
        except Exception as e:
            soup = None
        return soup

    def parse_papername(self, soup):
        try:
            raw_title = soup.find('h1', class_='title mathjax').get_text()
            pattern = re.compile(r'Title:(.+)')
            title = re.findall(pattern, raw_title)
            if len(title) > 0:
                return title[0]
            logging.warning("Can not get the name of paper of {}.".format(
                self.arxiv_number))
        except Exception as e:
            logging.warning(e)
        return None

    def parse_authors(self, soup):
        try:
            raw_authors = soup.find('div', class_='authors').get_text()
            pattern = re.compile(r'Authors:(.+)')
            authors = re.findall(pattern, raw_authors)
            if len(authors) > 0:
                return authors[0].split(', ')
            logging.warning("Can not get the authors of paper of {}.".format(
                self.arxiv_number))
        except Exception as e:
            logging.warning(e)
        return None

    def parse_submission_date(self, soup):
        try:
            raw_time = soup.find('div', class_='submission-history').get_text()
            time_pattern = re.compile(r'.* (\d+ [a-zA-Z]+ \d+).*')
            time = re.findall(time_pattern, raw_time)
            if len(time) > 0:
                return time[0]
            logging.warning(
                "Can not get the submission date of paper of {}.".format(
                    self.arxiv_number))
        except Exception as e:
            logging.warning(e)
        return None

    def download(self, path):
        url = 'https://arxiv.org/pdf/{}'.format(self.arxiv_number)
        try:
            u = urllib.request.urlopen(url)
        except Exception as e:
            logging.warning(
                "Can't obtain the pdf file from arxiv. Maybe need to download manually"
            )
            logging.warning(e)
            return False
        with open(os.path.join(path, self.papername + '.pdf')) as fout:
            while True:
                buffer = u.read(8192)
                if buffer:
                    fout.write(buffer)
                else:
                    break
        return True
