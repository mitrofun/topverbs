import os

from topverbs import (make_list_flat, is_verb, get_verbs_from_function_name,
                      get_verbs, get_top_verbs)


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


def test_get_top_verbs():
    root_path = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
    fixtures = os.path.join(root_path, 'fixtures')
    verbs = get_top_verbs(fixtures)
    assert 'get' in make_list_flat(verbs)
    assert 'say' in make_list_flat(verbs)
