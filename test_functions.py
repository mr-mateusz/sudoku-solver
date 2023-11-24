import numpy as np
import pytest

from functions import square_indices_to_grid_indices, square_idx_to_grid_indices, pos_to_square_idx, __get_row_list, \
    __get_col_list, __get_square_list, __get_row_arr, __get_col_arr, __get_square_arr, get_row, get_col, get_square, \
    get_row_for_pos, get_col_for_pos, get_square_for_pos, get_unique_numbers


@pytest.mark.parametrize('inputs,outputs', [
    ((0, 0), ((0, 3), (0, 3))),
    ((0, 1), ((0, 3), (3, 6))),
    ((0, 2), ((0, 3), (6, 9))),
    ((1, 0), ((3, 6), (0, 3))),
    ((1, 1), ((3, 6), (3, 6))),
    ((1, 2), ((3, 6), (6, 9))),
    ((2, 0), ((6, 9), (0, 3))),
    ((2, 1), ((6, 9), (3, 6))),
    ((2, 2), ((6, 9), (6, 9))),
])
def test_square_indices_to_grid_indices(inputs, outputs):
    assert square_indices_to_grid_indices(*inputs) == outputs


@pytest.mark.parametrize('inputs,outputs', [
    (0, ((0, 3), (0, 3))),
    (1, ((0, 3), (3, 6))),
    (2, ((0, 3), (6, 9))),
    (3, ((3, 6), (0, 3))),
    (4, ((3, 6), (3, 6))),
    (5, ((3, 6), (6, 9))),
    (6, ((6, 9), (0, 3))),
    (7, ((6, 9), (3, 6))),
    (8, ((6, 9), (6, 9))),
])
def test_square_idx_to_grid_indices(inputs, outputs):
    assert square_idx_to_grid_indices(inputs) == outputs


@pytest.mark.parametrize('inputs,outputs', [
    ((0, 0), 0),
    ((2, 3), 1),
    ((1, 8), 2),
    ((3, 2), 3),
    ((4, 5), 4),
    ((5, 6), 5),
    ((8, 1), 6),
    ((6, 4), 7),
    ((7, 7), 8),
])
def test_pos_to_square_idx(inputs, outputs):
    assert pos_to_square_idx(inputs) == outputs


@pytest.fixture
def random_matrix():
    return np.random.randint(0, 9, size=(9, 9))


@pytest.fixture
def random_nested_list(random_matrix):
    return random_matrix.tolist()


@pytest.mark.parametrize('row_idx',
                         list(range(9)))
def test___get_row_list(random_nested_list, row_idx):
    assert __get_row_list(random_nested_list, row_idx) == random_nested_list[row_idx]


@pytest.mark.parametrize('col_idx',
                         list(range(9)))
def test___get_col_list(random_nested_list, col_idx):
    assert __get_col_list(random_nested_list, col_idx) == [row[col_idx] for row in random_nested_list]


@pytest.mark.parametrize('square_idx,list_indices', [
    (0, ((0, 3), (0, 3))),
    (1, ((0, 3), (3, 6))),
    (2, ((0, 3), (6, 9))),
    (3, ((3, 6), (0, 3))),
    (4, ((3, 6), (3, 6))),
    (5, ((3, 6), (6, 9))),
    (6, ((6, 9), (0, 3))),
    (7, ((6, 9), (3, 6))),
    (8, ((6, 9), (6, 9))),
])
def test___get_square_list(random_nested_list, square_idx, list_indices):
    square = [row[list_indices[1][0]: list_indices[1][1]] for row in
              random_nested_list[list_indices[0][0]: list_indices[0][1]]]

    assert __get_square_list(random_nested_list, square_idx) == square


@pytest.mark.parametrize('row_idx',
                         list(range(9)))
def test___get_row_arr(random_matrix, row_idx):
    arr1 = __get_row_arr(random_matrix, row_idx)
    arr2 = random_matrix[row_idx]
    assert np.array_equal(arr1, arr2)


@pytest.mark.parametrize('col_idx',
                         list(range(9)))
def test___get_col_arr(random_matrix, col_idx):
    arr1 = __get_col_arr(random_matrix, col_idx)
    arr2 = random_matrix[:, col_idx]
    assert np.array_equal(arr1, arr2)


