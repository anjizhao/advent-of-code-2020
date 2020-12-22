from collections import defaultdict

with open('input.txt', 'r') as f:
    input_text = f.read()

test_input = '42: 9 14 | 10 1\n9: 14 27 | 1 26\n10: 23 14 | 28 1\n1: "a"\n11: 42 31\n5: 1 14 | 15 1\n19: 14 1 | 14 14\n12: 24 14 | 19 1\n16: 15 1 | 14 14\n31: 14 17 | 1 13\n6: 14 14 | 1 14\n2: 1 24 | 14 4\n0: 8 11\n13: 14 3 | 1 12\n15: 1 | 14\n17: 14 2 | 1 7\n23: 25 1 | 22 14\n28: 16 1\n4: 1 1\n20: 14 14 | 1 15\n3: 5 14 | 16 1\n27: 1 6 | 14 18\n14: "b"\n21: 14 1 | 1 14\n25: 1 1 | 1 14\n22: 14 14\n8: 42\n26: 14 22 | 1 20\n18: 15 15\n7: 14 5 | 1 21\n24: 14 1\n\nabbbbbabbbaaaababbaabbbbabababbbabbbbbbabaaaa\nbbabbbbaabaabba\nbabbbbaabbbbbabbbbbbaabaaabaaa\naaabbbbbbaaaabaababaabababbabaaabbababababaaa\nbbbbbbbaaaabbbbaaabbabaaa\nbbbababbbbaaaaaaaabbababaaababaabab\nababaaaaaabaaab\nababaaaaabbbaba\nbaabbaaaabbaaaababbaababb\nabbbbabbbbaaaababbbbbbaaaababb\naaaaabbaabaaaaababaa\naaaabbaaaabbaaa\naaaabbaabbaaaaaaabbbabbbaaabbaabaaa\nbabaaabbbaaabaababbaabababaaab\naabbbbbaabbbaaaaaabbbbbababaaaaabbaaabba'  # noqa
# test_input_1 = '0: 4 1 5\n1: 2 3 | 3 2\n2: 4 4 | 5 5\n3: 4 5 | 5 4\n4: "a"\n5: "b"\n\nababbb\nbababa\nabbbab\naaabbb\naaaabbb'  # noqa
# test_input_2 = '0: 1 2\n1: "a"\n2: 1 3 | 3 1\n3: "b"\n4: 1\n5: 1 | 3\n6: 1 3\n\naba\n'  # noqa

def read_input(input_text):
    rules_str, messages_str = input_text.strip().split('\n\n')
    rules_str = rules_str + '\n8: 42 | 42 8\n11: 42 31 | 42 11 31'
    rules_list = rules_str.split('\n')
    messages_list = messages_str.split('\n')
    return rules_list, messages_list

rules_list, messages_list = read_input(input_text)
test_rules_list, test_messages_list = read_input(test_input)
# test_rules_list_2, test_messages_list_2 = read_input(test_input_2)

# print(rules_list[:2])
# print(messages_list[:2])
# print('messages:', len(messages_list))


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
# print(rules[8])
# print(rules[11])
test_rules = parse_rules(test_rules_list)
# test_rules_2 = parse_rules(test_rules_list_2)
# print(rules)


# replace 8: 42 and 11: 42 31 with the following:

# 8: 42 | 42 8 --> [any item in set 42] * n
# 11: 42 31 | 42 11 31  --> [any item in set 42] * n + [any item in set 31] * n


# solve for all the possible values of 42 and 31


def seed_solved_rules(rules, solved_rules):
    for number, rule_options in rules.items():
        if len(rule_options) == 1 and isinstance(rule_options[0], str):
            solved_rules[number].append(rule_options[0])


def get_possible_values(rules, solved_rules, number):
    # returns a LIST of possible STRING values for the number

    # print('getting possible values for', number, 'already solved:', solved_rules)  # noqa

    already_solved_values = solved_rules.get(number)

    if already_solved_values:
        # print('already solved for', number, already_solved_values)
        return already_solved_values

    rule_options = rules[number]
    # example [[9, 14], [10, 1]]
    # example 15: 1 | 14 -> [[1], [14]]
    # 5: 1 14 | 15 1 -> [[1, 14], [15, 1]]
    solved_options = [[get_possible_values(rules, solved_rules, o) for o in option] for option in rule_options]  # noqa

    # print('solved options', solved_options)
    # example  [ [['a'], ['b']], [['a', 'b'], ['a']] ]
    # want to return ['ab', 'aa', 'ba']
    # o1 = [['a'], ['b']]
    # o2 = [['a', 'b'], ['a']]

    final_solved = []

    for o in solved_options:
        if len(o) == 1:  # only one option
            final_solved.append(''.join(o[0]))
            continue
        for i in range(len(o[0])):  # two options - build out all combinations
            for j in range(len(o[1])):
                final_solved.append(o[0][i] + o[1][j])

    # final_solved = [''.join([''.join(i) for i in o]) for o in solved_options]
    # print('final solved', final_solved)
    solved_rules[number] = final_solved
    return final_solved



def prep_solved_rules(rules, solved_rules):
    seed_solved_rules(rules, solved_rules)
    get_possible_values(rules, solved_rules, 31)
    get_possible_values(rules, solved_rules, 42)


