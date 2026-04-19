moves = [(2,1),(1,2),(-1,2),(-2,1),(-2,-1),(-1,-2),(1,-2),(2,-1)]

def dfs(n, x, y, tx, ty, depth, visited):
    """在剩余深度为depth的情况下，从(x,y)递归尝试到(tx,ty)。
    visited 为当前路径上的节点集合，进入前 add，返回后 remove
    """
    if depth == 0:
        return (x, y) == (tx, ty)

    for dx, dy in moves:
        nx, ny = x + dx, y + dy
        if 1 <= nx <= n and 1 <= ny <= n and (nx, ny) not in visited:
            if (nx, ny) == (tx, ty):
                return True
            visited.add((nx, ny))
            if dfs(n, nx, ny, tx, ty, depth-1, visited):
                return True
            visited.remove((nx, ny))
    return False


def min_knight_moves_recursive(n, start, end):
    sx, sy = start
    tx, ty = end
    if (sx, sy) == (tx, ty):
        return 0

    max_limit = n * n

    for depth_limit in range(1, max_limit + 1):
        visited = set()
        visited.add((sx, sy))
        if dfs(n, sx, sy, tx, ty, depth_limit, visited):
            return depth_limit
    return -1

n = int(input())
sx,sy = map(int, input().split())
tx,ty = map(int, input().split())

res = min_knight_moves_recursive(n, (sx, sy), (tx, ty))
print(res)

