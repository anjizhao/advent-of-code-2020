

with open('input.txt', 'r') as f:
    lines = f.readlines()

lines = [l.strip() for l in lines]
# print(lines[:2])

# example seat: FBFBBFFRLR
# plane has 128 rows (numbered 0 to 127)
# each row has 8 seats (numbered 0 to 7)

def get_row(rows_str):
    # rows_str is 7 characters, F or B
    rows = range(128)
    for c in rows_str:
        middle = len(rows) // 2
        if c == 'F':
            rows = rows[:middle]
        elif c == 'B':
            rows = rows[middle:]
        # print(c, middle, rows)
    assert len(rows) == 1
    return rows[0]

def get_seat(seats_str):
    # seats_str is 3 characters, L or R
    seats = range(8)
    for c in seats_str:
        middle = len(seats) // 2
        if c == 'L':
            seats = seats[:middle]
        elif c == 'R':
            seats = seats[middle:]
        # print(c, middle, seats)
    assert len(seats) == 1
    return seats[0]

# print(get_row('FBFBBFF'))
# print(get_seat('RLR'))

def read_pass(pass_str):
    assert len(pass_str) == 10
    row = get_row(pass_str[:7])
    seat = get_seat(pass_str[7:])
    return (row, seat)

assert read_pass('BFFFBBFRRR') == (70, 7)

decoded = [read_pass(s) for s in lines]
seat_ids = [row * 8 + seat for row, seat in decoded]

print(max(seat_ids))



# part 2

sorted_seats = sorted(seat_ids)

# find my seat (only one gap between all seat ids)
for i in range(len(sorted_seats)-1):
    if (sorted_seats[i] + 1) != sorted_seats[i+1]:
        print(sorted_seats[i] + 1)








