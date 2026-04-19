def birthnum(num):
    total = sum(int(d) for d in str(num))
    if total > 9:
        return birthnum(total)
    return total

s = input()
digits = ''.join(ch for ch in s if ch.isdigit())
print(birthnum(digits))