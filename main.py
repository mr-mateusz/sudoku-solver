from collections.abc import Iterable
from pprint import pprint

import numpy as np

from functions import get_row_for_pos, get_col_for_pos, get_square_for_pos, unique_numbers


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


path = 'input.txt'

grid = read(path)
print(grid)

helper_grid = create_helper_grid()

pprint(helper_grid)

print(all_numbers())


def fill_helper_grid(helper_grid: list[list[set]], grid: np.ndarray) -> None:
    for pos in positions():
        if grid[*pos] == 0:
            possible_numbers = all_numbers() \
                               - unique_numbers(get_row_for_pos(grid, pos)) \
                               - unique_numbers(get_col_for_pos(grid, pos)) \
                               - unique_numbers(get_square_for_pos(grid, pos))
            helper_grid[pos[0]][pos[1]].update(possible_numbers)


fill_helper_grid(helper_grid, grid)

pprint(helper_grid)


def remove_possible_val(helper_grid: list[list[set]], pos: tuple[int, int], value: int) -> None:
    # Todo refactor after writing unit tests
    # remove from row
    row_ = helper_grid[pos[0]]
    for possible_vals in row_:
        possible_vals.discard(value)
    # remove from column
    for row_ in helper_grid:
        possible_vals = row_[pos[1]]
        possible_vals.discard(value)
    # remove from square
    square_ = get_square_for_pos(helper_grid, pos)
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
