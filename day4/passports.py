
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

passport_is_valid = [REQUIRED_FIELDS.issubset(p.keys()) for p in passports_parsed]

print(sum(passport_is_valid))




