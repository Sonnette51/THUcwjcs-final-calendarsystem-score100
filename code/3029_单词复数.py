def RegularPlural(word):
    if word.endswith('y') and word[-2] not in 'aeiou':
        return word[:-1] + 'ies'
    elif word.endswith(('s', 'sh', 'ch', 'x', 'z')):
        return word + 'es'
    else:
        return word + 's'
s=input()
print(RegularPlural(s))