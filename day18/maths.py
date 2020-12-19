
with open('input.txt', 'r') as f:
    lines = f.readlines()

lines = [l.strip() for l in lines]
test_lines = [
    '1 + 2 * 3 + 4 * 5 + 6',
    '(1 + 2) * 3 + 4 * 5 + 6',
    '1 + (2 * 3) + (4 * (5 + 6))',
    '2 * 3 + (4 * 5)',
    '5 + (8 * 3 + 9 + 3 * 4 * 3)',
    '5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))',
    '((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2',
]

def evaluate(raw_str):
    padded = '({})'.format(raw_str)
    exp_str = padded.replace('(', '( ').replace(')', ' )')  # add spaces lol
    assert len(exp_str) % 2 == 1  # should have odd # of characters
    exp_list = exp_str.split(' ')
    exp_iter = iter(exp_list)
    return evaluate_iter(exp_iter)


def is_operator(c):
    if c in ['+', '*']:
        return True
    return False


def evaluate_iter(expression_iter):
    # takes an ITERATOR for each item (#, operator, paren) in an expression
    # evaluates it in left-to-right order
    # call this fn (using the same iterator!!) to evaluate things in parens
    # before adding/multiplying in the main left-to-right expression
    # always returns an int!!!!!!

    total = None

    while True:
        try:
            next_item = next(expression_iter)
        except StopIteration:
            # print('stop')
            break

        # print(next_item)

        if next_item == ')':
            # end of parens, break out of while loop to return total
            break

        # for paren at the beginning!! todo
        if next_item == '(':
            number = evaluate_iter(expression_iter)
            if total is None:
                total = number
            else:
                # if exp starts with '(', total should not have been set yet
                raise Exception('?????')

        elif is_operator(next_item):
            # these should go in pairs - operator then number
            next_next_item = next(expression_iter)
            if next_next_item == '(':
                # solve inside parentheses to get the number
                number = evaluate_iter(expression_iter)
            elif next_next_item.isdigit():
                number = int(next_next_item)
            else:
                raise Exception('invalid stuff after operator')

            if next_item == '+':
                total += number
            elif next_item == '*':
                total *= number

        elif next_item.isdigit():
            # just a number with no operator beforehand means it's the first #
            total = int(next_item)

    # print('returning total', total)
    return total

assert evaluate(test_lines[0]) == 71
# assert evaluate(test_lines[1]) == 71
assert evaluate(test_lines[2]) == 51
assert evaluate(test_lines[3]) == 26
assert evaluate(test_lines[4]) == 437
assert evaluate(test_lines[5]) == 12240
assert evaluate(test_lines[6]) == 13632

homework_results = [evaluate(l) for l in lines]
print(sum(homework_results))
