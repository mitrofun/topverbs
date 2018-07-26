from dclnt import flat


def test_flat():
    assert flat([(1, 2)]) == [1, 2]
    assert flat([(1, 2), (3, 4)]) == [1, 2, 3, 4]