@pytest.mark.parametrize('square_idx,list_indices', [
    (0, ((0, 3), (0, 3))),
    (1, ((0, 3), (3, 6))),
    (2, ((0, 3), (6, 9))),
    (3, ((3, 6), (0, 3))),
    (4, ((3, 6), (3, 6))),
    (5, ((3, 6), (6, 9))),
    (6, ((6, 9), (0, 3))),
    (7, ((6, 9), (3, 6))),
    (8, ((6, 9), (6, 9))),
])
def test___get_square_arr(random_matrix, square_idx, list_indices):
    square = random_matrix[list_indices[0][0]:list_indices[0][1], list_indices[1][0]:list_indices[1][1]]
    result = __get_square_arr(random_matrix, square_idx)
    assert np.array_equal(square, result)


@pytest.mark.parametrize('row_idx', [0, 5, 7])
def test_get_row(random_matrix, random_nested_list, row_idx):
    assert get_row(random_nested_list, row_idx) == random_nested_list[row_idx]
    assert np.array_equal(get_row(random_matrix, row_idx), random_matrix[row_idx])


@pytest.mark.parametrize('col_idx', [0, 5, 7])
def test_get_col(random_matrix, random_nested_list, col_idx):
    assert get_col(random_nested_list, col_idx) == [row[col_idx] for row in random_nested_list]
    assert np.array_equal(get_col(random_matrix, col_idx), random_matrix[:, col_idx])


@pytest.mark.parametrize('square_idx,list_indices', [
    (0, ((0, 3), (0, 3))),
    (5, ((3, 6), (6, 9))),
    (7, ((6, 9), (3, 6))),
])
def test_get_square(random_matrix, random_nested_list, square_idx, list_indices):
    square = [row[list_indices[1][0]:list_indices[1][1]] for row in
              random_nested_list[list_indices[0][0]:list_indices[0][1]]]
    assert get_square(random_nested_list, square_idx) == square

    arr1 = get_square(random_matrix, square_idx)
    arr2 = random_matrix[list_indices[0][0]:list_indices[0][1], list_indices[1][0]:list_indices[1][1]]
    assert np.array_equal(arr1, arr2)


@pytest.mark.parametrize('position', [
    (0, 1),
    (5, 8),
    (7, 4),
])
def test_get_row_for_pos(random_matrix, random_nested_list, position: tuple[int, int]):
    assert get_row_for_pos(random_nested_list, position) == random_nested_list[position[0]]
    assert np.array_equal(get_row_for_pos(random_matrix, position), random_matrix[position[0]])


@pytest.mark.parametrize('position', [
    (0, 1),
    (5, 8),
    (7, 4),
])
def test_get_col_for_pos(random_matrix, random_nested_list, position: tuple[int, int]):
    assert get_col_for_pos(random_nested_list, position) == [row[position[1]] for row in random_nested_list]
    assert np.array_equal(get_col_for_pos(random_matrix, position), random_matrix[:, position[1]])


@pytest.mark.parametrize('position,list_indices', [
    ((0, 1), ((0, 3), (0, 3))),
    ((5, 8), ((3, 6), (6, 9))),
    ((7, 4), ((6, 9), (3, 6))),
])
def test_get_square_for_pos(random_matrix, random_nested_list, position: tuple[int, int], list_indices):
    square = [row[list_indices[1][0]:list_indices[1][1]] for row in
              random_nested_list[list_indices[0][0]:list_indices[0][1]]]
    assert get_square_for_pos(random_nested_list, position) == square

    arr1 = get_square_for_pos(random_matrix, position)
    arr2 = random_matrix[list_indices[0][0]:list_indices[0][1], list_indices[1][0]:list_indices[1][1]]
    assert np.array_equal(arr1, arr2)


@pytest.mark.parametrize('inputs,outputs,flag', [
    (np.array([0, 0, 0]), {0}, False),
    (np.array([0, 0, 0]), set(), True),
    (np.array([0, 2, 2, 4]), {0, 2, 4}, False),
    (np.array([0, 2, 2, 4]), {2, 4}, True),
])
def test_get_unique_numbers(inputs, outputs, flag):
    assert get_unique_numbers(inputs, flag) == outputs

    # test if default value changed
    if flag:
        assert get_unique_numbers(inputs) == outputs
