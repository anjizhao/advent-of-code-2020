import re


with open('input.txt', 'r') as f:
    input_text = f.read()

passports = input_text.strip().split('\n\n')
passports = [p.replace('\n', ' ') for p in passports]


passports_parsed = []

for p_str in passports:
    parsed = {}
    fields = p_str.split(' ')
    for f in fields:
        key, val = f.split(':')
        parsed[key] = val
    passports_parsed.append(parsed)

REQUIRED_FIELDS = {'byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid'}

passports_with_all_fields = [p for p in passports_parsed if REQUIRED_FIELDS.issubset(p.keys())]
print(len(passports_with_all_fields))


def hgt_valid(x):
    if 'cm' in x:
        split_list = x.split('cm')
        if len(split_list) == 2 and split_list[0].isdigit():
            hgt = int(split_list[0])
            if hgt >= 150 and hgt <= 193:
                return True
    elif 'in' in x:
        split_list = x.split('in')
        if len(split_list) == 2 and split_list[0].isdigit():
            hgt = int(split_list[0])
            if hgt >= 59 and hgt <= 76:
                return True
    return False

assert not hgt_valid('10cm')
assert hgt_valid('155cm')
assert not hgt_valid('6sdfsdf0in')
assert not hgt_valid('60incmcm cm cm')

RULES = {
    'byr': lambda x: x.isdigit() and int(x) >= 1920 and int(x) <= 2002,
    'iyr': lambda x: x.isdigit() and int(x) >= 2010 and int(x) <= 2020,
    'eyr': lambda x: x.isdigit() and int(x) >= 2020 and int(x) <= 2030,
    'hgt': hgt_valid,
    'hcl': lambda x: len(x) == 7 and x[0] == '#' and re.match('[0-9a-f]{6}', x[1:]),
    'ecl': lambda x: x in {'amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth'},
    'pid': lambda x: len(x) == 9 and x.isdigit(),
    'cid': lambda x: True,
}

def check_passport_valid(p):  # p is a dict
    for k, v in p.items():
        valid = RULES[k](v)
        if not valid:
            return False
    return True

valid_passports = []

for p in passports_with_all_fields:
    if check_passport_valid(p):
        valid_passports.append(p)

print(len(valid_passports))


