
with open('input.txt', 'r') as f:
    lines = f.readlines()

lines = [l.strip() for l in lines]

bus_ids_raw = lines[1].split(',')

bus_ids = []

test_bus_ids_raw = '7,13,x,x,59,x,31,19'.split(',')
# bus_ids_raw = test_bus_ids_raw

for index, bus in enumerate(bus_ids_raw):
    if bus.isdigit():
        bus_ids.append((index, int(bus)))

print(bus_ids)
bus_ids_sorted = sorted(bus_ids, key=lambda x: x[1], reverse=True)
print(bus_ids_sorted)

# in bus_ids_sorted we have (r1, b) pairs s.t. t + r1 = 0 (mod b), but we want
# it in form t = r2 (mod b). subtract r1 from both sides & take mod b to get r2
bus_ids_sorted_mod = [(i[0] * (-1) % i[1], i[1]) for i in bus_ids_sorted]
print(bus_ids_sorted_mod)


def find_next_bus(bus_ids_sorted):
    '''
    i am trying to do this:
    https://en.wikipedia.org/wiki/Chinese_remainder_theorem#Search_by_sieving
    '''
    base = 1
    t = 0
    for r, m in bus_ids_sorted:
        # m is the modulo and r is the remainder we expect
        # for i in range(1000):
        i = 0
        while True:
            remainder = (i * base + t) % m
            # print('({} * {} + {}) % {} = {}'.format(i, base, t, m, remainder))  # noqa
            if remainder == r:
                t = (i * base + t)
                # print((r, m), 'done, t =', t)
                base = base * m
                break
            i += 1
    return base, t

res = find_next_bus(bus_ids_sorted_mod)
print(res)



# test_bus_ids = [7, 13, 59, 31, 19]
# assert find_next_bus(test_bus_ids) == (59, 944)
