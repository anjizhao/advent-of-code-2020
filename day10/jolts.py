from collections import defaultdict

with open('input.txt', 'r') as f:
    lines = f.readlines()

adapters = sorted([int(l.strip()) for l in lines])

# adapters = sorted([16,10,15,5,1,11,7,19,6,12,4])  # example test

# print(len(adapters))
# print(adapters[:10])

counts = defaultdict(int)

for i in range(len(adapters)):
    if i == 0:
        last_step = adapters[i]
    else:
        last_step = adapters[i] - adapters[i-1]
    counts[last_step] += 1

counts[3] += 1  # built-in adapter is 3 higher than the largest adapter

print(counts)

print(counts[1]*counts[3])




