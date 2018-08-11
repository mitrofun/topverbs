import os

import ast
from nltk import pos_tag

import logging
import logging.config


from helpers import get_file_content, make_list_flat

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


def get_variable_names_from_body(body):
    _list = []
    for node in body:
        if isinstance(node, ast.Assign) and isinstance(node.targets[0], ast.Name):
            _list.append(node.targets[0].id)
    return _list


def get_variables_names_from_tree(tree):
    variables_names = []
    body_functions = [node.body for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
    for body in body_functions:
        variables_names += get_variable_names_from_body(body)
    return variables_names


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
