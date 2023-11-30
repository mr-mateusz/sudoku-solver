import itertools
from pprint import pprint

import numpy as np

from src.functions import create_helper_grid, all_numbers, fill_helper_grid, remove_possible_value, get_unique_numbers, \
    get_row, get_col, get_square, square_and_position_indices_to_absolute_position, \
    find_places_in_sequence_for_values, find_positions_with_single_possible_value, find_pairs, find_triplets, \
    find_pair_subset


def read(path: str) -> np.ndarray:
    with open(path, 'r', encoding='utf8') as f:
        lines = f.readlines()
    lines = [[int(char) for char in line.strip()] for line in lines]
    return np.array(lines)


path = 'input.txt'

grid = read(path)
print(grid)

helper_grid = create_helper_grid()

fill_helper_grid(helper_grid, grid)

pprint(helper_grid)


def clear_possible_values(helper_grid: list[list[set]], position: tuple[int, int]) -> None:
    helper_grid[position[0]][position[1]].clear()


def place_value(grid: np.ndarray, helper_grid: list[list[set]], position: tuple[int, int], value: int) -> None:
    if grid[*position] != 0:
        raise ValueError(f'Position {position} not empty')

    grid[*position] = value
    clear_possible_values(helper_grid, position)
    # todo - find a better name for this function
    remove_possible_value(helper_grid, position, value)


def remove_pairs():
    pass


def remove_triplets():
    pass


def remove_pair_subset():
    pass


def place_values():
    pass


for row_idx in range(9):
    print(row_idx)

    row_possible_vals = get_row(helper_grid, row_idx)

    # Find pos with single possible value
    positions = find_positions_with_single_possible_value(row_possible_vals)
    # Find pairs
    pairs = find_pairs(row_possible_vals)
    # Find triplets
    triplets = find_triplets(row_possible_vals)
    # Find pair subsets
    subsets = find_pair_subset(row_possible_vals)

    # Find numbers which can be placed in only one position
    missing = all_numbers() - get_unique_numbers(get_row(grid, row_idx))
    # row_possible_vals = get_row(helper_grid, row_idx)

    found_places = find_places_in_sequence_for_values(row_possible_vals, missing)
    print(found_places)
    for index, value in found_places:
        position = (row_idx, index)
        grid[*position] = value
        remove_possible_value(helper_grid, position, value)

# for col_idx ....
for col_idx in range(9):
    print(col_idx)

    missing = all_numbers() - get_unique_numbers(get_col(grid, col_idx))
    col_possible_vals = get_col(helper_grid, col_idx)

    found_places = find_places_in_sequence_for_values(col_possible_vals, missing)
    print(found_places)
    for index, value in found_places:
        position = (index, col_idx)
        grid[*position] = value
        remove_possible_value(helper_grid, position, value)

# for square_idx ...
for square_idx in range(9):
    print(square_idx)

    missing = all_numbers() - get_unique_numbers(get_square(grid, square_idx))
    square_possible_vals = list(itertools.chain(*get_square(helper_grid, square_idx)))

    found_places = find_places_in_sequence_for_values(square_possible_vals, missing)
    print(found_places)
    for index, value in found_places:
        position = square_and_position_indices_to_absolute_position(square_idx, index)
        grid[*position] = value
        remove_possible_value(helper_grid, position, value)

# todo
#   - place value function (add to grid and update helper grid)
#   - remove possible vals based on pair, triplet
#   - remove possible vals based on subset
