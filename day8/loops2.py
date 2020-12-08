

with open('input.txt', 'r') as f:
    lines = f.readlines()

lines = [l.strip() for l in lines]

instructions = []

for l in lines:
    operation, argument_str = l.split(' ')
    instructions.append((operation, int(argument_str)))    

# print(instructions[:2])


def run_with_one_operation_swap(swap_index):
    index = 0
    accumulator = 0
    visited = set()
    
    for i in range(10000):
    # while True:
        if index in visited:
            return False
        if index == len(instructions):
            return accumulator
        visited.add(index)
        instruction = instructions[index]
        if instruction[0] == 'nop':
            if index == swap_index:
                index += instruction[1]
                continue
            index += 1
            continue
        if instruction[0] == 'acc':
            accumulator += instruction[1]
            index += 1
            continue
        if instruction[0] == 'jmp':
            if index == swap_index:
                index += 1
                continue
            index += instruction[1]
            continue

for i in range(len(instructions)):
    if instructions[i][0] == 'acc': 
        continue
    result = run_with_one_operation_swap(i)
    if result:
        print('swap index', i)
        print('accumulated', result)



