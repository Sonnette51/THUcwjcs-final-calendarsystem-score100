a=input()
cnt=1
maxcnt=1
for i in range(len(a)-1):
    if a[i]<=a[i+1]:
        cnt+=1
    else:
        if cnt>maxcnt:
            maxcnt=cnt
        cnt=1
print(maxcnt)