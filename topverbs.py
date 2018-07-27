from topverbs.topverbs import (parse_args, get_ungrouped_list_verbs, make_list_flat)
from topverbs.console import print_top_words_in_console


def main():
    """
    Used to call from the command line
    :return: Print in console
    """
    args = parse_args()

    words = get_ungrouped_list_verbs(args.dirs)
    print_top_words_in_console(make_list_flat(words), args.top_size)


if __name__ == '__main__':
    main()
