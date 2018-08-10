import os
import ast
import nltk
import argparse
import collections

import logging.config
import tempfile

from nltk import pos_tag

from helpers import (
    make_list_flat,
    convert_list_of_tuples_to_json_dict,
    get_file_names_from_path,
    get_file_content
)

from console import print_top_words_in_console, colored_print
from os_handler import clone_to_dir, delete_created_repo_dir

DEBUG = os.environ.get('DEBUG') == 'true'

if DEBUG:
    logging.config.fileConfig('log.conf')

logger = logging.getLogger(__name__)


def is_verb(word):
    if not word:
        return False
    pos_info = pos_tag([word])
    return pos_info[0][1] == 'VB'


def is_noun(word):
    if not word:
        return False
    pos_info = pos_tag([word])
    return pos_info[0][1] == 'NN'


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
    return [word for word in function_name.split('_') if is_verb(word)]


def get_nouns_from_function_name(function_name):
    return [word for word in function_name.split('_') if is_noun(word)]


def get_functions_from_tree(tree):
    return [node.name.lower() for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]


def get_variables_names_from_tree(tree):
    body_functions = \
        [node.body for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
    return make_list_flat([[a.targets[0].id for a in fb if isinstance(a, ast.Assign) and
                            isinstance(a.targets[0], ast.Name)] for fb in body_functions])


def clean_special_names(all_function_names):
    functions = []
    for function_name in all_function_names:
        if not (function_name.startswith('__') and function_name.endswith('__')):
            functions.append(function_name)
    return functions


def get_all_function_names(trees):
    name_lists = [get_functions_from_tree(tree) for tree in trees]
    return make_list_flat(name_lists)


def get_all_variables_names(trees):
    name_lists = [get_variables_names_from_tree(tree) for tree in trees]
    return make_list_flat(name_lists)


def get_verbs(function_name_list):
    verbs = [get_verbs_from_function_name(function_name) for function_name in function_name_list]
    return make_list_flat(verbs)


def get_nouns(function_name_list):
    nouns = [get_nouns_from_function_name(function_name) for function_name in function_name_list]
    return make_list_flat(nouns)


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


def get_top_words(dirs, top_size=10, format_data='list', lang_category='verb'):
    if not type(dirs) == list:
        project_dirs = [dirs]
    else:
        project_dirs = dirs
    words = get_ungrouped_list_words(project_dirs, lang_category)
    data = collections.Counter(make_list_flat(words)).most_common(top_size)
    if format_data == 'json':
        data = convert_list_of_tuples_to_json_dict(data)
    return data


def get_code_elements_from_syntax_trees(syntax_trees, code_element='func'):
    all_source = []

    if code_element == 'func':
        all_source = get_all_function_names(syntax_trees)

    if code_element == 'var':
        all_source = get_all_variables_names(syntax_trees)

    source_names = clean_special_names(all_source)

    return source_names


def get_ungrouped_list_words(projects_dir, lang_category='verb', code_element='func'):
    if type(projects_dir) != list:
        raise TypeError('Send to function list of path projects.')
    words = []
    word_list = []

    download_nltk_data()

    for path in projects_dir:
        file_names = get_file_names_from_path(path)
        syntax_trees = get_syntax_trees_from_files(file_names)
        source_names = get_code_elements_from_syntax_trees(syntax_trees, code_element)
        if lang_category == 'verb':
            word_list = get_verbs(source_names)
        if lang_category == 'noun':
            word_list = get_nouns(source_names)
        words.append(word_list)
    return words


def parse_args():

    parser = argparse.ArgumentParser(
        description='Top verbs used in function names in the project(s).'
    )
    parser.add_argument(
        '-d',
        '--dirs',
        nargs='+',
        dest='dirs',
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
    parser.add_argument(
        '--repo',
        dest='repo',
        help='The repository url.'
    )
    parser.add_argument(
        '-c',
        '--category',
        dest='lang_category',
        help='Language word category. Possible value: noun, verb.',
        default='verb',
        choices=['noun', 'verb']
    )
    parser.add_argument(
        '-e',
        '--element',
        dest='code_element',
        help='The analyzed part of the code.'
             'Search for words in function names or local variables. '
             'Possible value: var, func.',
        default='func',
        choices=['var', 'func']
    )

    return parser.parse_args()


def main():
    if DEBUG:
        colored_print('Start script in debug mode', mode='warning')

    args = parse_args()
    dirs = args.dirs

    if args.repo:
        tmp_dir = tempfile.mkdtemp()
        clone_to_dir(args.repo, tmp_dir)
        dirs = [tmp_dir]

    words = get_ungrouped_list_words(dirs, args.lang_category, args.code_element)
    print_top_words_in_console(
        make_list_flat(words), args.top_size, args.lang_category, args.code_element
    )

    if args.repo:
        delete_created_repo_dir(dirs[0])


if __name__ == '__main__':
    main()
