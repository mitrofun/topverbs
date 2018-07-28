import sys

import os
import ast
import nltk
import json
import argparse
import collections

import logging
import logging.config

from nltk import pos_tag

DEBUG = os.environ.get('DEBUG') == 'true'

if DEBUG:
    logging.config.fileConfig('log.conf')

logger = logging.getLogger(__name__)


class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    RED = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def make_list_flat(_list):
    """ [(1,2), (3,4)] -> [1, 2, 3, 4]"""
    return sum([list(item) for item in _list], [])


def is_verb(word):
    """Check what word is verb"""
    if not word:
        return False
    pos_info = pos_tag([word])
    return pos_info[0][1] == 'VB'


def get_file_names_from_path(path):
    file_names = []
    for dir_name, dirs, files in os.walk(path, topdown=True):
        for file in files:
            if file.endswith('.py'):
                file_names.append(os.path.join(dir_name, file))
                if len(file_names) == 100:
                    break
    logger.debug('total %s files' % len(file_names))
    return file_names


def get_file_content(filename):
    """
    Get content from file
    :param filename: name file, str
    :return: content from file
    """
    with open(filename, 'r', encoding='utf-8') as attempt_handler:
        main_file_content = attempt_handler.read()
    return main_file_content


def get_syntax_trees_from_files(file_names):
    trees = []

    for filename in file_names:
        file_content = get_file_content(filename)
        try:
            tree = ast.parse(file_content)
        except SyntaxError as e:
            logger.debug(e)
            continue
        trees.append(tree)

    return trees


def get_all_names(tree):
    return [node.id for node in ast.walk(tree) if isinstance(node, ast.Name)]


def get_verbs_from_function_name(function_name):
    """
    Get verbs from string
    :return list with verbs
    """
    return [word for word in function_name.split('_') if is_verb(word)]


def get_functions_from_tree(tree):
    return [node.name.lower() for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]


def clean_special_function_names(all_function_names):
    """
    Get a list of function names without special functions,
    such as __init__, __add__ etc.
    :param all_function_names: list with function names
    :return: list with function names without special function name
    """
    functions = []
    for function_name in all_function_names:
        if not (function_name.startswith('__') and function_name.endswith('__')):
            functions.append(function_name)
    return functions


def get_all_function_names(trees):
    name_lists = [get_functions_from_tree(tree) for tree in trees]
    return make_list_flat(name_lists)


def get_verbs(function_name_list):
    verbs = [get_verbs_from_function_name(function_name) for function_name in function_name_list]
    return make_list_flat(verbs)


def download_nltk_data():
    """
    Upload the data for analysis to the download folder
    :return: none
    """
    tagger = 'averaged_perceptron_tagger'
    nltk_downloader = nltk.downloader.Downloader()
    if nltk_downloader.status(tagger) == 'installed':
        return
    nltk.download(tagger)


def parse_args():
    """
    Get arguments from the command line
    :return: args from console
    """
    parser = argparse.ArgumentParser(
        description='Top verbs used in function names in the project(s).'
    )
    parser.add_argument(
        '-d',
        '--dirs',
        nargs='+',
        dest='dirs',
        required=True,
        help='The path to the project or projects separated by space.'
    )
    parser.add_argument(
        '-t',
        '--top',
        action='store',
        default=10,
        type=int,
        dest='top_size',
        help='The size of the top verbs, default is 10.',
    )

    return parser.parse_args()


def print_top_words_in_console(words, top_size):
    """
    Prints top words in the console
    :param words: Word list
    :param top_size: Size top, int
    :return: Print in console
    """
    sys.stdout.write(Colors.BOLD)
    print('=' * 30, f'top {top_size} verbs', '=' * 30)
    print(f'total {len(words)} words, {len(set(words))} unique')
    len_row = 30 * 2 + len(f'top {top_size} verbs') + 2
    print('=' * len_row)
    for word, occurrence in collections.Counter(words).most_common(top_size):
        print(word, occurrence)
    print('=' * len_row)
    sys.stdout.write(Colors.ENDC)


def words_to_json_dict(_list):
    """
    Make from list of tuples = > dict in json
    :param _list:
    :return: json, like {word: freq}
    """
    dictionary = dict((word, count) for word, count in _list)
    return json.dumps(dictionary)


def get_ungrouped_list_verbs(projects_dir):
    """
    Returns an ungrouped list of words
    :param projects_dir: list
    :return: return list with ungrouped words(verbs)
    """
    if type(projects_dir) != list:
        raise TypeError('Send to function list of path projects.')
    words = []

    download_nltk_data()

    for path in projects_dir:
        file_names = get_file_names_from_path(path)
        syntax_trees = get_syntax_trees_from_files(file_names)
        all_functions = get_all_function_names(syntax_trees)
        function_names = clean_special_function_names(all_functions)
        verbs = get_verbs(function_names)
        words.append(verbs)

    return words


def get_top_verbs(dirs, top_size=10, format_data='list'):
    """
    Get top verbs used in function names in projects.
    To get data in json format, specify format_data in the variable
    :param format_data: output format,possible value :'json','list'.
    Default is 'list'
    :param dirs: path to project or list with path to project
    :param top_size: top size
    :return: list of tuples or json
    """
    if not type(dirs) == list:
        project_dirs = [dirs]
    else:
        project_dirs = dirs
    words = get_ungrouped_list_verbs(project_dirs)
    data = collections.Counter(make_list_flat(words)).most_common(top_size)
    if format_data == 'json':
        data = words_to_json_dict(data)
    return data


def main():
    """
    Used to call from the command line
    :return: Print in console
    """
    args = parse_args()

    words = get_ungrouped_list_verbs(args.dirs)
    print_top_words_in_console(make_list_flat(words), args.top_size)


if __name__ == '__main__':
    main()
