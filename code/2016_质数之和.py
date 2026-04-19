def is_prime(num):
    if num<2:
        return False
    for i in range(2,int(num**0.5)+1):
        if num%i==0:
            return False
    return True
n=int(input())
k=1
sum=0
while n>0:
    k+=1
    if is_prime(k):
        sum+=k
        n-=1
print(sum)




