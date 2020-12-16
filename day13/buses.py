
with open('input.txt', 'r') as f:
    lines = f.readlines()

lines = [l.strip() for l in lines]

current_timestamp = int(lines[0])
bus_ids_raw = lines[1].split(',')

bus_ids = [int(i) for i in bus_ids_raw if i != 'x']

print(bus_ids)


def find_next_bus(current_timestamp, bus_ids):
    for t in range(current_timestamp, current_timestamp + 20):
        for bus in bus_ids:
            if t % bus == 0:
                return (bus, t)

test_timestamp = 939
test_bus_ids = [7, 13, 59, 31, 19]
assert find_next_bus(test_timestamp, test_bus_ids) == (59, 944)

result = find_next_bus(current_timestamp, bus_ids)
print(result)

wait = result[1] - current_timestamp
print(wait * result[0])
