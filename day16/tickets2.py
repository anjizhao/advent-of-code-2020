from collections import defaultdict

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


def get_valid_tickets(tickets, rules):
    all_ranges = []
    for r in rules.values():
        all_ranges.extend(r)
    valid_tickets = []
    for t in tickets:
        if all([any([value in r for r in all_ranges]) for value in t]):
            valid_tickets.append(t)
    return valid_tickets


valid_tickets = get_valid_tickets(nearby_tickets, rules_dict)
# print(valid_tickets)

# for each position on the tickets, compare values with the rules
# compile all possible fields each index could be
possible_fields_per_index = defaultdict(list)
for index in range(len(my_ticket)):
    values = [t[index] for t in valid_tickets]
    for field, ranges in rules_dict.items():
        if all([any([value in r for r in ranges]) for value in values]):
            possible_fields_per_index[index].append(field)

# print(possible_fields_per_index)

# now find the actual fields per index by first assigning to indices which
# only have one possible field; then, for indices w/ multiple possible fields,
# choose out of the remaining field options until all fields are assigned
min_length = 1
available_fields = set(rules_dict.keys())
field_per_index = {}
while len(available_fields) > 0:
    for index, fields in possible_fields_per_index.items():
        if len(fields) > min_length:
            continue
        for field in fields:
            if field in available_fields:
                field_per_index[index] = field
                available_fields.remove(field)
                break
    min_length += 1

print(field_per_index)

# now read my ticket
my_ticket_parsed = {}
for i, v in enumerate(my_ticket):
    my_ticket_parsed[field_per_index[i]] = v

print(my_ticket_parsed)

values = [v for k, v in my_ticket_parsed.items() if k[:9] == 'departure']
print(values)
