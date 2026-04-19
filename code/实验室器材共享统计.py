n = int(input())
groups = []

for i in range(n):
    items = input().split()
    groups.append(set(items))

common_items = set(groups[0]) 
for group in groups[1:]:
    common_items &= group

all_items = {}
for group in groups:
    for item in group:
        if item in all_items:
            all_items[item] += 1
        else:
            all_items[item] = 1

unique_items = set()
for item, count in all_items.items():
    if count == 1:
        unique_items.add(item)


if common_items:
    print(' '.join(sorted(common_items)))
else:
    print("None")

if unique_items:
    print(' '.join(sorted(unique_items)))
else:
    print("None")
