
with open('input.txt', 'r') as f:
    input_text = f.read()

test_input_1 = '0: 4 1 5\n1: 2 3 | 3 2\n2: 4 4 | 5 5\n3: 4 5 | 5 4\n4: "a"\n5: "b"\n\nababbb\nbababa\nabbbab\naaabbb\naaaabbb'  # noqa
test_input_2 = '0: 1 2\n1: "a"\n2: 1 3 | 3 1\n3: "b"\n4: 1\n5: 1 | 3\n6: 1 3\n\naba\n'  # noqa

def read_input(input_text):
    rules_str, messages_str = input_text.strip().split('\n\n')
    rules_list = rules_str.split('\n')
    messages_list = messages_str.split('\n')
    return rules_list, messages_list

rules_list, messages_list = read_input(input_text)
test_rules_list_1, test_messages_list_1 = read_input(test_input_1)
test_rules_list_2, test_messages_list_2 = read_input(test_input_2)

print(rules_list[:2])
print(messages_list[:2])


def parse_rules(rules_list):
    rules_dict = {}
    for r in rules_list:
        number_str, rule_str = r.split(': ')
        number = int(number_str)

        if '"' in rule_str:  # single characters
            letter = rule_str.strip('"')
            rules_dict[number] = [letter]

        else:  # |-separated list of rules
            sub_rules = rule_str.split(' | ')
            sub_rules = [[int(i) for i in sr.split(' ')] for sr in sub_rules]
            rules_dict[number] = sub_rules

    return rules_dict

rules = parse_rules(rules_list)
test_rules_1 = parse_rules(test_rules_list_1)
test_rules_2 = parse_rules(test_rules_list_2)
# print(rules)


def substr_matches_rule_number(rules_dict, rule_number, string):
    # return the part of the string that matches the rule

    # print('substring matches rule? rule number', rule_number)
    rule = rules_dict[rule_number]

    if len(rule) == 1 and isinstance(rule[0], str):
        # "base" case where rule is just one character
        if string[0] == rule[0]:
            return string[0]

    # otherwise we have a list of rule options
    else:

        matches = []
        for rule_option in rule:
            # print('rule option', rule_option)
            match = matches_multipart_rule(rules_dict, rule_option, string)
            # print('match?', match)
            if match:
                return match

        return False


def matches_multipart_rule(rules_dict, rule_option, string, full_match=False):
    # if full_match==True, the whole string must match all of the rule;
    # there can't be extra unmatched characters in the message.

    # print('matches multipart rule?', rule_option)
    if isinstance(rule_option, str):
        return rule_option == string

    matched_string = ''
    remaining_string = string

    for rule_number in rule_option:
        # print('checking rule_number', rule_number, 'in option', rule_option)
        if len(remaining_string) == 0:
            # if we've exhausted the whole string but there are still
            # unmatched rules left, it's not a match
            # print('no match')
            return False
        match = substr_matches_rule_number(
            rules_dict, rule_number, remaining_string)
        if match:
            remaining_string = remaining_string.replace(match, '', 1)
            matched_string = matched_string + match
            # print('found match', match, 'matched string', matched_string, 'remaining string', remaining_string)  # noqa
        else:
            # print('no match')
            return False

    # print('final strings', remaining_string, matched_string)

    if full_match and len(remaining_string) == 0:
        return matched_string

    elif not full_match and matched_string:
        return matched_string

    return False


def matches_rule(rules_dict, rule_number, string):
    rule = rules_dict[rule_number]

    return any([
        matches_multipart_rule(
            rules_dict, rule_option, string, full_match=True)
        for rule_option in rule
    ])


# tests

assert matches_rule(test_rules_2, 1, 'a')
assert not matches_rule(test_rules_2, 1, 'aa')
assert not matches_rule(test_rules_2, 1, 'b')

assert matches_rule(test_rules_2, 5, 'a')
assert matches_rule(test_rules_2, 5, 'b')
assert matches_rule(test_rules_2, 6, 'ab')

assert matches_rule(test_rules_2, 2, 'ab')
assert matches_rule(test_rules_2, 2, 'ba')

assert matches_rule(test_rules_2, 0, 'aab')
assert matches_rule(test_rules_2, 0, 'aba')

assert matches_rule(test_rules_1, 0, 'aaaabb')
assert matches_rule(test_rules_1, 0, 'abbabb')
assert matches_rule(test_rules_1, 0, 'abbbab')
assert not matches_rule(test_rules_1, 0, 'abbbbb')
assert not matches_rule(test_rules_1, 0, 'abbbaa')
assert matches_rule(test_rules_1, 0, 'aaaabb')
assert not matches_rule(test_rules_1, 0, 'aaaabbb')


def count_matching_messages(rules, messages, rule_number=0):
    matches_rules = [matches_rule(rules, rule_number, m) for m in messages]
    # print(matches_rules)
    return sum(matches_rules)


assert count_matching_messages(test_rules_1, test_messages_list_1) == 2


result = count_matching_messages(rules, messages_list)
print(result)
