import argparse
import pytest
import mock

from topverbs import *  # noqa


def test_make_list_flat():
    assert make_list_flat([(1, 2)]) == [1, 2]
    assert make_list_flat([[1, 2, 3]]) == [1, 2, 3]
    assert make_list_flat([(1, 2), (3, 4)]) == [1, 2, 3, 4]


def test_is_verb():
    """
    Test for self, for understanding working function
    the original project
    """
    assert is_verb('do') is True
    assert is_verb('save') is True
    assert is_verb('car') is False


def test_get_verbs_from_function_name():
    assert get_verbs_from_function_name('save_data') == ['save']
    assert get_verbs_from_function_name('get_list') == ['get']
    assert get_verbs_from_function_name('get_and_save') == ['get', 'save']


def test_get_verbs():
    functions_name = ['save_data', 'get_list']
    assert get_verbs(functions_name) == ['save', 'get']


def test_get_top_verbs(fixtures_path):
    verbs = get_top_verbs(fixtures_path)
    assert 'get' in make_list_flat(verbs)
    assert 'say' in make_list_flat(verbs)
    assert len(verbs) == 2


def test_get_top_verbs_json(fixtures_path):
    verbs = get_top_verbs(fixtures_path, format_data='json')
    assert 'get' in verbs
    assert 'say' in verbs


def test_get_top_verbs_top_count(fixtures_path):
    verbs = get_top_verbs(fixtures_path, top_size=1)
    assert len(verbs) == 1


def test_get_ungrouped_list_verbs(fixtures_path):
    verbs = get_ungrouped_list_verbs([fixtures_path])
    assert len(verbs[0]) == 2
    with pytest.raises(Exception):
        get_ungrouped_list_verbs(fixtures_path)


def test_get_file_names_from_path(fixtures_path):
    list_files = get_file_names_from_path(fixtures_path)
    file = os.path.basename(list_files[0])
    assert file == 'hello.py'


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


def test_clean_special_function_names():
    assert clean_special_function_names(['__add__', 'add']) == ['add']


@mock.patch('argparse.ArgumentParser.parse_args',
            return_value=argparse.Namespace(dirs=['.'], top_size=3))
def test_main(args, capfd):
    main()
    out, err = capfd.readouterr()
    print('\n')
    print(out)
    assert 'top 3 verbs' in out
