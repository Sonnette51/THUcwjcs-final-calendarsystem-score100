a2=input()
a10=0
n=len(a2)
for i in range(n):
    a10+=int(a2[n-1-i])*(2**i)
print(a10)
