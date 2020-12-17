import numpy as np

with open('input.txt', 'r') as f:
    lines = f.readlines()

# test_lines = ['.#.', '..#', '###']
# lines = test_lines

# convert each line to a list of characters
lines = [list(l.strip()) for l in lines]
initial_slice = np.array(lines)

# convert values to 1s (for active) and 0s
active = np.full(initial_slice.shape, '#')
initial_slice = (initial_slice == active).astype(int)

# print(initial_slice)

# convert slice to full (hyper)cube
length = initial_slice.shape[0]
initial_data = np.zeros(shape=(length, length, length, length), dtype=int)
initial_data[None, None, 1, 1] = initial_slice
# print(initial_data)


def extend_array(initial_data):
    # create new array that adds an extra row/column on each side
    length = initial_data.shape[0]
    new_cube = np.zeros(
        shape=(length + 2, length + 2, length + 2, length + 2),
        dtype=int,
    )
    # now put the initial data in the middle
    new_cube[
        1:(length + 1), 1:(length + 1), 1:(length + 1), 1:(length + 1)
    ] = initial_data
    return new_cube


initial_data_padded = extend_array(initial_data)
# print(initial_data_padded)


def count_active_adjacent(data, i, j, k, m):
    # get the 81-cell hypercube with (i, j, k, m) in the middle
    subcube = data[i - 1:i + 2, j - 1:j + 2, k - 1:k + 2, m - 1:m + 2]
    # get total active, ignoring the center cube (i,j,k,m)
    count = subcube.sum() - subcube[1, 1, 1, 1]
    return count


def cube_flips(data, i, j, k, m):
    # return True if cube changes, False if not
    # if cube is active & active neighbor count NOT in [2,3], it changes
    # if cube is inactive & exactly 3 neighbors are active, it changes
    # otherwise no change

    this_cube = data[i, j, k, m]

    active_adjacent = count_active_adjacent(data, i, j, k, m)

    if this_cube and active_adjacent not in (2, 3):
        return True

    if not this_cube and active_adjacent == 3:
        return True

    return False


def change_cubes(cubes):
    # takes an array of (padded) cubes and applies one cycle
    # returns the new cube array
    length = cubes.shape[0]
    new_cubes = cubes.copy()
    # print(cubes)
    for i in range(1, length - 1):
        for j in range(1, length - 1):
            for k in range(1, length - 1):
                for m in range(1, length - 1):
                    # print(i,j)
                    this_seat = cubes[i, j, k, m]
                    change = cube_flips(cubes, i, j, k, m)
                    if change:
                        new_cubes[i, j, k, m] = this_seat ^ 1

    return new_cubes


current_cubes = initial_data_padded
for i in range(6):
    data = extend_array(current_cubes)
    current_cubes = change_cubes(data)

print(current_cubes.sum())
# print(current_cubes[:, :, 10])
