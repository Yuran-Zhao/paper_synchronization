import os
import urllib.request


def download_from_arxiv(url, papername, path):
    try:
        u = urllib.request.urlopen(url)
    except:
        print(
            "Can't obtain the pdf file from arxiv. Maybe need to download manually"
        )
        return False
    with open(os.path.join(path, papername + '.pdf')) as fout:
        while True:
            buffer = u.read(8192)
            if buffer:
                fout.write(buffer)
            else:
                break
    return True