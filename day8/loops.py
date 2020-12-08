

with open('input.txt', 'r') as f:
    lines = f.readlines()

lines = [l.strip() for l in lines]

instructions = []

for l in lines:
    operation, argument_str = l.split(' ')
    instructions.append((operation, int(argument_str)))    

# print(instructions[:2])

index = 0
accumulator = 0
visited = set()

# for i in range(1000):
while True:
    if index in visited:
        break
    visited.add(index)
    instruction = instructions[index]
    if instruction[0] == 'nop':
        index += 1
        continue
    if instruction[0] == 'acc':
        accumulator += instruction[1]
        index += 1
        continue
    if instruction[0] == 'jmp':
        index += instruction[1]
        continue

print(visited)
print('accumulated:', accumulator)
print('operations:', len(visited))





