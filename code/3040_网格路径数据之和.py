def trans(a):
    x=8-int(a[0])
    y=int(a[1])-1
    return [x,y]

grid = [
    [2,4,6,8,9,7,5,3],
    [3,4,6,7,8,4,3,2],
    [5,8,4,9,0,4,3,2],
    [4,3,2,1,6,7,8,9],
    [4,5,6,7,8,9,0,7],
    [2,3,4,6,7,8,9,6],
    [1,2,3,4,5,6,7,8],
    [0,9,8,7,6,5,4,3],
]

n = int(input())
route = []
sum = 0
for i in range(n):
    r=input().split()
    transr=trans(r)
    route.append(transr)
if len(route)==1:
    print(grid[route[0][0]][route[0][1]])
    exit()
for j in range(len(route)-1):
    if route[j][0]==route[j+1][0]:
        for c in grid[route[j][0]][min(route[j][1],route[j+1][1]):max(route[j][1],route[j+1][1])+1]:
            sum+=c
    elif route[j][1]==route[j+1][1]:
        for r in range(min(route[j][0],route[j+1][0]),max(route[j][0],route[j+1][0])+1):
            sum+=grid[r][route[j][1]]
for r in range(1,len(route)-1):
    sum-=grid[route[r][0]][route[r][1]]
print(sum)




