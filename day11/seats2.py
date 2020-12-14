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

def get_visible_seats(seatmap, i,j):
    # returns list of who is in seats visible from seatmap[i,j] (up to 8)

    i_limit, j_limit = seatmap.shape

    visible_seats = []

    # up left
    m, n = i, j
    while m > 0 and n > 0:
        m -= 1
        n -= 1
        if seatmap[m, n] == '.':
            continue
        else:
            visible_seats.append(seatmap[m, n])
            break

    # up
    m = i
    while m > 0:
        m -= 1
        if seatmap[m, j] == '.':
            continue
        else:
            visible_seats.append(seatmap[m, j])
            break

    # up right
    m, n = i, j
    while m > 0 and n < j_limit - 1:
        m -= 1
        n += 1
        if seatmap[m, n] == '.':
            continue
        else:
            visible_seats.append(seatmap[m, n])
            break

    # left
    n = j
    while n > 0:
        n -= 1
        if seatmap[i, n] == '.':
            continue
        else:
            visible_seats.append(seatmap[i, n])
            break

    # right
    n = j
    while n < j_limit - 1:
        n += 1
        if seatmap[i, n] == '.':
            continue
        else:
            visible_seats.append(seatmap[i, n])
            break

    # down left
    m, n = i, j
    while m < i_limit - 1 and n > 0:
        m += 1
        n -= 1
        if seatmap[m, n] == '.':
            continue
        else:
            visible_seats.append(seatmap[m, n])
            break

    # down
    m = i
    while m < i_limit - 1:
        m += 1
        if seatmap[m, j] == '.':
            continue
        else:
            visible_seats.append(seatmap[m, j])
            break

    # down right
    m, n = i, j
    while m < i_limit - 1 and n < j_limit - 1:
        m += 1
        n += 1
        if seatmap[m, n] == '.':
            continue
        else:
            visible_seats.append(seatmap[m, n])
            break

    return visible_seats

# print(test_seats)
assert get_visible_seats(test_seats, 0, 0) == ['L', 'L', 'L']
assert get_visible_seats(test_seats, 0, 1) == ['L', 'L', 'L', 'L', 'L']
assert get_visible_seats(test_seats, 1, 1) == ['L', 'L', 'L', 'L', 'L', 'L', 'L']  ## noqa
assert get_visible_seats(test_seats, 2, 7) == ['L', 'L', 'L', 'L', 'L', 'L']


def seat_changes(seatmap, i, j):
    # return True if seat changes, False if not
    # if seat is empty and 0 visible seats are occupied, it becomes occupied
    # if seat is occupied and 5+ visible seats are occupied, it becomes empty
    # otherwise no change

    this_seat = seatmap[i,j]

    if this_seat == '.':
        return False

    visible_seats = get_visible_seats(seatmap, i, j)
    visible_occupied = visible_seats.count('#')

    if this_seat == 'L' and visible_occupied == 0:
        return True

    if this_seat == '#' and visible_occupied >= 5:
        return True

    return False


# test that indexing works and empty seats change to filled
assert seat_changes(test_seats, 0, 0) is True
assert seat_changes(test_seats, 1, 1) is True
assert seat_changes(test_seats, 9, 9) is True

# test that floors never change
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
