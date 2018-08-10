import json
import os
import shutil
from git import Repo

from console import colored_print


def make_list_flat(_list):
    """ [(1,2), (3,4)] -> [1, 2, 3, 4]"""
    return sum([list(item) for item in _list], [])


def convert_list_of_tuples_to_json_dict(_list):
    dictionary = dict((word, count) for word, count in _list)
    return json.dumps(dictionary)


def get_file_names_from_path(path, ext='py'):
    file_names = []
    for dir_name, dirs, files in os.walk(path, topdown=True):
        for file in files:
            if file.endswith(f'.{ext}'):
                file_names.append(os.path.join(dir_name, file))
    return file_names


def get_file_content(filename):
    with open(filename, 'r', encoding='utf-8') as attempt_handler:
        file_content = attempt_handler.read()
    return file_content


def clone_to_dir(git_url, repo_dir):
    repo = Repo.clone_from(git_url, repo_dir)
    colored_print(f"Repository cloned to path: {repo.common_dir.strip('.git')}")


def delete_created_repo_dir(repo_dir):
    shutil.rmtree(repo_dir)
    colored_print(f"Remove temporary dir: {repo_dir}")
