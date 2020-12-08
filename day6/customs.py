
with open('input.txt', 'r') as f:
    text = f.read()

groups = text.split('\n\n')

people_in_group = [g.split('\n') for g in groups]

answers_dict = {ix: a for ix, a in enumerate(people_in_group)}

# print(people_in_group[:2])
# print(answers_dict[0])
# print(answers_dict[1])

letters_per_group = {}

for k, v in answers_dict.items():
    s = set()
    for i in v:  # each i is a string of one person's answers
        for c in i:
            s.add(c)
    letters_per_group[k] = s  # store set of group's unique answers as value for group's index

counts = [len(v) for k, v in letters_per_group.items()]

print(sum(counts))


