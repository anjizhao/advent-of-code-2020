
with open('input.txt', 'r') as f:
    lines = f.readlines()

lines = [l.strip() for l in lines]

operations = [l.split(' = ') for l in lines]

test_operations = [
    ['mask', 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X'],
    ['mem[8]', '11'],
    ['mem[7]', '101'],
    ['mem[8]', '0'],
]
# operations = test_operations

MASK = {
    'string': '',
    'mask_0': 1,
    'mask_1': 0,
}
MEMORY = {}

def set_mask(mask_str):
    MASK['string'] = mask_str
    MASK['mask_0'] = int(mask_str.replace('X', '1'), 2)
    MASK['mask_1'] = int(mask_str.replace('X', '0'), 2)

def parse_address(mem_str):
    address_str = op[0][4:-1]
    assert address_str.isdigit()
    return int(address_str)

def apply_mask_to_value(original):
    masked = (original & MASK['mask_0']) | MASK['mask_1']
    return masked

for op in operations:
    # print(op)
    if op[0] == 'mask':
        set_mask(op[1])
        # print(mask)
    else:
        address = parse_address(op[0])
        value = int(op[1])
        masked_value = apply_mask_to_value(value)
        MEMORY[address] = masked_value

# print(MEMORY)

result = sum(MEMORY.values())
print(result)
