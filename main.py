from collections.abc import Iterable
from pprint import pprint

import numpy as np


def read(path: str) -> np.ndarray:
    with open(path, 'r', encoding='utf8') as f:
        lines = f.readlines()
    lines = [[int(char) for char in line.strip()] for line in lines]
    return np.array(lines)


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


##
def square_idx_to_grid_indices(square_idx: int) -> tuple[tuple[int, int], tuple[int, int]]:
    square_row_idx = square_idx // 3
    square_col_idx = square_idx % 3

    return indices_square_to_grid(square_row_idx, square_col_idx)


def pos_to_square_idx(pos: tuple[int, int]) -> int:
    return pos[0] * 3 + pos[1]


def get_row(grid: np.ndarray, row_idx: int) -> np.ndarray:
    return grid[row_idx, :]


def get_col(grid: np.ndarray, col_idx: int) -> np.ndarray:
    return grid[:, col_idx]


def get_square(grid: np.ndarray, square_idx: int) -> np.ndarray:
    (row_start, row_end), (col_start, col_end) = square_idx_to_grid_indices(square_idx)
    return grid[row_start: row_end, col_start: col_end]


def get_row_for_pos(grid: np.ndarray, pos: tuple[int, int]) -> np.ndarray:
    return get_row(grid, pos[0])


def get_col_for_pos(grid: np.ndarray, pos: tuple[int, int]) -> np.ndarray:
    return get_col(grid, pos[1])


def get_square_for_pos(grid: np.ndarray, pos: tuple[int, int]) -> np.ndarray:
    return get_square(grid, pos_to_square_idx(pos))


def unique_numbers(arr: np.ndarray) -> set[int]:
    return set(arr.flatten())


##

def numbers_in_row(grid: np.ndarray, pos: tuple[int, int] | int) -> set[int]:
    if isinstance(pos, int):
        row_idx = pos
    else:
        row_idx = pos[0]
    return set(grid[row_idx, :].flatten())  # todo - remove 0?


def numbers_in_col(grid: np.ndarray, pos: tuple[int, int] | int) -> set[int]:
    if isinstance(pos, int):
        col_idx = pos
    else:
        col_idx = pos[1]
    return set(grid[:, col_idx].flatten())


def indices_square_to_grid(square_row_idx: int, square_col_idx: int) -> tuple[tuple[int, int], tuple[int, int]]:
    row_start = square_row_idx * 3
    row_end = row_start + 3

    col_start = square_col_idx * 3
    col_end = col_start + 3

    return (row_start, row_end), (col_start, col_end)


def get_square_indices(pos: tuple[int, int]) -> tuple[tuple[int, int], tuple[int, int]]:
    """
            0       1       2
          0 1 2 | 3 4 5 | 6 7 8
       0
     0 1            +           -> (1,4) -> (0,1) -> ((0,3), (3,6))
       2
       -
       3
     1 4
       5
       -
       6
     2 7
       8

    Args:
        pos:

    Returns:

    """
    square_row_idx = pos[0] // 3
    square_col_idx = pos[1] // 3

    return indices_square_to_grid(square_row_idx, square_col_idx)


def get_square_indices_from_square_idx(square_idx: int) -> tuple[tuple[int, int], tuple[int, int]]:
    square_row_idx = square_idx // 3
    square_col_idx = square_idx % 3

    return indices_square_to_grid(square_row_idx, square_col_idx)


def get_square_from_idx(grid: np.ndarray, square_idx: int) -> np.ndarray:
    """

    Square indices:
    +---+---+---+
    | 0 | 1 | 2 |
    +---+---+---+
    | 3 | 4 | 5 |
    +---+---+---+
    | 6 | 7 | 8 |
    +---+---+---+


    Args:
        grid:
        square_idx:

    Returns:

    """
    square_row_idx = square_idx // 3
    square_col_idx = square_idx % 3


def get_square(grid: np.ndarray, pos: tuple[int, int]) -> np.ndarray:
    (row_start, row_end), (col_start, col_end) = get_square_indices(pos)
    return grid[row_start:row_end, col_start: col_end]


def numbers_in_square(grid: np.ndarray, pos: tuple[int, int]) -> set[int]:
    return set(get_square(grid, pos).flatten())


def get_square_helper(helper_grid: list[list[set]], position: tuple[int, int]) -> list[list[set]]:
    (row_start, row_end), (col_start, col_end) = get_square_indices(position)
    square = []
    for r in range(row_start, row_end):
        row = helper_grid[r]
        square.append(row[col_start:col_end])
    return square


path = 'input.txt'

grid = read(path)
print(grid)

helper_grid = create_helper_grid()

pprint(helper_grid)

print(all_numbers())

for pos in positions():
    if grid[*pos] == 0:
        possible_numbers = all_numbers() - numbers_in_row(grid, pos) - numbers_in_col(grid, pos) - numbers_in_square(
            grid, pos)
        helper_grid[pos[0]][pos[
            1]] = possible_numbers  # todo - replace list in helper grid with set (and tuples) and modify the set here instead of assigning a new one
    else:
        helper_grid[pos[0]][pos[1]] = set()

pprint(helper_grid)


def remove_possible_val(helper_grid: list[list[set]], position: tuple[int, int], value: int) -> None:
    # remove from row
    row_ = helper_grid[position[0]]
    for possible_vals in row_:
        possible_vals.discard(value)
    # remove from column
    for row_ in helper_grid:
        possible_vals = row_[position[1]]
        possible_vals.discard(value)
    # remove from square
    square_ = get_square_helper(helper_grid, position)
    for row_ in square_:
        for possible_vals in row_:
            possible_vals.discard(value)


for row_idx in range(9):
    # Find fields with single possible value
    # Find pairs
    # Find triples
    # Find pair subsets

    # Find numbers which can be placed in only one position
    missing = all_numbers() - set(grid[row_idx, :].flatten())
    for m in missing:
        possible_places = []
        for col_idx, possible_values in enumerate(helper_grid[row_idx]):
            if m in possible_values:
                possible_places.append((row_idx, col_idx))
        print(m, possible_places)
        if len(possible_places) == 1:
            position = possible_places[0]
            grid[*position] = m

            # update grid
            remove_possible_val(helper_grid, position, m)

            pprint(grid)
            pprint(helper_grid)

        # (optional) add positions where updated to possible places to check

# for col_idx ....

# for square_idx ...

# find fields with single possible value
# find pairs
# find triples
# find pair subsets
