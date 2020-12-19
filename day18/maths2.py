
from collections import deque

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
    # print('original:', raw_str)
    padded = '({})'.format(raw_str)
    exp_str = padded.replace('(', '( ').replace(')', ' )')  # add spaces lol
    assert len(exp_str) % 2 == 1  # should have odd # of characters
    exp_list = exp_str.split(' ')
    exp_dq = deque(exp_list)
    return evaluate_deque(exp_dq)


def is_operator(c):
    if c in ['+', '*']:
        return True
    return False


def evaluate_deque(expression_deque, group_type='('):
    # group type could be '(' or '*'
    # takes a python deque of each item (#, operator, paren) in an expression
    # evaluates it in left-to-right order
    # call this fn (using the same deque!!) to evaluate things in parens
    # before adding/multiplying in the main left-to-right expression
    # always returns an int!!!!!!

    # print('group type', group_type)

    total = None

    while True:
        try:
            next_item = expression_deque.popleft()
        except IndexError:
            break

        if group_type == '(' and next_item == ')':
            # end of parens, break out of while loop to return total
            break

        if group_type == '*' and next_item in ['*', ')']:
            # end of our fake multiply parens, break out of while loop
            # BUT we need to unpop the * or ) back on for the next operation
            expression_deque.appendleft(next_item)
            break

        # for paren at the beginning!!
        if next_item == '(':
            number = evaluate_deque(expression_deque)
            if total is None:
                total = number
            else:
                # if exp starts with '(', total should not have been set yet
                raise Exception('?????')

        elif is_operator(next_item):

            if next_item == '*':
                # since * has the lowest precedence, we can pretend
                # everything AFTER the * (until the next *) is in parentheses
                number = evaluate_deque(expression_deque, group_type='*')

            else:
                # these should go in pairs - operator then number
                next_next_item = expression_deque.popleft()
                if next_next_item == '(':
                    # solve inside parentheses to get the number
                    number = evaluate_deque(expression_deque)
                elif next_next_item.isdigit():
                    number = int(next_next_item)
                else:
                    raise Exception('invalid stuff after operator')

            if next_item == '+':
                total += number
                # print('adding', number, 'new total', total)
            elif next_item == '*':
                total *= number
                # print('multiplying', number, 'new total', total)

        elif next_item.isdigit():
            # just a number with no operator beforehand means it's the first #
            total = int(next_item)

    # print('returning total', total)
    return total

# assert evaluate(test_lines[0]) == 231
# assert evaluate(test_lines[1]) == 231
# assert evaluate(test_lines[2]) == 51
# assert evaluate(test_lines[3]) == 46
# assert evaluate(test_lines[4]) == 1445
# assert evaluate(test_lines[5]) == 669060
# assert evaluate(test_lines[6]) == 23340

homework_results = [evaluate(l) for l in lines]
print(sum(homework_results))
