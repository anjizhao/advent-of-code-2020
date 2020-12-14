import numpy as np

with open('input.txt', 'r') as f:
    lines = f.readlines()

# convert each line to a list of characters
lines = [list(l.strip()) for l in lines]
seats = np.array(lines)

test_seats = np.array(
    [['L', '.', 'L', 'L', '.', 'L', 'L', '.', 'L', 'L'], ['L', 'L', 'L', 'L', 'L', 'L', 'L', '.', 'L', 'L'], ['L', '.', 'L', '.', 'L', '.', '.', 'L', '.', '.'], ['L', 'L', 'L', 'L', '.', 'L', 'L', '.', 'L', 'L'],  # NOQA
    ['L', '.', 'L', 'L', '.', 'L', 'L', '.', 'L', 'L'], ['L', '.', 'L', 'L', 'L', 'L', 'L', '.', 'L', 'L'], ['.', '.', 'L', '.', 'L', '.', '.', '.', '.', '.'], ['L', 'L', 'L', 'L', 'L', 'L', 'L', 'L', 'L', 'L'],  # NOQA
    ['L', '.', 'L', 'L', 'L', 'L', 'L', 'L', '.', 'L'], ['L', '.', 'L', 'L', 'L', 'L', 'L', '.', 'L', 'L']]  # NOQA
)

def get_adjacent_seats(seatmap, i,j):
    # returns list of who is in seats adjacent to seatmap[i,j] (up to 8)

    i_limit, j_limit = seatmap.shape

    # get the adjacent seats
    adjacent_seats = []

    if i > 0:
        if j > 0:
            adjacent_seats.append(seatmap[i - 1, j - 1])
        adjacent_seats.append(seatmap[i - 1, j])
        if j < j_limit - 1:
            adjacent_seats.append(seatmap[i - 1, j + 1])

    if j > 0:
        adjacent_seats.append(seatmap[i, j - 1])
    # do NOT count THIS seat!!!!! // adjacent_seats.append(seatmap[i, j])
    if j < j_limit - 1:
        adjacent_seats.append(seatmap[i, j + 1])

    if i < i_limit - 1:
        if j > 0:
            adjacent_seats.append(seatmap[i + 1, j - 1])
        adjacent_seats.append(seatmap[i + 1, j])
        if j < j_limit - 1:
            adjacent_seats.append(seatmap[i + 1, j + 1])

    return adjacent_seats


def seat_changes(seatmap, i, j):
    # return True if seat changes, False if not
    # if seat is empty and 0 adjacent seats are occupied, it becomes occupied
    # if seat is occupied and 4+ adjacent seats are occupied, it becomes empty
    # otherwise no change

    this_seat = seatmap[i,j]

    if this_seat == '.':
        return False

    adjacent_seats = get_adjacent_seats(seatmap, i, j)
    adjacent_occupied = adjacent_seats.count('#')

    if this_seat == 'L' and adjacent_occupied == 0:
        return True

    if this_seat == '#' and adjacent_occupied >= 4:
        return True

    return False


# test that indexing works and empty seats change to filled
assert seat_changes(test_seats, 0, 0) is True
assert seat_changes(test_seats, 1, 1) is True
assert seat_changes(test_seats, 9, 9) is True

# test floors never change
assert seat_changes(test_seats, 9, 1) is False


def change_seats(seats):
    # takes an array of seats and applies one round of seat change rules
    # if there are changes, returns the new seat map
    # if there are no changes, returns None
    new_seats = seats.copy()

    has_changes = False

    for i in range(seats.shape[0]):
        for j in range(seats.shape[1]):
            this_seat = seats[i, j]
            change = seat_changes(seats, i, j)
            if change:
                has_changes = True
                if this_seat == 'L':
                    new_seats[i, j] = '#'
                elif this_seat == '#':
                    new_seats[i, j] = 'L'

    if has_changes:
        return new_seats


# my_test_seats = test_seats
my_test_seats = seats

while True:
    new_seats = change_seats(my_test_seats)
    if new_seats is not None:
        my_test_seats = new_seats
    else:
        print('no more changes')
        print('final seats:')
        print(my_test_seats)
        occupied = my_test_seats == '#'
        print('final count occupied:', occupied.sum())
        break
