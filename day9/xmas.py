

with open('input.txt', 'r') as f:
    lines = f.readlines()

numbers = [int(l.strip()) for l in lines]

# print(numbers[:10])

preamble_len = 25

def valid_next_number(previous_numbers, this_number):
    prev_set = set(previous_numbers)
    for p in previous_numbers:
        prev_set.remove(p)
        if this_number - p in prev_set:
            return True
        prev_set.add(p)
    return False

assert valid_next_number([35,20,15,25,47], 40)
assert not valid_next_number([35,20,15,25,47], 42)
assert not valid_next_number([95,102,117,150,192], 127)


# find first invalid number
first_invalid = None
for i in range(preamble_len, len(numbers)):
    previous_list = numbers[i - preamble_len: i]
    if not valid_next_number(previous_list, numbers[i]):
        print('first invalid number', numbers[i])
        first_invalid = numbers[i]
        break


# find contiguous set of at least 2 numbers in full list which sum to that invalid number


def test_start_index(i):
    # returns set of addends if the start index is valid
    # i is the "start" index of each contiguous set we will be testing
    i_sum = numbers[i]
    # print(i_sum)
    for j in range(i+1, len(numbers)):
        i_sum += numbers[j]
        # print('added', numbers[j], 'total', i_sum)
        if i_sum > first_invalid:
            # we already exceeded the target number so we know i is not the correct start index
            return False
        elif i_sum == first_invalid:
            print('found set')
            print('beginning/end indices:', i, j)
            addends = numbers[i:j+1]
            print('min/max in set:', min(addends), max(addends))
            return addends


def go():
    for i in range(len(numbers)):
        result = test_start_index(i)
        if result:
            print(result)
            return result


result_list = go()

print(min(result_list) + max(result_list))




