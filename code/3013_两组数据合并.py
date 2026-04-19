M,N=map(int,input().split())
a=list(map(int,input().split()))
b=list(map(int,input().split()))

i = j = 0
res = []
while i < M and j < N:
    if a[i] < b[j]:
        if not res or res[-1]!= a[i]:
            res.append(a[i])
        i += 1
    elif a[i] > b[j]:
        if not res or res[-1]!= b[j]:
            res.append(b[j])
        j += 1
    else:
        if not res or res[-1]!= a[i]:
            res.append(a[i])
        i += 1
        j += 1

while i < M:
    if not res or res[-1]!= a[i]:
        res.append(a[i])
    i += 1

while j < N:
    if not res or res[-1]!= b[j]:
        res.append(b[j])
    j += 1

print(' '.join(map(str, res)))