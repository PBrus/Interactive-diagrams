"""
Test package of the idgrms.data module
"""
import pytest
from unittest.mock import Mock
from collections import Counter
from idgrms.data import _read_file
from idgrms.data import *


@pytest.fixture
def data_file():
    return 'example_data/mags.db'


@pytest.fixture
def group_file():
    return 'example_data/better.num'


@pytest.fixture
def mock_data(data_file):
    mock_data = Mock()
    mock_data.content = read_file_content(data_file)
    mock_data.numbers = tuple(
        np.array(mock_data.content[:, 0], dtype='int').tolist())
    return mock_data


@pytest.fixture
def data_header():
    header = np.array([
        'no', 'U', 'errU', 'B', 'errB', 'V', 'errV', 'I', 'errI',
        'U-B', 'errU-B', 'B-V', 'errB-V', 'V-I', 'errV-I'
    ])
    return header


@pytest.fixture
def mock_get_data(data_file):
    mock_get_data = Mock()
    mock_get_data.content = get_data(data_file, [[12, -10], [12, -4]])
    return mock_get_data


def test_read_file(data_file):
    last_row = _read_file(data_file)[-1]
    row = np.array([
        6.40800e+03, 1.61958e+01, 4.20000e-03, 1.67973e+01, 8.90000e-03,
        1.64573e+01, 7.60000e-03, 1.58256e+01, 1.91000e-02, -6.01500e-01,
        9.80000e-03, 3.40000e-01, 1.17000e-02, 6.31700e-01, 2.06000e-02
    ])
    assert (last_row == row).all()


def test_read_file_header(data_file, data_header):
    header = read_file_header(data_file)
    assert (header == data_header).all()


def test_read_file_content(data_file):
    first_row = read_file_content(data_file)[0]
    row = np.array([
        6.00000e+00, 1.74027e+01, 8.40000e-03, 1.53704e+01, 4.90000e-03,
        1.34930e+01, 1.70000e-03, 1.02656e+01, 2.40000e-03, 2.03230e+00,
        9.70000e-03, 1.87740e+00, 5.20000e-03, 3.22740e+00, 2.90000e-03
    ])
    assert (first_row == row).all()


def test_read_group_file(group_file):
    content = read_group_file(group_file)
    numbers = (
        48, 49, 65, 205, 286, 314, 341, 345,
        403, 474, 506, 508, 533, 539, 593, 740
    )
    assert content == numbers


@pytest.mark.parametrize("nested_list, list_result", [
    ([[1, -3], [5, 6], [-4, 5]], [1, -3, 5, 6, -4]),
    ([[-5, 5, 1], [-1, 1, 6]], [-5, 5, 1, -1, 6]),
    ([[2, 3], [0, -1], [12, 92], [-3, 3]], [2, 3, 0, -1, 12, 92, -3])
])
def test_unique_columns_list(nested_list, list_result):
        unique_list = unique_columns_list(nested_list)
        assert Counter(unique_list) == Counter(list_result)


def test_get_necessary_data_column(mock_data, data_header):
    array = np.ma.array([
        0.0083, 0.0019, 0.0015, 0.0089, 0.0103,
        0.0072, 0.0086, 0.0025, 0.0014, 0.0015
    ])
    values = get_necessary_data_column(mock_data.content, data_header, 3)
    values = values[-1][60:70]
    assert (array == values).all()


@pytest.mark.parametrize("columns, results", [
    ([[4, -3]], np.ma.array([17.2035, 17.2442, 17.1444, 17.1882, 16.7973])),
    ([[2, 3]], np.ma.array([17.5104, 17.4642, 17.8264, 17.3051, 16.1958])),
    ([[5, 6]], np.ma.array([0.0115, 0.0119, 0.0101, 0.0105, 0.0089])),
])
def test_get_data(data_file, columns, results):
    values = get_data(data_file, columns)[0][-1][-5:]
    assert (values == results).all()


@pytest.mark.parametrize("columns, indexes", [
    ([12, -4], (0, 1)),
    ([12, -10], (0, 2))
])
def test_current_data_indexes(mock_get_data, columns, indexes):
    assert current_data_indexes(mock_get_data.content, columns) == indexes


@pytest.mark.parametrize("columns, results", [
    ([12, -4], np.ma.array([17.2035, 17.2442, 17.1444, 17.1882, 16.7973])),
    ([12, -10], np.ma.array([0.3069, 0.22, 0.682, 0.1169, -0.6015]))
])
def test_get_specific_data_numbers(mock_get_data, columns, results):
    values = get_specific_data(mock_get_data.content, columns)[0][1][-5:]
    assert (values == results).all()


@pytest.mark.parametrize("columns, results", [
    ([12, -4], (('B-V', 'B'), (12, -4))),
    ([12, -10], (('B-V', 'U-B'), (12, -10)))
])
def test_get_specific_data_labels_and_indexes(mock_get_data, columns, results):
    values = get_specific_data(mock_get_data.content, columns)[1:]
    assert Counter(values) == Counter(results)


@pytest.mark.parametrize("columns, marked_data, results", [
    ([12, -4], ((0.4748, 0.4433), (13.3463, 13.2855), (0.0252, 0.3454)),
        ((0.4748, 0.4433), (13.3463, 13.2855))),
    ([12, -10], ((0.4748, 0.4433), (13.3463, 13.2855), (0.0252, 0.3454)),
        ((0.4748, 0.4433), (0.0252, 0.3454)))
])
def test_get_marked_points(mock_get_data, columns, marked_data, results):
    values = get_marked_points(mock_get_data.content, marked_data, columns)
    assert Counter(values) == Counter(results)
