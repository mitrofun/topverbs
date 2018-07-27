import ast
import os
import collections
import nltk
import logging
import logging.config

from nltk import pos_tag

TOP_SIZE = 10

PATH = ''

logging.config.fileConfig('log.conf')
# logging.basicConfig(level=logging.DEBUG)
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
            logger.warning(e)
            continue
        trees.append(tree)

    return trees


def get_syntax_trees(_path, with_file_names=False, with_file_content=False):
    """Get trees in path"""
    path = PATH
    file_names = get_file_names_from_path(path)
    # for dir_name, dirs, files in os.walk(path, topdown=True):
    #     for file in files:
    #         if file.endswith('.py'):
    #             file_names.append(os.path.join(dir_name, file))
    #             if len(file_names) == 100:
    #                 break
    # logger.debug('total %s files' % len(file_names))

    # for filename in file_names:
    #     with open(filename, 'r', encoding='utf-8') as attempt_handler:
    #         main_file_content = attempt_handler.read()
    #     try:
    #         tree = ast.parse(main_file_content)
    #     except SyntaxError as e:
    #         logger.warning(e)
    #         tree = None
    #
    #     if with_file_names:
    #         if with_file_content:
    #             trees.append((filename, main_file_content, tree))
    #         else:
    #             trees.append((filename, tree))
    #     else:
    #         trees.append(tree)
    trees = get_syntax_trees_from_files(file_names)
    logger.debug('trees generated')
    return trees


def get_all_names(tree):
    return [node.id for node in ast.walk(tree) if isinstance(node, ast.Name)]


def get_verbs_from_function_name(function_name):
    """
    Get verbs from string
    :return list with verbs
    """
    return [word for word in function_name.split('_') if is_verb(word)]


# def get_all_words_in_path(path):
#     """Get all words in path"""
#     trees = [t for t in get_syntax_trees(path) if t]
#     function_names = [f for f in make_list_flat([get_all_names(t) for t in trees])
#                       if not (f.startswith('__') and f.endswith('__'))]

    # def split_snake_case_name_to_words(name):
    #     return [n for n in name.split('_') if n]
    #
    # return make_list_flat([split_snake_case_name_to_words(function_name)
    #                        for function_name in function_names])


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


def get_top_verbs_in_path(path, top_size=10):
    """
    Получаем топ 10 глаголов в текущей дирректории
    :param path: Путь, строка
    :param top_size: Ограничение
    :return:
    """
    global PATH
    PATH = path

    logger.debug(f'path is {path}')

    trees = get_syntax_trees(None)
    all_functions = get_all_function_names(trees)

    logger.debug(f'count of all function: {len(all_functions)}')

    functions = get_function_names_without_special(all_functions)

    logger.debug(f'count of function: {len(functions)}')
    logger.debug('functions extracted')

    verbs = get_verbs(functions)
    return collections.Counter(verbs).most_common(top_size)


# def get_top_functions_names_in_path(path, top_size=10):
#     """Get top function name in path"""
#     t = get_syntax_trees(path)
#     nms = [f for f in make_list_flat(
#         [[node.name.lower() for node in ast.walk(t) if isinstance(node, ast.FunctionDef)]
#          for t in t]) if not (f.startswith('__') and f.endswith('__'))]
#     return collections.Counter(nms).most_common(top_size)


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


def print_top_words(words, top_size):
    """
    Печатает в консоли топ слов
    :param words: Список слов, словарь
    :param top_size: Размер топа
    :return: Выводит топ слов в консоль
    """
    print('-' * 120)
    print('total %s words, %s unique' % (len(words), len(set(words))))
    print(words)
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
        words += get_top_verbs_in_path(path, top_size=TOP_SIZE)

    print_top_words(words, TOP_SIZE)


if __name__ == '__main__':
    main()
