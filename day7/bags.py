

with open('input.txt', 'r') as f:
    lines = f.readlines()

lines = [l.strip() for l in lines]

# print(lines[:2])

# construct rules dict
rules = {}

for l in lines:
    color, contents_str = l.split(' bags contain ')
    if 'no other bags' in contents_str:
        rules[color] = []
        continue
    # split str into each color bags inside
    contents_list = contents_str.replace(' bag.', '').replace(' bags.', '').replace('bag,', 'bags,').split(' bags, ')
    color_rules = []
    for c in contents_list:
        content_count, content_color = c.split(' ', maxsplit=1)
        color_rules.append({'count': int(content_count), 'color': content_color})
    rules[color] = color_rules


# # example
# rules = {
#     'muted white': [
#         {'count': 4, 'color': 'dark orange'},
#         {'count': 3, 'color': 'bright white'},
#     ],
#     'dim salmon': [],
#     ...
# }


# master set of all colors that eventually contain the shiny gold
eventually_contains_gold = set()

def check_contains_gold(outer_color):
    if outer_color in eventually_contains_gold:
        # skip repeat checks
        return True
    for content in rules[outer_color]:
        if content['color'] == 'shiny gold':
            eventually_contains_gold.add(outer_color)
            return True
    if any([check_contains_gold(content['color']) for content in rules[outer_color]]):
        eventually_contains_gold.add(outer_color)
        return True
    return False

# test_colors = ['muted white', 'bright salmon', 'drab brown', 'dark salmon']
#
# for c in test_colors:
#     print('checking {}'.format(c))
#     check_contains_gold(c)
#     print(eventually_contains_gold)
#
# print('final set:')
# print(eventually_contains_gold)


for k in rules.keys():
    check_contains_gold(k)

# print(eventually_contains_gold)
print(len(eventually_contains_gold))


