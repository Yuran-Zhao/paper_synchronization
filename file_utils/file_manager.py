import os
import re
import hashlib

from paper_utils import paperManager


class fileManager(object):
    def __init__(self, mdfile):
        self.file = mdfile
        self.md5 = None
        self.papers = self.devide_papers()
        self.generate_md5()

    def devide_papers(self):
        with open(self.file, 'r', encoding='utf8') as fin:
            lines = fin.read().split('##### ')
        # lines is a list, while the '' signals a new block
        # devider = [idx for idx, item in enumerate(lines) if item == '']
        # cnt, i = 0, 0
        # papers = []
        # while i < len(lines):
        #     papers.append(paperManager(lines[i:devider[cnt]]))
        #     i = devider[cnt] + 1
        #     cnt += 1

        papers = []
        for line in lines:
            if line == '':
                continue
            papers.append(paperManager(line))
        return papers

    def format_file(self):
        lines = []
        for paper in self.papers:
            lines += paper.format()
            # lines += ['']
        with open(self.file, 'w', encoding='utf8') as fout:
            for line in lines:
                fout.write(line + '\n')
                fout.write('\n')

    def generate_md5(self):
        self.format_file()
        with open(self.file, 'rb') as fin:
            data = fin.read()
        self.md5 = hashlib.md5(data).hexdigest()