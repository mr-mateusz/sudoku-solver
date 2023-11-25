from pprint import pprint

import numpy as np

from functions import create_helper_grid, all_numbers, fill_helper_grid, remove_possible_val


def read(path: str) -> np.ndarray:
    with open(path, 'r', encoding='utf8') as f:
        lines = f.readlines()
    lines = [[int(char) for char in line.strip()] for line in lines]
    return np.array(lines)


path = 'input.txt'

grid = read(path)
print(grid)

helper_grid = create_helper_grid()

pprint(helper_grid)

print(all_numbers())

fill_helper_grid(helper_grid, grid)

pprint(helper_grid)

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
