import os
import pytest

from helpers import (
    make_list_flat,
    convert_list_of_tuples_to_json_dict,
    get_file_names_from_path,
    get_file_content,
    get_max_len_word,
    get_max_len_number
)


def test_make_list_flat():
    assert make_list_flat([(1, 2)]) == [1, 2]
    assert make_list_flat([[1, 2, 3]]) == [1, 2, 3]
    assert make_list_flat([(1, 2), (3, 4)]) == [1, 2, 3, 4]


def test_convert_list_of_tuples_to_json_dict():
    assert convert_list_of_tuples_to_json_dict(
        [('words', 4), ('less', 5)]) == '{"words": 4, "less": 5}'


def test_get_file_names_from_path(fixtures_path):
    list_files = get_file_names_from_path(fixtures_path)
    file = os.path.basename(list_files[0])
    assert file == 'hello.py'


def test_get_file_content(file_with_code_path):
    assert 'say_hello' in get_file_content(file_with_code_path)


@pytest.mark.parametrize('_list', [
    ['тест', 1, 12, 'проверка'],
    ['тест', 'проверка']
])
def test_get_max_len_word(_list):
    assert get_max_len_word(_list) == 8


@pytest.mark.parametrize('_list', [
    ['тест', 1, 12, 'проверка'],
    ['тест', 'проверка', 23, 46]
])
def test_get_max_len_number(_list):
    assert get_max_len_number(_list) == 2
