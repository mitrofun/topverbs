import csv
import os

import collections

from pathlib import Path

from console import colored_print
from helpers import convert_list_of_tuples_to_json_dict


def create_csv(file_name, data):
    f = open(file_name, 'w')
    with f:
        writer = csv.writer(f)
        for row in data:
            writer.writerow(row)


def create_json(file_name, data):
    f = open(file_name, 'w')
    json = convert_list_of_tuples_to_json_dict(data)
    with f:
        f.write(json)


def create_report_file(words, top_size, report_path, lang_category='verb', code_element='func',
                       format_file='json'):
    if report_path == '~':
        path = str(Path.home())
    else:
        path = report_path

    if not os.path.exists(path):
        colored_print(f"Directory '{path}' not found.", mode='warning')
        return

    words_collection = collections.Counter(words).most_common(top_size)

    file_name = f'{path}/top{top_size}_{lang_category}_in_{code_element}.{format_file}'

    if format_file == 'csv':
        create_csv(file_name, words_collection)

    if format_file == 'json':
        create_json(file_name, words_collection)

    colored_print(f'Report save to : {file_name}')
