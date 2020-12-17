
from collections import defaultdict

starting_numbers = [0, 5, 4, 1, 10, 14, 7]
# starting_numbers = [0, 3, 6]  # test

numbers = defaultdict(list)

last_number = None
# for turn in range(1, 30000001):  # for part 2. this is not efficient lol
for turn in range(1, 2021):
    if turn <= len(starting_numbers):
        this_number = starting_numbers[turn - 1]
    else:
        prev_turns_for_last_number = numbers[last_number]
        if len(prev_turns_for_last_number) == 1:
            this_number = 0
        else:
            last_two_turns = prev_turns_for_last_number[-2:]
            this_number = last_two_turns[1] - last_two_turns[0]

    numbers[this_number].append(turn)
    last_number = this_number

print(last_number)