test_solved_rules = defaultdict(list)
prep_solved_rules(test_rules, test_solved_rules)

# # do NOT try to call on 8 or 11! will hit maximum recursion depth error
# get_possible_values(test_rules, solved_rules, 8)

# print(31, test_solved_rules[31])
# print(42, test_solved_rules[42])


solved_rules = defaultdict(list)
prep_solved_rules(rules, solved_rules)
# print(31, solved_rules[31])
# print(42, solved_rules[42])


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
            match = matches_multipart_rule(rules_dict, rule_option, string)  # noqa
            # print('match?', match)
            if match:
                return match

        return False


def matches_multipart_rule(rules_dict, rule_option, string, full_match=False):  # noqa
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


def matches_rule(rules_dict, solved_rules, rule_number, string):
    rule = rules_dict[rule_number]
    if rule_number == 0:
        # special logic for weird numbers
        # 8: 42 | 42 8 --> [any item in set 42] * n
        # 11: 42 31 | 42 11 31  --> [any item in set 42] * n + [any item in set 31] * n  # noqa

        # we know the rule is '0: 8 11' and this is the only place 8 & 11 appear  # noqa
        assert rule == [[8, 11]]
        # print('rule number', rule_number)
        # print('string', string)

        str_copy = string

        matched = ''
        str_len_42 = len(solved_rules[42][0])
        possible_strings_42 = set(solved_rules[42])
        str_len_31 = len(solved_rules[31][0])
        possible_strings_31 = set(solved_rules[31])

        count_42 = 0
        count_31 = 0

        while str_copy[:str_len_42] in possible_strings_42:
            matched = matched + str_copy[:str_len_42]
            str_copy = str_copy.replace(str_copy[:str_len_42], '', 1)
            count_42 += 1

        # print('matched 42', matched)
        count = len(matched) // str_len_42

        for i in range(count):
            # we can have more 42s than 31s bc the rule for 0 is "0: 8 11"
            # so as long as count(31s) < count(42s) AND count(31s) > 0
            # then we have a match
            if str_copy[:str_len_31] in possible_strings_31:
                if i == count - 1:  # needs at least one extra 42 substring
                    return False
                matched = matched + str_copy[:str_len_31]
                str_copy = str_copy.replace(str_copy[:str_len_31], '', 1)
                count_31 += 1
            else:  # there needs to be at least one 31 substring
                if i == 0:
                    return False

        # if len(matched) > 0 and len(str_copy) == 0:
        #     print('matched', matched, 'str_copy', str_copy, 'counts', count_42, count_31)  # noqa
        return len(matched) > 0 and len(str_copy) == 0

    return any([
        matches_multipart_rule(
            rules_dict, solved_rules, rule_option, string, full_match=True)
        for rule_option in rule
    ])


def count_matching_messages(rules, messages, rule_number=0):
    solved_rules = defaultdict(list)
    prep_solved_rules(rules, solved_rules)
    matches_rules = [matches_rule(rules, solved_rules, rule_number, m) for m in messages]  # noqa
    # print(matches_rules)
    # for i in range(len(matches_rules)):
    #     if matches_rules[i]:
    #         print(messages[i])
    return sum(matches_rules)



test_res = count_matching_messages(test_rules, ['bbabbbbaabaabba'])
assert test_res == 1

test_res = count_matching_messages(test_rules, ['aaaabbaaaabbaaa'])
assert test_res == 0

test_res_all = count_matching_messages(test_rules, test_messages_list)
# print(test_res_all)
assert test_res_all == 12

result = count_matching_messages(rules, messages_list)
print(result)


# print(test_rules)

# for i in sorted(test_rules.keys()):
#     print(i, test_rules[i])



# def a():

# 42: 9 14 | 10 1

# 31: 14 17 | 1 13
# 14: "b"
# 1: "a"


# 42: 'babbb' | 'baabb' | 'bbaab' | 'bbabb' | 'bbbab' | 'bbbbb' | 'abbbb' | 'aabbb' | 'aaaab' | 'aaabb' | 'aaaba' | 'ababa' | 'bbbba' | 'aaaaa' | 'bbaaa' | 'bbaaa'  # noqa
# 31: 'b' 17 | 'a' 13

# 9: 'babb' | 'baab' | 'bbaa' | 'bbab' | 'bbba' | 'bbbb' | 'abbb' | 'aabb' | 'aaaa' | 'aaab'  # noqa
# 27: 'abb' | 'aab' | 'baa' | 'bab' | 'bba' | 'bbb'
# 26: 'bbb' | 'abb' | 'aaa' | 'aab'
# 10: 'aaab' | 'abab' | 'bbbb' | 'aaaa' | 'bbaa' | 'bbaa'
# 20: 'bb' | 'aa' | 'ab'
# 22: 'bb'
# 15: 'a' | 'b'
# 6: 'bb' | 'ab'
# 18: 'aa' | 'ab' | 'ba' | 'bb'
# 23: 'aaa' | 'aba' | 'bbb'
# 28: 'aaa' | 'bba' | 'bba'
# 25: 'aa' | 'ab'
# 16: 'aa' | 'bb' | 'bb'
# 13: 'b' 3 | 'a' 12
# 15: 'a' | 'b'
# 17: 'b' 2 | 'a' 7
# 5: 1 14 | 15 1  -> # 5: 'ab' | 'aa' | 'ba'
