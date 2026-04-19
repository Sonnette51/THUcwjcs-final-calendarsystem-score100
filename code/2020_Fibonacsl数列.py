data=input().split()
F1, F2, a, b, n = map(int, data)

if n == 1:
	print(F1)
elif n == 2:
	print(F2)
else:
    f_prev2 = F1
    f_prev1 = F2
	
    for i in range(3, n+1):
        fn = a * f_prev2 + b * f_prev1
        f_prev2, f_prev1 = f_prev1, fn
	
    print(fn)