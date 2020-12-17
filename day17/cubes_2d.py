import numpy as np

with open('input.txt', 'r') as f:
    lines = f.readlines()

test_lines = ['.#.', '..#', '###']
lines = test_lines

# convert each line to a list of characters
lines = [list(l.strip()) for l in lines]
initial_slice = np.array(lines)

# convert values to 1s (for active) and 0s
active = np.full(initial_slice.shape, '#')
initial_data = (initial_slice == active).astype(int)

# print(initial_slice)
# print(initial_data)


def extend_array(initial_data):
    # create new array that adds an extra row/column on each side
    initial_h, initial_w = initial_data.shape
    new_square = np.zeros(shape=(initial_h + 2, initial_w + 2), dtype=int)
    # now put the initial data in the middle
    new_square[1:(initial_h + 1), 1:(initial_w + 1)] = initial_data
    return new_square

initial_data_padded = extend_array(initial_data)
# print(initial_data_padded)


def count_active_adjacent(data, i, j):
    # get the 9-cell square with (i, j) in the middle
    subslice = data[i - 1:i + 2, j - 1:j + 2]
    count = subslice.sum() - subslice[1, 1]  # get total active, ignoring (i,j)
    return count


def cube_flips(data, i, j):
    # return True if cube changes, False if not
    # if cube is active & active neighbor count NOT in [2,3], it changes
    # if cube is inactive & exactly 3 neighbors are active, it changes
    # otherwise no change

    this_cube = data[i,j]

    active_adjacent = count_active_adjacent(data, i, j)

    if this_cube and active_adjacent not in (2, 3):
        return True

    if not this_cube and active_adjacent == 3:
        return True

    return False


def change_cubes(cubes):
    # takes an array of (padded) cubes and applies one cycle
    # returns the new cube array
    new_cubes = cubes.copy()
    # print(cubes)
    for i in range(1, cubes.shape[0] - 1):
        for j in range(1, cubes.shape[1] - 1):
            # print(i,j)
            this_seat = cubes[i, j]
            change = cube_flips(cubes, i, j)
            if change:
                new_cubes[i, j] = this_seat ^ 1

    return new_cubes


current_cubes = initial_data_padded
for i in range(6):
    data = extend_array(current_cubes)
    current_cubes = change_cubes(data)

print(current_cubes.sum())
