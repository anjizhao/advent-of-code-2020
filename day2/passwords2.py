
with open('input.txt', 'r') as f:
    lines = f.readlines()

items = [l.strip() for l in lines]


def parse_item(item):
    policy, password = item.split(': ')
    numbers, letter = policy.split(' ')
    min, max = numbers.split('-')
    return {'letter': letter, 'min': int(min), 'max': int(max), 'password': password}

def is_valid(parsed):
    i = parsed['min'] - 1
    j = parsed['max'] - 1
    char_i = parsed['password'][i]
    char_j = parsed['password'][j]
    if (char_i == parsed['letter']) + (char_j == parsed['letter']) == 1:
        return True
    # print((char_i, char_j))
    return False

# print(parse_item(items[0]))
# print(is_valid(parse_item(items[0])))

def check_item(item):
    return is_valid(parse_item(item))


checked = [check_item(i) for i in items]

print(sum(checked))



