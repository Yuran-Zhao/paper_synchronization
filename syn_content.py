import os
import time
from db_utils import MD5DB, paperDB
from hashlib import md5
import re
from tqdm import tqdm


def synchronize_content(root, interval):
    db = MD5DB(root)
    while True:
        for filename in os.listdir(root):
            if os.path.splitext(filename)[-1] == '.md':
                prefix = os.path.splitext(filename)[0]
                with open(os.path.join(root, filename), 'r',
                          encoding='utf8') as fin:
                    content = fin.read()
                cur_md5 = md5(content.encode('utf8')).hexdigest()
                if db.check_modification(filename, cur_md5):
                    update(content, prefix)
                    db.update(filename, cur_md5)
        time.sleep(interval)


def update(root, prefix, content):
    paper_db = paperDB(root, prefix)
    previous_papers = paper_db.get_all_saved_papers()
    lines = content.split('\n')
    cur_papers = find_papers_in_file(lines)
    # ignore the possible deleted papers
    new_papers = set(cur_papers) - set(previous_papers)
    for paper in new_papers:
        paper_db.insert(paper)


def find_papers_in_file(lines):
    pattern = re.compile(r"##### [\d*. ]?([a-zA-Z0-9 -?:!]+) \([0-9a-zA-Z]+")
    papers = []
    for line in lines:
        papername = re.findall(pattern, line)
        if len(papername) > 0:
            papers.append(papername[0].strip())
    return papers
