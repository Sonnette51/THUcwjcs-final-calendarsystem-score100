a=input().split()
cnt=0
for i in a:
    if i==i[::-1]:
        cnt+=1
print(cnt)
