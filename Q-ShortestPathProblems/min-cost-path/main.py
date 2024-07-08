import heapq


def min_cost(grid, start, end):
    h, w = len(grid), len(grid[0])
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    pq = [(grid[start[0]][start[1]], start[0], start[1])]
    costs = [[float('inf')] * w for _ in range(h)]
    costs[start[0]][start[1]] = grid[start[0]][start[1]]
    
    while pq:
        cost, x, y = heapq.heappop(pq)
        if (x, y) == end:
            return cost
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < h and 0 <= ny < w:
                new_cost = cost + grid[nx][ny]
                if new_cost < costs[nx][ny]:
                    costs[nx][ny] = new_cost
                    heapq.heappush(pq, (new_cost, nx, ny))


# 入力例
h, w = map(int, input().split())
grid = [list(map(int, input().split())) for _ in range(h)]
start, end = (0, 0), (h-1, w-1)

# 17秒ここでテスト用にストップする
import time
time.sleep(3)


# 最小コストを計算
print(min_cost(grid, start, end))
