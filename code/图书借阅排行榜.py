n = int(input())
totals = {}
for i in range(n):
    line = input().strip()
    parts = line.split()
    category = parts[0]
    duration = int(parts[1])
    if category in totals:
        totals[category] += duration
    else:
        totals[category] = duration
        
items = sorted(totals.items(), key=lambda x: (-x[1], x[0]))
for category, total in items[:3]:
    print(category, total)
