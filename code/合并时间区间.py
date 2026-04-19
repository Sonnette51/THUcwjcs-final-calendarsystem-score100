def merge(intervals):
	intervals.sort()
	merged = []
	for s, e in intervals:
		if not merged or s > merged[-1][1]:
			merged.append([s, e])
		else:
			merged[-1][1] = max(merged[-1][1], e)
	return merged

n = int(input().strip())

intervals = []
for i in range(n):
    s, e = map(int, input().split())
    intervals.append((s, e))
res = merge(intervals)
for s, e in res:
	print(s, e)
