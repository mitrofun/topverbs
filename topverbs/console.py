import sys

import collections


class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    RED = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def output_horizontal_bold_bolder(style, length_bolder):
    sys.stdout.write(style)
    print('=' * length_bolder)
    sys.stdout.write(Colors.ENDC)


def output_vertical_border(style, string_end='\n'):
    sys.stdout.write(style)
    print('|', end=string_end)
    sys.stdout.write(Colors.ENDC)


def output_header(style, wrapper, title):
    sys.stdout.write(style)
    print(wrapper, title, wrapper)
    sys.stdout.write(Colors.ENDC)


def print_top_words_in_console(words, top_size):
    """
    Prints top words in the console
    :param words: Word list
    :param top_size: Size top, int
    :return: Print in console
    """
    # style for borders and header table
    style_table = Colors.BOLD + Colors.GREEN
    # set wrapper len, to change all output len
    wrapper_len = 30

    text_header = f'top {top_size} verbs'
    text_header_wrapper = '=' * wrapper_len

    len_all_row = len(text_header) + len(text_header_wrapper) * 2 + 2

    output_header(style_table, text_header_wrapper, text_header)
    # output content
    sys.stdout.write(Colors.BOLD)
    total_text = f'total {len(words)} words, {len(set(words))} unique'
    output_vertical_border(style_table, string_end=' ')

    sys.stdout.write(Colors.BOLD)
    additional_spaces_len = len_all_row - len(total_text) - 4
    print(total_text, ' ' * additional_spaces_len, end='')
    output_vertical_border(style_table)
    output_horizontal_bold_bolder(style_table, length_bolder=len_all_row)
    words_collection = collections.Counter(words).most_common(top_size)

    for word, occurrence in words_collection:
        content_len = len(f'{word} : {occurrence}')
        additional_spaces_len = len_all_row - content_len - 4
        output_vertical_border(style_table, string_end=' ')
        sys.stdout.write(Colors.BOLD)
        print(f'{word} : {occurrence}', ' ' * additional_spaces_len, end='')
        output_vertical_border(style_table)
    # end table
    output_horizontal_bold_bolder(style_table, length_bolder=len_all_row)


def print_debug_mode_header():
    sys.stdout.write(Colors.BOLD + Colors.FAIL)
    print('start script in debug mode')
    sys.stdout.write(Colors.ENDC)
