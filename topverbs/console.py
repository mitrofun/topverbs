import sys

import collections

from .colors import Colors


def print_top_words_in_console(words, top_size):
    """
    Prints top words in the console
    :param words: Word list
    :param top_size: Size top, int
    :return: Print in console
    """
    sys.stdout.write(Colors.BOLD)
    print('=' * 30, f'top {top_size} verbs', '=' * 30)
    print(f'total {len(words)} words, {len(set(words))} unique')
    len_row = 30 * 2 + len(f'top {top_size} verbs') + 2
    print('=' * len_row)
    for word, occurrence in collections.Counter(words).most_common(top_size):
        print(word, occurrence)
    print('=' * len_row)
    sys.stdout.write(Colors.ENDC)
