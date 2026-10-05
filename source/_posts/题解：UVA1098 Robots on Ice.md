---
abbrlink: UVA1098 题解
categories:
- - 题解
date: '2026-10-05T19:58:10.008099+08:00'
description: null
mathjax: true
tags:
- 题解
title: 题解：UVA1098 Robots on Ice
updated: '2026-10-05T19:58:10.725+08:00'
---
# 题解：UVA1098 Robots on Ice

## 思路

机器人从 $(0, 0)$ 出发，必须走遍所有格子各一次，最终停在 $(0, 1)$，并且在三个指定步数（总步数的 $\frac{1}{4}$、$\frac{1}{2}$、$\frac{3}{4}$ 向下取整）必须到达三个指定的检查点。

考虑采用深度优先搜索来枚举所有可能路径，并通过剪枝减少搜索空间。

首先读入网格大小和三个检查点坐标，计算总步数，并确定三个检查点对应的步数。然后进行检查：

- 检查点时间必须严格递增；
- 检查点不能重复；
- 如果起点或终点被指定为检查点；
- 其时间必须符合要求（起点时间为 $1$，终点时间为总步数）。

初始化 $vis$ 数组，在网格周围设置围墙（边界外格子标记为已访问），并标记起点已访问。从起点开始搜索，每一步尝试向四个方向移动。对于每个可能的下一步，通过 $check$ 函数进行检查：

- 不能走到已访问的格子；
- 如果下一步是终点，则必须是在总步数时到达；
- 对于每个检查点，如果该检查点还未被访问，且下一步正好是该检查点，则当前步数加一必须等于该检查点规定的时间，否则剪枝；
- 如果当前步数加一已经超过某个未访问检查点的时间，也剪枝。
- **还有一个剪枝条件涉及相邻格子的访问状态，用于避免走入死胡同**，例如这样：
  ![](https://cdn.luogu.com.cn/upload/image_hosting/zud7ev4j.png)

  像这样，当走到蓝色格子这个地方的时候，可以剪枝，因为这样进入死胡同的话无论怎么走都出不来了。

当搜索到达终点且步数等于总步数时，说明找到一条合法路径，答案计数加一。搜索完成后输出答案。

## 代码

```cpp
#include <bits/stdc++.h>
#define endl '\n'
using namespace std;

int T, n, m, ans;
bool vis[10][10];
struct STRUCT
{
    int x, y, t;
} p[3];
int fx[4] = {1, -1, 0, 0};
int fy[4] = {0, 0, -1, 1};

bool check(int x, int y, int d, int s)
{
    if (vis[x][y])
        return false;
    if (x == 1 && y == 2 && s != n * m)
        return false;
    for (int i = 0; i < 3; i++)
    {
        if (vis[p[i].x][p[i].y])
            continue;
        if (p[i].x == x && p[i].y == y && s != p[i].t)
            return false;
        if (s > p[i].t)
            return false;
    }
    if (vis[x + fx[d]][y + fy[d]] &&
        !vis[x + fy[d]][y - fx[d]] &&
        !vis[x - fy[d]][y + fx[d]])
        return false;
    return true;
}

void dfs(int stp, int x, int y)
{
    if (x == 1 && y == 2)
    {
        if (stp == n * m)
            ans++;
        return;
    }
    for (int i = 0; i < 4; i++)
    {
        int nx = x + fx[i];
        int ny = y + fy[i];
        if (nx >= 1 && nx <= n && ny >= 1 && ny <= m && check(nx, ny, i, stp + 1))
        {
            vis[nx][ny] = true;
            dfs(stp + 1, nx, ny);
            vis[nx][ny] = false;
        }
    }
}

int mian()
{
    cin >> n >> m;
    for (int i = 0; i < 3; i++)
    {
        cin >> p[i].x >> p[i].y;
        p[i].x++;
        p[i].y++;
    }
    int total = n * m;
    p[0].t = total / 4;
    p[1].t = total / 2;
    p[2].t = total * 3 / 4;
    if (p[0].t >= p[1].t || p[1].t >= p[2].t)
    {
        return cout << 0 << endl, 0;
    }
    for (int i = 0; i < 3; i++)
    {
        for (int j = i + 1; j < 3; j++)
        {
            if (p[i].x == p[j].x && p[i].y == p[j].y)
                return cout << 0 << endl, 0;
        }
    }
    int sx = 1, sy = 1;
    int ex = 1, ey = 2;
    for (int i = 0; i < 3; i++)
    {
        if (p[i].x == sx && p[i].y == sy && p[i].t != 1)
            return cout << 0 << endl, 0;
        if (p[i].t == 1 && (p[i].x != sx || p[i].y != sy))
            return cout << 0 << endl, 0;
        if (p[i].x == ex && p[i].y == ey && p[i].t != total)
            return cout << 0 << endl, 0;
        if (p[i].t == total && (p[i].x != ex || p[i].y != ey))
            return cout << 0 << endl, 0;
    }
    memset(vis, 0, sizeof(vis));
    for (int i = 0; i <= n + 1; i++)
        vis[i][0] = vis[i][m + 1] = true;
    for (int j = 0; j <= m + 1; j++)
        vis[0][j] = vis[n + 1][j] = true;
    vis[sx][sy] = true;
    ans = 0;
    dfs(1, sx, sy);
    return ans;
}

int main()
{
    cin >> T;
    for (int _ = 1; _ <= T; _++)
        cout << "Case " << _ << ": " << mian() << endl;
    return 0;
}
```

## 后记

集训的时候这道题给同学干崩溃了（原题时间限制 9s，校内 OJ 上题面写的 3s，结果数据只有 1s 的限制），原题也没找到，后来用原题机才找到的。
