import nltk
import os
import sys

sys.path.insert(0, os.path.abspath('.'))

from topverbs.topverbs import check_download_dir  # noqa

download_dir = check_download_dir()
nltk.data.path.append(download_dir)
