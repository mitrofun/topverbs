from syntax import *  # noqa


def test_is_verb():
    assert is_verb('do') is True
    assert is_verb('save') is True
    assert is_verb('car') is False
    assert is_verb('') is False


def test_is_noun():
    assert is_noun('do') is False
    assert is_noun('save') is False
    assert is_noun('car') is True
    assert is_noun('') is False


def test_get_verbs_from_function_name():
    assert get_verbs_from_function_name('save_data') == ['save']
    assert get_verbs_from_function_name('get_list') == ['get']
    assert get_verbs_from_function_name('get_and_save') == ['get', 'save']


def test_get_nouns_from_function_name():
    assert get_nouns_from_function_name('get_list') == ['list']
    assert get_nouns_from_function_name('get_and_save') == []


def test_get_verbs():
    functions_name = ['save_data', 'get_list']
    assert get_verbs(functions_name) == ['save', 'get']


def test_get_syntax_trees_from_files(file_with_code_path):
    """
    Test for self, for understanding working ast module
    """
    tree = get_syntax_trees_from_files([file_with_code_path])
    astNode = tree[0]
    assert len(astNode.body) == 2
    function_name = astNode.body[0].name
    assert function_name == 'get_name'


def test_get_functions_from_tree(file_with_code_path):
    tree = get_syntax_trees_from_files([file_with_code_path])[0]
    functions = get_functions_from_tree(tree)
    assert len(functions) == 2
    assert 'say_hello' in functions


def test_clean_special_names():
    assert clean_special_names(['__add__', 'add']) == ['add']
