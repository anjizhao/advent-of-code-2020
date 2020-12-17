
with open('input.txt', 'r') as f:
    text = f.read()

test_text = 'class: 1-3 or 5-7\nrow: 6-11 or 33-44\nseat: 13-40 or 45-50\n\nyour ticket:\n7,1,14\n\nnearby tickets:\n7,3,47\n40,4,50\n55,2,20\n38,6,12'  # noqa
# text = test_text

rules_str, other_str = text.strip().split('\n\nyour ticket:\n')
my_ticket_str, nearby_tickets_str = other_str.strip().split(
    '\n\nnearby tickets:\n')


rules_list = rules_str.split('\n')
my_ticket = [int(i) for i in my_ticket_str.split(',')]
nearby_tickets = [
    [int(i) for i in s.split(',')] for s in nearby_tickets_str.split('\n')
]

def parse_rules(rules_list):
    rules_dict = {}
    for r_str in rules_list:
        key, other = r_str.split(': ')
        range_strs = other.split(' or ')
        ranges = []
        for r in range_strs:
            lower, upper = r.split('-')
            ranges.append(range(int(lower), int(upper) + 1))
        rules_dict[key] = ranges
    return rules_dict

rules_dict = parse_rules(rules_list)


def find_invalid_values(tickets, rules):
    all_ranges = []
    for r in rules.values():
        all_ranges.extend(r)
    invalid_values = []
    for t in tickets:
        for value in t:
            if any([value in r for r in all_ranges]):
                continue
            invalid_values.append(value)
    return invalid_values

invalid_values = find_invalid_values(nearby_tickets, rules_dict)
# print(invalid_values)
print(sum(invalid_values))
