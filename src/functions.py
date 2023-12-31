from collections import defaultdict
from collections.abc import Iterable, Sequence
from typing import TypeVar

import numpy as np


def square_indices_to_grid_indices(square_row_idx: int, square_col_idx: int) \
        -> tuple[tuple[int, int], tuple[int, int]]:
    row_start = square_row_idx * 3
    row_end = row_start + 3

    col_start = square_col_idx * 3
    col_end = col_start + 3

    return (row_start, row_end), (col_start, col_end)


def square_idx_to_grid_indices(square_idx: int) -> tuple[tuple[int, int], tuple[int, int]]:
    square_row_idx = square_idx // 3
    square_col_idx = square_idx % 3

    return square_indices_to_grid_indices(square_row_idx, square_col_idx)


def square_and_position_indices_to_absolute_position(square_idx: int, position_idx: int) -> tuple[int, int]:
    (row_start, _), (col_start, _) = square_idx_to_grid_indices(square_idx)

    row_offset = position_idx // 3
    col_offset = position_idx % 3

    return row_start + row_offset, col_start + col_offset


def pos_to_square_idx(pos: tuple[int, int]) -> int:
    return pos[0] // 3 * 3 + pos[1] // 3


def __get_row_list(nested_list: list[list], row_idx: int) -> list[list]:
    return nested_list[row_idx]


def __get_col_list(nested_list: list[list], col_idx: int) -> list[list]:
    return [row[col_idx] for row in nested_list]


def __get_square_list(nested_list: list[list], square_idx: int) -> list[list]:
    (row_start, row_end), (col_start, col_end) = square_idx_to_grid_indices(square_idx)
    return [row[col_start: col_end] for row in nested_list[row_start: row_end]]


def __get_row_arr(arr: np.ndarray, row_idx: int) -> np.ndarray:
    return arr[row_idx, :]


def __get_col_arr(arr: np.ndarray, col_idx: int) -> np.ndarray:
    return arr[:, col_idx]


def __get_square_arr(arr: np.ndarray, square_idx: int) -> np.ndarray:
    (row_start, row_end), (col_start, col_end) = square_idx_to_grid_indices(square_idx)
    return arr[row_start: row_end, col_start: col_end]


# TODO - think about type hints for these functions
# It's definitely confusing, especially because square returns 2d result, but row and column 1d
# Keep dims?
# Cannot use list[list] int TypeVar, because get_row and get_col will reduce "number of dims" in nested list
T = TypeVar('T', np.ndarray, list)


def get_row(grid: T, row_idx: int) -> T:
    return __get_row_list(grid, row_idx) if isinstance(grid, list) else __get_row_arr(grid, row_idx)


def get_col(grid: T, col_idx: int) -> T:
    return __get_col_list(grid, col_idx) if isinstance(grid, list) else __get_col_arr(grid, col_idx)


def get_square(grid: T, square_idx: int) -> T:
    """
    +- - -+- - -+- - -+
    |  0  |  1  |  2  |
    +- - -+- - -+- - -+
    |  3  |  4  |  5  |
    +- - -+- - -+- - -+
    |  6  |  7  |  8  |
    +- - -+- - -+- - -+

    Args:
        grid:
        square_idx:

    Returns:

    """
    return __get_square_list(grid, square_idx) if isinstance(grid, list) else __get_square_arr(grid, square_idx)


def get_row_for_pos(grid: T, pos: tuple[int, int]) -> T:
    return get_row(grid, pos[0])


def get_col_for_pos(grid: T, pos: tuple[int, int]) -> T:
    return get_col(grid, pos[1])


def get_square_for_pos(grid: T, pos: tuple[int, int]) -> T:
    return get_square(grid, pos_to_square_idx(pos))


def get_unique_numbers(arr: np.ndarray, remove_0: bool = True) -> set[int]:
    unique = set(arr.flatten())
    if remove_0:
        unique.discard(0)
    return unique


def positions() -> Iterable[tuple[int, int]]:
    for x in range(9):
        for y in range(9):
            yield x, y


def create_helper_grid() -> list[list[set]]:
    grid = []
    for _ in range(9):
        row = []
        for _ in range(9):
            row.append(set())
        grid.append(row)
    return grid


def all_numbers() -> set[int]:
    return set(range(1, 10))


def fill_helper_grid(helper_grid: list[list[set]], grid: np.ndarray) -> None:
    for pos in positions():
        if grid[*pos] == 0:
            possible_numbers = all_numbers() \
                               - get_unique_numbers(get_row_for_pos(grid, pos)) \
                               - get_unique_numbers(get_col_for_pos(grid, pos)) \
                               - get_unique_numbers(get_square_for_pos(grid, pos))
            helper_grid[pos[0]][pos[1]].update(possible_numbers)


