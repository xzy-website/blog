---
abbrlink: CF2187E 题解
categories:
- - 题解
date: '2026-10-05T20:14:46.550940+08:00'
description: null
mathjax: true
tags:
- 题解
title: 题解：CF2187E Doors and Keys
updated: '2026-10-05T20:14:47.326+08:00'
---
# 题解：CF2187E Doors and Keys

## 思路

### 题意转换

题意中你只能携带一把钥匙，但允许放下、再回来捡。

我们注意到，如果你需要用到后面某房间的钥匙，你会不断地在相邻房间之间来回搬运钥匙，把多把钥匙逐步向前移动。

这个过程等价为你可以同时携带任意把钥匙，但从房间 $i$ 移动到房间 $i+1$ 的代价变为 $\operatorname{cost}(k) = \max(1, 2\times k-1)$，其中 $k$ 是你当前持有的钥匙数量。

- 当 $k=0$ 时，直接走过去，耗时 $1$。
- 当 $k\ge 1$ 时，你需要来回搬运 $k$ 把钥匙，每扇门的净前进时间为 $2 \times k-1$。

最后到达终点时不应留有钥匙，否则不如当初不捡。

### 状态转移

设 $dp_{i, j}$ 表示到达房间 $i$，身上带着 $j$ 把钥匙时的最小时间。

1. 捡钥匙
   若第 $i$ 个房间有初始钥匙（$s_i=1$），你可以捡起它：$dp_{i, j+1} \leftarrow \min(dp_{i, j+1}, dp_{i, j})$（从大到小更新以避免重复捡起）。
2. 走向下一房间

   - 等门自动开（不消耗钥匙）：
     需要等到第 $a_i$ 秒门才开，因此通过时间为 $\max(dp_{i, j}, a_i) + \operatorname{cost}(j)$。
     $dp_{i+1, j} \leftarrow \min(dp_{i+1, j}, \max(dp_{i, j}, a_i) + \operatorname{cost}(j))$
   - 用钥匙开门（消耗一把钥匙，若 $j\ge 1$）：
     不需要等 $a_i$，直接通过，时间 $dp_{i, j} + \operatorname{cost}(j)$，且钥匙数减 $1$。
     $dp_{i+1, j-1} \leftarrow \min(dp_{i+1, j-1}, dp_{i, j} + \operatorname{cost}(j))$

到达房间 $i+1$ 的答案即为 $dp_{i+1, 0}$（无多余钥匙）。

### 第二维开多大

若携带 $j$ 把钥匙并全部用来开门，仅搬运这些钥匙的累计时间至少为 $\sum_{x=1}^{j}(2 \times x-1) = j^2$。

答案不会超过 $n + \max a_i \le 4\times 10^5$，因此 $j$ 只需保留到 $O(\sqrt{\max a_i})$ 级别，约 $450 \sim 500$ 即可。

那么最后考虑用滚动数组 $f_{0/1, M}$ 进行 DP，输出每步 $f_{\text{nxt}, 0}$ 即可。

## 代码

[https://codeforces.com/contest/2187/submission/374076276](https://codeforces.com/contest/2187/submission/374076276)。

```cpp
#include <bits/stdc++.h>
#define endl '\n'
using namespace std;

const int N = 200005;
const int M = 500;
const int INF = 1e9;
int T, n, a[N];
string s;
int f[2][M];

void mian()
{
    cin >> n;
    for (int i = 1; i <= n; i++)
        cin >> a[i];
    cin >> s;
    s = " " + s;
    for (int i = 0; i < M; i++)
        f[0][i] = f[1][i] = INF;
    int now = 0;
    f[now][0] = 0;
    for (int i = 1; i <= n; i++)
    {
        if (s[i] == '1')
        {
            for (int j = M - 1; j >= 0; j--)
            {
                if (f[now][j] != INF && j + 1 < M)
                    if (f[now][j + 1] > f[now][j])
                        f[now][j + 1] = f[now][j];
            }
        }
        int nxt = now ^ 1;
        for (int j = 0; j < M; j++)
            f[nxt][j] = INF;
        for (int j = 0; j < M; j++)
        {
            if (f[now][j] == INF)
                continue;
            int cost = max(1, 2 * j - 1);
            int v = max(f[now][j], a[i]) + cost;
            if (v < f[nxt][j])
                f[nxt][j] = v;
            if (j > 0)
            {
                v = f[now][j] + cost;
                if (v < f[nxt][j - 1])
                    f[nxt][j - 1] = v;
            }
        }
        cout << f[nxt][0] << " ";
        now = nxt;
    }
    cout << endl;
}

int main()
{
    ios::sync_with_stdio(0);
    cin.tie(0), cout.tie(0);
    cin >> T;
    while (T--)
        mian();
    return 0;
}
```
