import os
from utils import detect_modification
import time
from utils import MD5DB
from hashlib import md5


def synchronize_content(root, interval):
    db = MD5DB(root)
    while True:
        for filename in os.listdir(root):
            if os.path.splitext(filename)[-1] == '.md':
                with open(filename, 'r', encoding='utf8') as fin:
                    content = fin.read()
                cur_md5 = md5(content.encode('utf8')).hexdigest()
                if db.check_modification(filename, cur_md5):
                    update(content)
                    db.update(filename, cur_md5)
        time.sleep(interval)


def update(content):
    lines = content.split('\n')