def __remove_from_row(helper_grid: list[list[set]], row_idx: int, value: int) -> None:
    for possible_vals in get_row(helper_grid, row_idx):
        print(type(possible_vals))
        possible_vals.discard(value)


def __remove_from_col(helper_grid: list[list[set]], col_idx: int, value: int) -> None:
    for possible_vals in get_col(helper_grid, col_idx):
        possible_vals.discard(value)


def __remove_from_square(helper_grid: list[list[set]], square_idx: int, value: int) -> None:
    for row in get_square(helper_grid, square_idx):
        for possible_vals in row:
            possible_vals.discard(value)


def remove_possible_value(helper_grid: list[list[set]], pos: tuple[int, int], value: int) -> None:
    __remove_from_row(helper_grid, pos[0], value)
    __remove_from_col(helper_grid, pos[1], value)
    __remove_from_square(helper_grid, pos_to_square_idx(pos), value)


def find_positions_with_single_possible_value(seq: Sequence[set]) -> list[int]:
    """
    In the sequence (row/column/square) find positions where only one value can be put
    (there is only one value in a set of possible values).

    Args:
        seq:

    Returns:
        list of indexes at which only one value can be put
    """
    found = []
    for index, possible_values in enumerate(seq):
        if len(possible_values) == 1:
            found.append(index)
    return found


def __find_n_equal_subsets_of_n_elements(seq: Sequence[set], n: int) -> list[tuple[tuple[int, int], tuple[int, ...]]]:
    pair_occurrences = defaultdict(list)
    for index, possible_values in enumerate(seq):
        # n possible values in a position
        if len(possible_values) == n:
            pair_occurrences[tuple(sorted(possible_values))].append(index)

    result = []
    for pos_vals, positions in pair_occurrences.items():
        # Pair has to occur exactly n times
        if len(positions) == n:
            result.append((pos_vals, tuple(positions)))

    return result


def find_pairs(seq: Sequence[set]) -> list[tuple[tuple[int, int], tuple[int, int]]]:
    """
    In the sequence (row/column/square) find pairs (exactly the same 2 and only 2 possible values for 2 positions).

    Args:
        seq:

    Returns:
        [((elem1, elem2), index1, index2), ...]
    """
    return __find_n_equal_subsets_of_n_elements(seq, 2)


def find_triplets(seq: Sequence[set]) -> list[tuple[tuple[int, int, int], tuple[int, int, int]]]:
    """
    In the sequence (row/column/square) find triplets (exactly the same 3 and only 3 possible values for 3 positions).

    Args:
        seq:

    Returns:
        [((elem1, elem2, elem3), index1, index2, index3), ...]
    """
    return __find_n_equal_subsets_of_n_elements(seq, 3)


def find_pair_subset(seq: Sequence[set]) -> list[tuple[tuple[int, int], int, int]]:
    """
    In the sequence:
    1. Find all positions that have 2 possible values
    2. From found positions (and possible values) take the ones that fulfill the following requirement:
        - both of the numbers from this position occur in one different position (but this position
          can contain different possible values as well)
        - none of the numbers occur in any different position
    Args:
        seq:

    Returns:
        List of found pair subsets in the following form:
        [((number1, number2), pair position, position with pair as subset), ...]
    """
    possible_vals_2_elem = [(index, s) for index, s in enumerate(seq) if len(s) == 2]

    result = []
    for index, pair in possible_vals_2_elem:
        num1, num2 = sorted(pair)
        num1_in = []
        num2_in = []
        for other_index, other in enumerate(seq):
            if index == other_index:
                continue
            if num1 in other:
                num1_in.append(other_index)
            if num2 in other:
                num2_in.append(other_index)

        if len(num1_in) == 1 and len(num2_in) == 1 and num1_in[0] == num2_in[0]:
            result.append(((num1, num2), index, num1_in[0]))
    return result


def find_places_in_sequence_for_values(seq: Sequence[set], values: Iterable[int]) -> list[tuple[int, int]]:
    """
    Find numbers which can be placed in only one position in the sequence (row/column/square).

    Argument seq contains sequence of sets that indicates which values can be placed in each position.
    From the iterable of values find ones which can be placed in only one position in the seq
    (it means that there is only one position where this value can be put).


    Args:
        seq:
        values:

    Returns:
        list of values that can be placed in only one position in format: [(index_in_seq, value), ...]
    """
    found_places = []
    for val in values:
        possible_places = []
        for index, possible_values in enumerate(seq):
            if val in possible_values:
                possible_places.append(index)
        if len(possible_places) == 1:
            found_places.append((possible_places[0], val))
    return found_places
