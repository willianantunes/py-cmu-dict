from py_cmu_dict.support.iter_utils import flatten


def test_should_flatten_list():
    sample_list = [[1, 2, 3], [4, 5, 6], [7], [8, 9]]

    result = flatten(sample_list)

    assert result == [1, 2, 3, 4, 5, 6, 7, 8, 9]
