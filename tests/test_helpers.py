# import mock
from topverbs.topverbs import make_list_flat


def test_make_list_flat():
    assert make_list_flat([(1, 2)]) == [1, 2]
    assert make_list_flat([(1, 2), (3, 4)]) == [1, 2, 3, 4]


# @mock.patch()
# def test__check_download_dir():
#     assert True
