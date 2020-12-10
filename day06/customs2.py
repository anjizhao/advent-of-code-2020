from collections import Counter

with open('input.txt', 'r') as f:
    text = f.read()

groups = text.strip().split('\n\n')

people_in_group = [g.split('\n') for g in groups]

answers_dict = {ix: a for ix, a in enumerate(people_in_group)}

# print(people_in_group[:2])
# print(answers_dict[0])
# print(answers_dict[1])

letters_per_group = {}

for k, v in answers_dict.items():
    members = len(v)
    c_group = Counter()
    for i in v:  # each i is a string of one person's answers
        c_person = Counter(set(i))  # dedupe per person just in case
        c_group += c_person
    common_answers = []  # letters that were answered by every person in the group
    for letter, count in c_group.items():
        if count == members:
            common_answers.append(letter)
    letters_per_group[k] = common_answers

counts = [len(v) for k, v in letters_per_group.items()]

print(sum(counts))

