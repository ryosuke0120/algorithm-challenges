# 初めに

## 入力と出力

### 入力

通常の変数

| 項目         | 入力例      | コード                                |
| ------------ | ----------- | ------------------------------------- |
| 単一の整数   | 1           | `n = int(input())`                    |
| 単一の文字列 | abc         | `s = input()`                         |
| 2 つの整数   | 1 2         | `a, b = map(int, input().split())`    |
| 2 つの文字列 | abc def     | `s, t = input().split()`              |
| 3 つの整数   | 1 2 3       | `a, b, c = map(int, input().split())` |
| 3 つの文字列 | abc def ghi | `s, t, u = input().split()`           |

配列

| 項目               | 入力例                       | コード                                                    |
| ------------------ | ---------------------------- | --------------------------------------------------------- |
| 1 行 m 列 の整数   | 1 2 3                        | `a = list(map(int, input().split()))`                     |
| 1 行 m 列 の文字列 | abc def ghi                  | `s = input().split()`                                     |
| n 行 1 列 の整数   | 1 `\n` 2 `\n` 3              | `a = [int(input()) for _ in range(n)]`                    |
| n 行 1 列 の文字列 | abc `\n` def `\n` ghi        | `s = [input() for _ in range(n)]`                         |
| n 行 m 列の整数    | 1 2 3 `\n` 4 5 6             | `a = [list(map(int, input().split())) for _ in range(n)]` |
| n 行 m 列の文字列  | abc def ghi `\n` jkl mno pqr | `s = [input().split() for _ in range(n)]`                 |
