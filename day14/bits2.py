
with open('input.txt', 'r') as f:
    lines = f.readlines()

lines = [l.strip() for l in lines]

operations = [l.split(' = ') for l in lines]

test_operations = [
    ['mask', '000000000000000000000000000000X1001X'],
    ['mem[42]', '100'],
    ['mask', '00000000000000000000000000000000X0XX'],
    ['mem[26]', '1'],
]
# operations = test_operations

MASK = {
    'string': '',
    'mask_1': 0,
    'x_indices': [],
}
MEMORY = {}

def set_mask(mask_str):
    MASK['string'] = mask_str
    MASK['mask_1'] = int(mask_str.replace('X', '0'), 2)
    MASK['x_indices'] = [i for i, v in enumerate(mask_str) if v == 'X']


def parse_address(mem_str):
    address_str = op[0][4:-1]
    assert address_str.isdigit()
    return int(address_str)


def apply_mask_to_address(original):
    # takes an int and returns a STRING with 1s and Xs overwritten
    # first apply mask that overwrites with 1
    masked_1 = original | MASK['mask_1']
    masked_str = format(masked_1, '036b')  # format as padded binary str
    masked_list = list(masked_str)
    for i in MASK['x_indices']:
        masked_list[i] = 'X'
    masked_str = ''.join(masked_list)
    return masked_str


def get_floating_values(masked_str):
    # takes a STRING like 00010X1010XX001X0. each X can be either a 1 or a 0.
    # returns list of possible INTS the string could represent
    possible_addresses = []

    def replace_xs(s):
        if s.count('X') > 0:
            replace_xs(s.replace('X', '1', 1))  # only replace the first X
            replace_xs(s.replace('X', '0', 1))
        else:
            possible_addresses.append(int(s, 2))

    replace_xs(masked_str)
    return possible_addresses


# test
set_mask(test_operations[0][1])
masked_str = apply_mask_to_address(42)
# print(masked_str)
assert masked_str == '000000000000000000000000000000X1101X'
floating_values = get_floating_values(masked_str)
# print(floating_values)
assert floating_values == [59, 58, 27, 26]


for op in operations:
    # print(op)
    if op[0] == 'mask':
        set_mask(op[1])
        # print(mask)
    else:
        address = parse_address(op[0])
        value = int(op[1])
        masked_address_str = apply_mask_to_address(address)
        possible_addresses = get_floating_values(masked_address_str)
        for a in possible_addresses:
            MEMORY[a] = value

# print(MEMORY)

result = sum(MEMORY.values())
print(result)
