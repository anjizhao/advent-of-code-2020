import math

with open('input.txt', 'r') as f:
    lines = f.readlines()

lines = [l.strip() for l in lines]

# print(len(lines))

# check all lines have same length
lengths = set([len(l) for l in lines])
assert len(lengths) == 1

grid_width = lengths.pop()

# slope given in problem: right 3, down 1
# to get location for each row: row index * 3

right = 3
down = 1


def count_trees(right, down):
    encounters = []
    for i, row in enumerate(lines):
        # skip rows if down > 1 ...
        if i % down != 0:
            continue
        row_index = int(i / down * right)
        row_index_mod = row_index % grid_width
        item = row[row_index_mod]
        encounters.append(item)
    trees = [e for e in encounters if e == '#']
    return len(trees)

def print_count_trees(right, down):
    print('right {}, down {}: {} trees'.format(right, down, count_trees(right, down)))


slopes = [
    (1, 1),
    (3, 1),
    (5, 1),
    (7, 1),
    (1, 2),
]


for args in slopes:
   print_count_trees(*args)


trees_for_all_slopes = [count_trees(*args) for args in slopes]

print(trees_for_all_slopes)
print(math.prod(trees_for_all_slopes))




