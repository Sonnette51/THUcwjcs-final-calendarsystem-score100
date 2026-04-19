x = int(input())

def alpha(n):
    if n < 10:
        return n
    outcome = 1
    for d in str(n):
        if d != '0':
            outcome *= int(d)
    return alpha(outcome)

print(alpha(x))
