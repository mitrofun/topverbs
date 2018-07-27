import ast
import os
import collections
import nltk
import logging
import logging.config

from nltk import pos_tag

DEBUG = os.environ.get('DEBUG') == 'true'

TOP_SIZE = 10

if DEBUG:
    logging.config.fileConfig('log.conf')

logger = logging.getLogger(__name__)


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


def get_all_function_names(trees):
    name_lists = [get_functions_from_tree(tree) for tree in trees]
    return make_list_flat(name_lists)


def get_function_names_without_special(all_function_names):
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


def get_verbs(function_name_list):
    verbs = [get_verbs_from_function_name(function_name) for function_name in function_name_list]
    return make_list_flat(verbs)


def check_download_dir():
    """
    The function checks the folder if the folder
    does not exist, then creates it
    :return: path to download dir, str
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.dirname(current_dir)
    download_dir = os.path.join('..', root_dir, 'nltk_data')
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)
    return download_dir


def download_nltk_data():
    """
    Upload the data for analysis to the download folder
    :return: none
    """
    tagger = 'averaged_perceptron_tagger'
    download_dir = check_download_dir()
    data_dir = os.path.join(download_dir, 'taggers', tagger)
    if os.path.exists(data_dir):
        return
    nltk.download(tagger, download_dir=download_dir)
    nltk.data.path.append(download_dir)


def print_top_words_in_console(words, top_size):
    """
    Prints top words in the console
    :param words: Word list
    :param top_size: Size top, int
    :return: Print in console
    """
    print('-' * 120)
    print(f'top {top_size} words')
    print(f'total {len(words)} words, {len(set(words))} unique')
    for word, occurrence in collections.Counter(words).most_common(top_size):
        print(word, occurrence)


def main():
    words = []
    projects = [
        'Kindergartens',
        'HJ-Site',
        'onpoint',
        'Google-Business-class'
    ]

    download_nltk_data()

    for project in projects:
        path = os.path.join('..', project)
        file_names = get_file_names_from_path(path)
        syntax_trees = get_syntax_trees_from_files(file_names)
        all_functions = get_all_function_names(syntax_trees)
        function_names = get_function_names_without_special(all_functions)
        verbs = get_verbs(function_names)
        words.append(verbs)

    print_top_words_in_console(make_list_flat(words), TOP_SIZE)


if __name__ == '__main__':
    main()
