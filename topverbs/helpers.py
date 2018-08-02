import json
import os


def make_list_flat(_list):
    """ [(1,2), (3,4)] -> [1, 2, 3, 4]"""
    return sum([list(item) for item in _list], [])


def convert_list_of_tuples_to_json_dict(_list):
    """
    Convert from list of tuples = > dict in json
    :param _list:
    :return: json, like {word: freq}
    """
    dictionary = dict((word, count) for word, count in _list)
    return json.dumps(dictionary)


def get_file_names_from_path(path):
    file_names = []
    for dir_name, dirs, files in os.walk(path, topdown=True):
        for file in files:
            if file.endswith('.py'):
                file_names.append(os.path.join(dir_name, file))
    return file_names


def get_file_content(filename):
    """
    Get content from file
    :param filename: name file, str
    :return: content from file
    """
    with open(filename, 'r', encoding='utf-8') as attempt_handler:
        file_content = attempt_handler.read()
    return file_content
