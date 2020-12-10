from collections import defaultdict

with open('input.txt', 'r') as f:
    lines = f.readlines()

adapters = sorted([int(l.strip()) for l in lines])

# adapters = sorted([16,10,15,5,1,11,7,19,6,12,4])  # example test

# print(len(adapters))
# print(adapters[:10])


# map each adapter to a list of valid next adapters

allowed_steps = defaultdict(list)

charging_outlet = 0
last_adapter = adapters[-1]

for a in [charging_outlet] + adapters:
    for i in range(1,4):
        if a+i in adapters:
            allowed_steps[a].append(a+i)

# print(allowed_steps)

WAYS = {}

def f(adapter):
    '''
    ways to get to last_adapter from this adapter
    recursive function
    '''

    # base/end step
    if adapter == last_adapter:
        return 1

    # check if we already know how many ways from this number
    if WAYS.get(adapter) is not None:
        return WAYS.get(adapter)

    # otherwise, call this same function for all allowed next steps
    # and take the sum of all the return values

    next_step_choices = allowed_steps[adapter]

    ways = sum([f(n) for n in next_step_choices])
    WAYS[adapter] = ways
    return ways


# test last couple of steps
# assert f(last_adapter) == 1
# assert f(137) == 1
# assert f(136) == 2
# assert f(135) == 4

total_ways = f(charging_outlet)
print(total_ways)

# print(WAYS)



