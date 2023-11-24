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


# Cannot use list[list] int TypeVar, because get_row and get_col will reduce "number of dims" in nested list
T = TypeVar('T', np.ndarray, list)


def get_row(grid: T, row_idx: int) -> T:
    return __get_row_list(grid, row_idx) if isinstance(grid, list) else __get_row_arr(grid, row_idx)


def get_col(grid: T, col_idx: int) -> T:
    return __get_col_list(grid, col_idx) if isinstance(grid, list) else __get_col_arr(grid, col_idx)


def get_square(grid: T, square_idx: int) -> T:
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
