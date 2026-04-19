def execute_instructions(instrs, functions, pos):
    x, y = pos
    for token in instrs:
        if token == 'U':
            y += 1
        elif token == 'D':
            y -= 1
        elif token == 'L':
            x -= 1
        elif token == 'R':
            x += 1
        elif token == 'CALL':
            pass
        else:
            if token in functions:
                fx = functions[token]
                x, y = execute_instructions(fx, functions, [x, y])
    return x, y

F = int(input())
functions = {}
for i in range(F):
    parts = input().split()
    name = parts[1]
    raw = parts[2:]
    parsed = []
    i = 0
    while i < len(raw):
        if raw[i] == 'CALL' and i + 1 < len(raw):
            parsed.append(raw[i+1])
            i += 2
        else:
            parsed.append(raw[i])
            i += 1
        functions[name] = parsed


M = int(input().strip())
main_parts = input().split()
main_instrs = []
i = 0
while i < len(main_parts):
    if main_parts[i] == 'CALL' and i + 1 < len(main_parts):
        main_instrs.append(main_parts[i+1])
        i += 2
    else:
        main_instrs.append(main_parts[i])
        i += 1

x, y = 0, 0
x, y = execute_instructions(main_instrs, functions, [x, y])

print(f"({x}, {y})")

