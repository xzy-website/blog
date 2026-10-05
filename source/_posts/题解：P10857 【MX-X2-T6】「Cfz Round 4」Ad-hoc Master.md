---
abbrlink: P10857 题解
categories:
- - 题解
date: '2026-10-05T20:18:03.216321+08:00'
description: null
mathjax: true
tags:
- 题解
title: 题解：P10857 【MX-X2-T6】「Cfz Round 4」Ad-hoc Master
updated: '2026-10-05T20:18:04.031+08:00'
---
# 题解：P10857 【MX-X2-T6】「Cfz Round 4」Ad-hoc Master

Amazing.

## 思路

根据题意，我们有一棵层数为 $h$ 的满二叉树的“距离异或和”信息 $f_{u,k}$，其中 $f_{u,k}$ 表示与结点 $u$ 距离恰好为 $k$ 的所有结点权值的异或和。题目要求输出一组合法的根结点编号 $r$ 以及其权值 $w$。虽然给出的信息涉及全树，但由于题目只要求输出根结点和根权值，因此我们可以不必复原整棵树，而是通过异或运算的性质和满二叉树的对称性直接求解。

首先考虑满二叉树的层级结构。设树根的深度为 $1$，则深度为 $d$ 的所有结点可以编号为 $\text{layer}_d$。观察可以发现，对于任意一个结点 $u$ 和任意层 $d$，满足 $\text{dis}(u,v)=d$ 的结点 $v$ 的数量与 $u$ 的深度有规律：若 $v$ 的深度正好等于 $d+1$ 或满足对称关系，则数量为奇数；否则数量为偶数。由于异或运算在偶数次作用下结果为零，这意味着，如果将每一层的 $f_{u,k}$ 对所有 $u$ 累积异或，那么结果恰好等于深度为 $k$ 的结点权值的异或和。

记

$$
G_k = \bigoplus_{u=1}^{n} f_{u,k}, \quad 1 \le k \le 2h-2
$$

则 $G_k$ 表示深度为 $k+1$ 的所有结点权值的异或和。利用这一性质，我们可以确定根结点的位置。设结点 $r$ 为根，则其距离信息应当满足

$$
f_{r,j} = G_{j+1}, \quad 1 \le j \le h-1
$$

并且由于根结点到叶子的最大距离为 $h-1$，对 $j \ge h$ 必有 $f_{r,j} = 0$。

因此我们只需枚举每个结点 $i$，检查其距离信息是否满足上述条件，即可确定根结点编号 $r$。

确定根结点后，下一步是求根结点权值 $w$。考虑整棵树所有结点权值的异或和 $S$。选取根结点 $r$ 和任意其他结点 $i$，将它们的奇数距离信息异或起来：

$$
\bigoplus_{k=1,3,5,\dots} f_{r,k}
\oplus
\bigoplus_{k=1,3,5,\dots} f_{i,k}
$$

若 $r$ 与 $i$ 的距离为奇数，则每个结点的权值会被计算奇数次，结果正好等于 $S$；若距离为偶数，则每个结点被计算偶数次，结果为零。枚举一个结点 $i \neq r$，若得到非零结果，则其值即为整棵树权值的异或和 $S$。若所有结果均为零，则整棵树的权值异或和本身为零。

最后考虑根结点的权值。根结点的所有距离信息 $f_{r,1}, f_{r,2}, \dots, f_{r,2h-2}$ 表示整棵树除根外所有结点权值的异或和，记作 $T$：

$$
T = \bigoplus_{k=1}^{2h-2} f_{r,k}
$$

由于总异或和 $S$ 包含根结点权值 $w$ 与所有其它结点权值的异或，因此有：

$$
S = w \oplus T
\quad \Rightarrow \quad
w = S \oplus T
$$

综上，通过计算每层结点权值异或和来确定根结点，并利用奇数距离信息求整棵树权值的异或和，最后还原根结点权值，可以在不还原整棵树的情况下正确求解根节点编号和权值。该方法复杂度为 $O(nh)$，挑战最慢解！

## 代码

```cpp
#include <bits/stdc++.h>
#define endl '\n'
using namespace std;

int T, h, n, m, r, c, s, w;
int f[65540][35];
int g[35], b[65540];

void mian()
{
    cin >> h;
    n = (1 << h) - 1;
    m = 2 * h - 2;
    r = -1;
    c = s = 0;

    for (int i = 1; i <= m; i++)
        g[i] = 0;
    for (int i = 1; i <= n; i++)
    {
        for (int j = 1; j <= m; j++)
        {
            cin >> f[i][j];
            g[j] ^= f[i][j];
        }
    }

    for (int i = 1; i <= n; i++)
    {
        bool fl = true;
        for (int j = 1; j <= h - 1; j++)
        {
            if (f[i][j] != g[j + 1])
                fl = false;
        }
        for (int j = h; j <= m; j++)
        {
            if (f[i][j] != 0)
                fl = false;
        }
        if (fl)
        {
            r = i;
            break;
        }
    }

    for (int i = 1; i <= n; i++)
    {
        if (i == r)
            continue;
        int t = 0;
        for (int k = 1; k <= m; k += 2)
            t ^= f[r][k] ^ f[i][k];
        if (t)
        {
            s = t;
            break;
        }
    }
    w = s;
    for (int k = 1; k <= m; k++)
        w ^= f[r][k];
    cout << r << " " << w << endl;
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
