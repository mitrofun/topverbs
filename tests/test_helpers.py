# import mock

from topverbs.topverbs import make_list_flat, is_verb, get_verbs_from_function_name, get_verbs


def test_make_list_flat():
    assert make_list_flat([(1, 2)]) == [1, 2]
    assert make_list_flat([[1, 2, 3]]) == [1, 2, 3]
    assert make_list_flat([(1, 2), (3, 4)]) == [1, 2, 3, 4]


# @mock.patch()
# def test__check_download_dir():
#     assert True

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
