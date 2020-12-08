
with open('input.txt', 'r') as f:
    lines = f.readlines()

items = [l.strip() for l in lines]


def parse_item(item):
    policy, password = item.split(': ')
    numbers, letter = policy.split(' ')
    min, max = numbers.split('-')
    return {'letter': letter, 'min': int(min), 'max': int(max), 'password': password}

def is_valid(parsed):
    count = parsed['password'].count(parsed['letter'])
    # print(count)
    if (count < parsed['min']) or (count > parsed['max']):
        return False
    return True

# print(is_valid(parse_item(items[0])))

def check_item(item):
    return is_valid(parse_item(item))


checked = [check_item(i) for i in items]

print(sum(checked))



