import os
import ast
import nltk
import argparse
import collections

import logging.config

from nltk import pos_tag

from helpers import (
    make_list_flat,
    convert_list_of_tuples_to_json_dict,
    get_file_names_from_path,
    get_file_content
)

from console import print_top_words_in_console, print_debug_mode_header

DEBUG = os.environ.get('DEBUG') == 'true'

if DEBUG:
    logging.config.fileConfig('log.conf')


logger = logging.getLogger(__name__)


def is_verb(word):
    """Check what word is verb"""
    if not word:
        return False
    pos_info = pos_tag([word])
    return pos_info[0][1] == 'VB'


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
        data = convert_list_of_tuples_to_json_dict(data)
    return data


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


def main():
    """
    Used to call from the command line
    :return: Print in console
    """
    if DEBUG:
        print_debug_mode_header()

    args = parse_args()

    words = get_ungrouped_list_verbs(args.dirs)
    print_top_words_in_console(make_list_flat(words), args.top_size)


if __name__ == '__main__':
    main()
