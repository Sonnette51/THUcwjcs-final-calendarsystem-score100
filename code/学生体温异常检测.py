n = int(input())
days = []
for i in range(n):
    parts = input().split()
    m = int(parts[0])
    day = {}
    idx = 1
    for j in range(m):
        name = parts[idx]; temp = float(parts[idx+1]); idx += 2
        if name not in day or temp > day[name]:
            day[name] = temp
    days.append(day)

consec = set()
for i in range(n - 1):
    consec |= set(days[i].keys()) & set(days[i + 1].keys())

records = []
for day in days:
    for name, temp in day.items():
        records.append((name, temp))

max_temp = {}
for name, temp in records:
    if name not in max_temp or temp > max_temp[name]:
        max_temp[name] = temp

names = sorted(consec)
print(' '.join(names))
max_temp = max(max_temp[name] for name in names)
print(f"{max_temp:.1f}")