import re

from bs4.element import Comment
from arxiv_utils import arxivManager


class paperManager(object):
    def __init__(self, all_lines):
        tmp = all_lines.split('\n')
        all_lines = [line for line in tmp if line.strip() != '']
        self.n_lines = len(all_lines)
        self.markers = [0] * self.n_lines
        self.markers[0] = 1
        # self.title_pattern = re.compile(r"##### [\d*. ]?([a-zA-Z0-9 -?:!]+)")
        self.title = all_lines[0]

        self.arxiv_number_pattern = re.compile(r'\d+.\d+')
        self.arxiv_number = self.parse_arxiv_number(all_lines)

        self.tag_pattern = re.compile(r'Tags: (.*)')
        self.tag = self.parse_tag(all_lines)

        # self.comment_pattern = re.compile(r'Comment: (.*)')
        self.comment = self.parse_comment(all_lines)

        self.arxiv_info = arxivManager(arxiv_number=self.arxiv_number,
                                       papername=self.title)
        self.authors = self.arxiv_info.authors
        self.submission_date = self.arxiv_info.submission_date
        self.arxiv_number = self.arxiv_info.arxiv_number
        self.title = self.arxiv_info.papername

    # def parse_title(self, lines):
    #     for i in range(self.n_lines):
    #         if self.markers[i] == 1:
    #             continue
    #         papername = re.findall(self.title_pattern, lines[i])
    #         if len(papername) > 0:
    #             self.markers[i] = 1
    #             return papername[0]
    #     return None

    def parse_arxiv_number(self, lines):
        for i in range(self.n_lines):
            if self.markers[i] == 1:
                continue
            arxiv_number = re.findall(self.arxiv_number_pattern, lines[i])
            if len(arxiv_number) > 0:
                self.markers[i] = 1
                return arxiv_number[0]
        return None

    def parse_tag(self, lines):
        for i in range(self.n_lines):
            if self.markers[i] == 1:
                continue
            tag = re.findall(self.tag_pattern, lines[i])
            if len(tag) > 0:
                self.markers[i] = 1
                return tag[0].split(', ')
        return ''

    def parse_comment(self, lines):
        comments = []
        for i in range(self.n_lines):
            if self.markers[i] == 0:
                comments.append(lines[i] + '\n')
        # TODO: in order to look better so add another blank line
        return '' if comments == [] else '\n'.join(comments)

    def format(self):
        title = '##### {} (Authors: {}; Submission Date: {})\n{}'.format(
            self.title, ', '.join(self.authors), self.submission_date,
            self.arxiv_number)
        tag = 'Tags: {}'.format(', '.join(self.tag))
        return [title, tag, self.comment]

    def __repr__(self) -> str:
        return '\n'.join(self.format())
