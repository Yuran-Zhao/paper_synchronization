import re

from bs4.element import Comment
from arxiv_utils import arxivManager


class paperManager(object):
    def __init__(self, all_lines):
        self.title_pattern = re.compile(
            r"##### [\d*. ]?([a-zA-Z0-9 -?:!]+) \([0-9a-zA-Z]+")
        self.title = self.parse_title(all_lines)

        self.arxiv_number_pattern = re.compile(r'\d+.\d+')
        self.arxiv_number = self.parse_arxiv_number(all_lines)

        self.tag_pattern = re.compile(r'Tags: ([a-zA-z ]*)')
        self.tags = self.parse_tags(all_lines)

        self.comment_pattern = re.compile(r'Comment: (.*)')
        self.comment = self.parse_comment(all_lines)

        self.arxiv_info = arxivManager(arxiv_number=self.arxiv_number,
                                       papername=self.title)
        self.authors = self.arxiv_info.authors
        self.submission_date = self.arxiv_info.submission_date
        self.arxiv_number = self.arxiv_info.arxiv_number
        self.title = self.arxiv_info.papername

    def parse_title(self, lines):
        for line in lines:
            papername = re.findall(self.title_pattern, line)
            if len(papername) > 0:
                return papername[0]
        return None

    def parse_arxiv_number(self, lines):
        for line in lines:
            arxiv_number = re.findall(self.arxiv_number_pattern, line)
            if len(arxiv_number) > 0:
                return arxiv_number[0]
        return None

    def parse_tags(self, lines):
        for line in lines:
            tags = re.findall(self.tag_pattern, line)
            if len(tags) > 0:
                return tags[0].split(' ')
        return None

    def parse_comment(self, lines):
        for line in lines:
            comment = re.findall(self.comment_pattern, line)
            if len(comment) > 0:
                return comment[0]
        return None

    def format(self):
        title = '##### {} (arXiv: {}, Authors: {}, Submission Date: {})'.format(
            self.title, self.arxiv_number, ', '.join(self.authors),
            self.submission_date)
        tags = 'Tags: {}'.format(' '.join(self.tags))
        comment = 'Comment: {}'.format(self.comment)
        return [title, tags, comment]
