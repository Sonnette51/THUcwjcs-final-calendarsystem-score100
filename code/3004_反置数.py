def InverNum(num):
        num2=num[::-1]
        return int(num2)
a,b=map(str,input().split())
a2=InverNum(a)
b2=InverNum(b)
add=a2+b2
print(InverNum(str(add)))
