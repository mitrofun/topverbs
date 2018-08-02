import os
import sys

import pytest

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

sys.path.insert(0, ROOT_DIR)
sys.path.insert(0, os.path.join(ROOT_DIR, 'topverbs'))

collect_ignore = ["setup.py"]


@pytest.fixture
def root_path():
    return os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))


@pytest.fixture
def fixtures_path(root_path):
    fixtures = os.path.join(root_path, 'fixtures')
    return fixtures


@pytest.fixture
def file_with_code_path(fixtures_path):
    return os.path.join(fixtures_path, 'hello.py')
