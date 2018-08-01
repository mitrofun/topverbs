import sys

import collections

from helpers import get_max_len_word, get_max_len_number, make_list_flat


class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    RED = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def print_top_words_in_console(words, top_size):
    """
    Prints top words in the console
    :param words: Word list
    :param top_size: Size top, int
    :return: Print in console
    """
    sys.stdout.write(Colors.BOLD + Colors.HEADER)
    print('=' * 30, f'top {top_size} verbs', '=' * 30)
    sys.stdout.write(Colors.ENDC)
    sys.stdout.write(Colors.BOLD)
    print(f'total {len(words)} words, {len(set(words))} unique')
    len_row = 30 * 2 + len(f'top {top_size} verbs') + 2
    print('=' * len_row)

    words_collection = collections.Counter(words).most_common(top_size)
    flat_words_collection = make_list_flat(words_collection)
    max_len_word = get_max_len_word(flat_words_collection)
    max_len_number = get_max_len_number(flat_words_collection)

    for word, occurrence in words_collection:
        str_len = len(f'{word} {occurrence}')
        complete_len = (max_len_word + max_len_number + 2) - str_len
        print(f'{word}: {occurrence}', ' ' * complete_len, '*' * occurrence)
    sys.stdout.write(Colors.BOLD + Colors.HEADER)
    print('=' * len_row)
    sys.stdout.write(Colors.ENDC)


def print_debug_mode_header():
    sys.stdout.write(Colors.BOLD + Colors.FAIL)
    print('start script in debug mode')
    sys.stdout.write(Colors.ENDC)
