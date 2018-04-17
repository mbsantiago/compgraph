import math
import re

SPECIAL_CHARACTERS = [
    '/',
    '+',
    '%',
    '[',
    ']',
    ':',
    ',',
    '(',
    ')'
]

CHARACTERS_REGEX = '[{}]'.format(
    ''.join(SPECIAL_CHARACTERS)
    .replace('[', r'\[')
    .replace(']', r'\]'))

IMPLEMENTED_OPERATIONS = {
    'floor': math.floor,
    'ceil': math.ceil,
}

def parse_variables(string):
    regex = r'(?<=\$)\w+(?={})'.format(CHARACTERS_REGEX)
    matches = re.findall(regex, string)
    return matches

def parse_operations(string):
    pass

matches = parse_names('$variable1+$variable2/$variable5[2:10]')
