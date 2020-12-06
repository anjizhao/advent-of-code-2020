

with open('input.txt', 'r') as f: 
    lines = f.readlines()

lines = [l.strip() for l in lines]

# check all lines have same length
lengths = set([len(l) for l in lines])
assert len(lengths) == 1

grid_width = lengths.pop()


# slope given in problem: right 3, down 1
# to get location for each row: row index * 3 

encounters = []
for i, row in enumerate(lines):
    check_index = i * 3 
    check_index_mod = check_index % grid_width
    item = row[check_index_mod]
    encounters.append(item)
    
# print(encounters) 

trees = [e for e in encounters if e == '#']

print(len(trees))





