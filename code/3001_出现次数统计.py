N = int(input())
a = [int(input()) for i in range(N)]

ans = a[0]
max_count = 1
cur_count = 1
for i in range(1, N):
    if a[i] == a[i-1]:
        cur_count += 1
    else:
        if cur_count > max_count:
            max_count = cur_count
            ans = a[i-1]
        cur_count = 1
if cur_count > max_count:
    ans = a[-1]
print(ans)
