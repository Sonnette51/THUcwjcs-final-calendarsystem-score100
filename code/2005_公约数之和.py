import math
x,y=map(int,input().split())
gcdxy=math.gcd(x,y)
sum=0
for i in range(1,gcdxy+1):
    if x%i==0 and y%i==0:
        sum+=i
print(sum)
