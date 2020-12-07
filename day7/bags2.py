

with open('input.txt', 'r') as f: 
    lines = f.readlines()

lines = [l.strip() for l in lines]

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

# how many bags inside one shiny gold bag?


def count_bags_inside(outer_color):
    total_count = 0
    contents_list = rules[outer_color]
    # for each inner bag color, get total count of all bags inside that color bag
    # then add 1 for the inner bag itself
    # then multiply by number of that color bag that go in the outer color bag
    # then add to the total count
    # return total count after all inner bags are counted
    for content in contents_list:
        color = content['color']
        count = content['count']
        per_bag_inside_count = count_bags_inside(color)
        total_for_color = (per_bag_inside_count + 1) * count
        total_count += total_for_color
    return total_count


# test_colors = ['dim salmon', 'light aqua', 'dim maroon']
# 
# for c in test_colors: 
#     print('test {}: {} bags inside'.format(c, count_bags_inside(c)))

print(count_bags_inside('shiny gold'))




