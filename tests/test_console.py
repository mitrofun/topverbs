import pytest

from console import print_top_words_in_console


@pytest.mark.parametrize('worlds', [
    ['get', 'set', 'update'],
    ['check'],
])
def test_print_top_words_in_console(worlds, capfd):

    top = 10
    print_top_words_in_console(worlds, top)
    out, err = capfd.readouterr()
    assert worlds[0] in out
    assert str(top) in out
