def ways(n, memo):
	if n == 0:
		return 1
	if n < 0:
		return 0
	if n in memo:
		return memo[n]
	memo[n] = ways(n-1, memo) + ways(n-2, memo) + ways(n-3, memo)
	return memo[n]

N = int(input())
result = ways(N, {})
print(result)

